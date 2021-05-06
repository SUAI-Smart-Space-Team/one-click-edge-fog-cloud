"""
 Copyright (c) 2021 Dell Inc, or its subsidiaries.
 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at
      http://www.apache.org/licenses/LICENSE-2.0
 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""


from src.product.parent_product import *


class TerraformProduct(ProductInterface):
    """
        The main function of the Product is a check
         that analyzes the actually deployed infrastructure and fills in
         the Product fields in accordance with the current state
         of the deployed computing infrastructure.
    """
    def __init__(self, configurator: ConfiguratorInterface):
        self.vm_exist = False
        self.vm_status = False
        self.terraform_ip = None
        self.terraform_vm_name = None
        self.terraform_login = None
        self.terraform_password = None
        self.terraform_domain_name = None
        self.terraform_gateway = None
        self.terraform_netmask = None
        self.terraform_dns_search = None
        self.terraform_dns_servers = None
        self.terraform_cpu = None
        self.terraform_ram = None
        self.terraform_os = None
        self.terraform_app = False
        self.__check_state_by_conf(configurator)

    def __check_state_by_conf(self, configurator: ConfiguratorInterface):
        """
        This function used for comparison of the received infrastructure with the desired.
        """
        # Check if BM exist in oVirt

        # fill up inventory template with terraform and engine variables
        inventory = json.loads(consts.template_fog_inventory)
        inventory['all']['hosts']['engine'] = {"ansible_host": configurator.get_cloud_provider_ip(),
                                               "ansible_password": configurator.get_cloud_provider_engine_bm_password(),
                                               "ansible_port": 22,
                                               "ansible_user": configurator.get_cloud_provider_engine_bm_login()}

        # define vars for playbook
        evars = {'ovirt_domain_name': configurator.get_cloud_provider_domain(),
                 'ovirt_user': configurator.get_cloud_provider_login(),
                 'ovirt_password': configurator.get_cloud_provider_password()}

        # run playbook to get list of vms from oVirt
        logger.info("Start playbook to get list of vms from oVirt")
        ansible_runner.run(
            project_dir=consts.path_to_deployment_playbooks,
            playbook=consts.playbook_ovirt_get_vms_list,
            inventory=inventory,
            extravars=evars)

        # load oVit vms json
        with open('ovirt/vms.json') as file:
            ovirt_vms_json_str = file.read()
        ovirt_vms_json = json.loads(ovirt_vms_json_str)

        # find terraform vm
        template_id = ''
        nic_id = ''
        for item in ovirt_vms_json:
            if item["name"] == configurator.get_terraform_vm_name():
                self.vm_exist = True
                self.vm_status = (item["status"] == "up")
                self.terraform_vm_name = item["name"]
                self.terraform_domain_name = item["fqdn"]
                self.terraform_cpu = str(item["cpu"]["topology"]["cores"])
                self.terraform_ram = str(int(item["memory"] / 1048576))  # because of bytes representation
                template_id = item["template"]["id"]
                nic_id = item["nics"][0]["id"]
                break

        if self.vm_exist:
            # run playbook to get list of templates from oVirt
            logger.info("Start playbook to get list of templates from oVirt")
            ansible_runner.run(
                project_dir=consts.path_to_deployment_playbooks,
                playbook=consts.playbook_ovirt_get_template_list,
                inventory=inventory,
                extravars=evars)

            with open('ovirt/templates.json') as file:
                ovirt_templates_json_str = file.read()
            ovirt_templates_json = json.loads(ovirt_templates_json_str)

            for item in ovirt_templates_json:
                if item["id"] == template_id:
                    self.terraform_os = item["name"]
                    break

            # run playbook to get list of nics from oVirt
            evars["vm_name"] = self.terraform_vm_name
            logger.info("Start playbook to get nics for vm")
            ansible_runner.run(
                project_dir=consts.path_to_deployment_playbooks,
                playbook=consts.playbook_ovirt_get_nics_list,
                inventory=inventory,
                extravars=evars)

            with open('ovirt/nics.json') as file:
                ovirt_nics_json_str = file.read()
            ovirt_nics_json = json.loads(ovirt_nics_json_str)

            for item in ovirt_nics_json:
                if item["id"] == nic_id:
                    for ip in item["reported_devices"][0]["ips"]:
                        if ip["version"] == "v4":
                            self.terraform_ip = ip["address"]
                            break
                    break

        if self.terraform_ip == configurator.get_terraform_ip() and self.vm_status:
            ssh = SSHClient()
            ssh.set_missing_host_key_policy(AutoAddPolicy())
            try:
                # Check if BM ssh connection available
                ssh.connect(self.terraform_ip, username=configurator.get_terraform_login(),
                            password=configurator.get_terraform_password())
                self.terraform_login = configurator.get_terraform_login()
                self.terraform_password = configurator.get_terraform_password()

                # Check network parameters
                sftp_client = ssh.open_sftp()
                remote_file = sftp_client.open('/etc/sysconfig/network-scripts/ifcfg-eth0')
                for line in remote_file:
                    if line.startswith("DNS1"):
                        self.terraform_dns_servers = line.split("=")[1].strip()
                    elif line.startswith("DOMAIN"):
                        self.terraform_dns_search = line.split("=")[1].strip()
                    elif line.startswith("GATEWAY"):
                        self.terraform_gateway = line.split("=")[1].strip()
                    elif line.startswith("NETMASK"):
                        self.terraform_netmask = line.split("=")[1].strip()
                    if self.terraform_dns_servers is not None and self.terraform_dns_search is not None and \
                            self.terraform_gateway is not None and self.terraform_netmask is not None:
                        break

                # Check terraform install
                if sftp_exists(sftp_client, "/root/terraform/modules") and \
                        sftp_exists(sftp_client, "/root/terraform/main") and \
                        sftp_exists(sftp_client, "/usr/local/bin/terraform"):
                    self.terraform_app = True

                sftp_client.close()
                ssh.close()

            except (BadHostKeyException, AuthenticationException,
                    SSHException, socket.error) as e:
                logger.error(e)
        else:
            logger.info("The IP of the machine and the IP in configurator are not equal.\n Or the machine "
                        "status is \"False\"")

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, TerraformProduct):
            return self.vm_exist == other.vm_exist and \
                   self.vm_status == other.vm_status and \
                   self.terraform_ip == other.terraform_ip and \
                   self.terraform_vm_name == other.terraform_vm_name and \
                   self.terraform_login == other.terraform_login and \
                   self.terraform_password == other.terraform_password and \
                   self.terraform_domain_name == other.terraform_domain_name and \
                   self.terraform_gateway == other.terraform_gateway and \
                   self.terraform_netmask == other.terraform_netmask and \
                   self.terraform_dns_search == other.terraform_dns_search and \
                   self.terraform_dns_servers == other.terraform_dns_servers and \
                   self.terraform_cpu == other.terraform_cpu and \
                   self.terraform_ram == other.terraform_ram and \
                   self.terraform_os == other.terraform_os and \
                   self.terraform_app == other.terraform_app
        return False
