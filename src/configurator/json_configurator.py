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



from src.configurator.configurator_parent import *

class JSONConfigurator(ConfiguratorInterface):

    """The configurator takes data from json file."""

    def __init__(self, path_to_json_file: str) -> None:
        self.path_to_json_file = path_to_json_file
        self.conf_dict = {}

        self.ovirt_machine = {}
        self.terraform_machine = {}

        self.load_conf_data()

    def load_conf_data(self):
        with open(self.path_to_json_file) as file:
            config_str = file.read()

        EFC_json_config = json.loads(config_str)
        self.conf_dict = EFC_json_config["fogs"][0]

    def load_ovirt_machine(self):
        for machine in self.conf_dict['infrastructure_config']:
            if machine['machine_role']['name'] == consts.ovirt_machine_role:  # find machine for virtualization_server
                self.ovirt_machine = machine

    def load_terraform_machine(self):
        for machine in self.conf_dict['infrastructure_config']:
            if machine['machine_role']['name'] == consts.terraform_machine_role:  # find machine for terraform
                self.terraform_machine = machine

    def get_cloud_provider_ip(self) -> str:
        if self.ovirt_machine == {}:
            self.load_ovirt_machine()

        ip = self.ovirt_machine["network"]["ip"]

        if ip_checker(ip):
            return ip
        else:
            raise ValidationValueError('Incorrect engine_BM_IP : ' + ip)

    def get_cloud_provider_engine_bm_login(self) -> str:
        if self.ovirt_machine == {}:
            self.load_ovirt_machine()

        bm_login = self.ovirt_machine["credential"]["login"]

        if name_checker(bm_login):
            return bm_login
        else:
            raise ValidationValueError('Incorrect engine_BM_login : ' + bm_login)

    def get_cloud_provider_engine_bm_password(self) -> str:
        if self.ovirt_machine == {}:
            self.load_ovirt_machine()

        password = self.ovirt_machine["credential"]["password"]

        if password_checker(password):
            return password
        else:
            raise ValidationValueError(
                'Incorrect engine_BM_password : ' + password)

    def get_cloud_provider_domain(self) -> str:

        domain = self.conf_dict["cloud_provider"]["network"]["dns_name"]

        if cloud_provider_domain_check(domain):
            return domain
        else:
            raise ValidationValueError('Incorrect oVirt_domain_name : ' + domain)

    def get_cloud_provider_login(self) -> str:

        login = self.conf_dict["cloud_provider"]["credential"]["login"]

        if cloud_provider_login_check(login):
            return login
        else:
            raise ValidationValueError('Incorrect oVirt_Login : ' + login)

    def get_cloud_provider_password(self) -> str:

        password = self.conf_dict["cloud_provider"]["credential"]["password"]

        if password_checker(password):
            return password
        else:
            raise ValidationValueError('Incorrect oVirt_Password : ' + password)

    def get_cloud_provider_templates(self) -> list:
        lsit_of_os = []
        for machine in self.conf_dict['infrastructure_config']:
            os_name = re.sub('[ ?.!/;:]', '', machine['operation_system']['name']).lower()  # get machine os
            if os_name not in lsit_of_os:
                if name_checker(os_name):
                    lsit_of_os.append(os_name)
                else:
                    raise ValidationValueError('Incorrect oVirt template name: ' + os_name)
        return lsit_of_os

    def get_terraform_ip(self) -> str:
        if self.terraform_machine == {}:
            self.load_terraform_machine()

        ip = self.terraform_machine["network"]["ip"]

        if ip_checker(ip):
            return ip
        else:
            raise ValidationValueError('Incorrect terraform_IP : ' + ip)

    def get_terraform_login(self) -> str:
        if self.terraform_machine == {}:
            self.load_terraform_machine()

        login = self.terraform_machine["credential"]["login"]

        if name_checker(login):
            return login
        else:
            raise ValidationValueError('Incorrect terraform_login : ' + login)

    def get_terraform_password(self) -> str:
        if self.terraform_machine == {}:
            self.load_terraform_machine()

        password = self.terraform_machine["credential"]["password"]

        if password_checker(password):
            return password
        else:
            raise ValidationValueError(
                'Incorrect terraform_password : ' + password)

    def get_terraform_vm_name(self) -> str:
        if self.terraform_machine == {}:
            self.load_terraform_machine()

        name = self.terraform_machine["name"]

        if name_checker(name):
            return name
        else:
            raise ValidationValueError('Incorrect terraform_name : ' + name)

    def get_terraform_domain_name(self) -> str:
        if self.terraform_machine == {}:
            self.load_terraform_machine()

        domain = self.terraform_machine["network"]["dns_name"]

        if cloud_provider_domain_check(domain):
            return domain
        else:
            raise ValidationValueError(
                'Incorrect terraform_domain_name : ' + domain)

    def get_terraform_gateway(self) -> str:
        if self.terraform_machine == {}:
            self.load_terraform_machine()

        gateway = self.terraform_machine["network"]["gateway"]

        if ip_checker(gateway):
            return gateway
        else:
            raise ValidationValueError('Incorrect terraform_gateway : ' + gateway)

    def get_terraform_netmask(self) -> str:
        if self.terraform_machine == {}:
            self.load_terraform_machine()

        netmask = self.terraform_machine["network"]["netmask"]

        if ip_checker(netmask):
            return netmask
        else:
            raise ValidationValueError('Incorrect terraform_netmask : ' + netmask)

    def get_terraform_dns_search(self) -> str:
        if self.terraform_machine == {}:
            self.load_terraform_machine()

        dns = self.terraform_machine["network"]["dns_search"]

        if cloud_provider_domain_check(dns):
            return dns
        else:
            raise ValidationValueError(
                'Incorrect terraform_dns_search : ' + dns)

    def get_terraform_dns_servers(self) -> str:
        if self.terraform_machine == {}:
            self.load_terraform_machine()

        dns_servers = self.terraform_machine["network"]["dns_servers"]

        if ip_checker(dns_servers):
            return dns_servers
        else:
            raise ValidationValueError('Incorrect terraform_dns_servers : ' + dns_servers)

    def get_terraform_cpu(self) -> str:
        if self.terraform_machine == {}:
            self.load_terraform_machine()

        cpu_num = str(self.terraform_machine["resource"]["cpu"])

        if hardware_requirements_check(cpu_num):
            return cpu_num
        else:
            raise ValidationValueError('Incorrect terraform_cpu : ' + cpu_num)

    def get_terraform_ram(self) -> str:
        if self.terraform_machine == {}:
            self.load_terraform_machine()

        ram = str(self.terraform_machine["resource"]["ram"])

        if hardware_requirements_check(ram):
            return ram
        else:
            raise ValidationValueError('Incorrect terraform_ram : ' + ram)

    def get_terraform_os(self) -> str:
        if self.terraform_machine == {}:
            self.load_terraform_machine()
        terraform_os = re.sub('[ ?.!/;:]', '', self.terraform_machine["operation_system"]["name"]).lower()
        if name_checker(terraform_os):
            return terraform_os
        else:
            raise ValidationValueError('Incorrect terraform_os : ' + terraform_os)
