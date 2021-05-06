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



from src.builder.builder_parent import *
import os


class VMStatusError(ValueError):
    pass


class TerraformAppError(ValueError):
    pass


class TerraformBuilder(Builder):
    """The builder follows the instructions to create the desired infrastructure for terraform"""
    def __init__(self, product: TerraformProduct, configurator: ConfiguratorInterface) -> None:

        super().__init__(product, configurator)
        self._product = product

        # load main parameters from configurator
        self.terraform_ip = configurator.get_terraform_ip()
        self.terraform_login = configurator.get_terraform_login()
        self.terraform_password = configurator.get_terraform_password()
        self.terraform_vm_name = configurator.get_terraform_vm_name()

    def test_product(self) -> bool:
        # Check that the configuration matches the product
        if self.terraform_ip == self._product.terraform_ip and \
                self.terraform_login == self._product.terraform_login and \
                self.terraform_password == self._product.terraform_password and \
                self.terraform_vm_name == self._product.terraform_vm_name:
            return True
        else:
            return False

    def prepare_inv_file(self):
        # fill up inventory template with terraform and engine variables
        inventory = json.loads(consts.template_fog_inventory)
        inventory['all']['hosts']['terraform'] = \
            {"ansible_host": self.terraform_ip,
             "ansible_password": self.terraform_password,
             "ansible_port": 22,
             "ansible_user": self.terraform_login}
        return inventory

    def product(self) -> TerraformProduct:
        return self._product

    def build_product(self) -> None:
        pass

    def annotate_product(self) -> None:
        pass


class TerraformSetupBuilder(TerraformBuilder):

    def __init__(self, product: TerraformProduct, configurator: ConfiguratorInterface) -> None:
        super().__init__(product, configurator)
        self.terraform_domain_name = configurator.get_terraform_domain_name()
        self.terraform_gateway = configurator.get_terraform_gateway()
        self.terraform_netmask = configurator.get_terraform_netmask()
        self.terraform_dns_search = configurator.get_terraform_dns_search()
        self.terraform_dns_servers = configurator.get_terraform_dns_servers()
        self.terraform_cpu = configurator.get_terraform_cpu()
        self.terraform_ram = configurator.get_terraform_ram()
        self.terraform_os = configurator.get_terraform_os()

    def product(self) -> TerraformProduct:
        return self._product

    def prepare_inv_file(self):
        inventory = super().prepare_inv_file()
        inventory['all']['hosts']['engine'] = \
            {"ansible_host": self._configurator.get_cloud_provider_ip(),
             "ansible_password": self._configurator.get_cloud_provider_engine_bm_password(),
             "ansible_port": 22,
             "ansible_user": self._configurator.get_cloud_provider_engine_bm_login()}
        return inventory

    def create_terraform_vm(self):
        inventory = self.prepare_inv_file()
        # define vars for playbook
        ansible_vars = {'ovirt_domain_name': self._configurator.get_cloud_provider_domain(),
                        'ovirt_user': self._configurator.get_cloud_provider_login(),
                        'ovirt_password': self._configurator.get_cloud_provider_password(),
                        'terraform_vm_name': self.terraform_vm_name,
                        'terraform_template': self.terraform_os,
                        'terraform_ram': self.terraform_ram,
                        'terraform_cpu': self.terraform_cpu,
                        'terraform_dns_servers': self.terraform_dns_servers,
                        'terraform_dns_search': self.terraform_dns_search,
                        'terraform_ip': self.terraform_ip,
                        'terraform_netmask': self.terraform_netmask,
                        'terraform_gateway': self.terraform_gateway,
                        'terraform_domain_name': self.terraform_domain_name,
                        'terraform_login': self.terraform_login,
                        'terraform_password': self.terraform_password}

        logger.info("Start playbook to setup Terraform vm")
        os.system(" ssh-keygen -R \"{}\"".format(self.terraform_ip))
        runner = ansible_runner.run(project_dir=consts.path_to_deployment_playbooks,
                                    playbook=consts.playbook_terraform_setup,
                                    extravars=ansible_vars, inventory=inventory,
                                    status_handler=ansible_status_handler, finished_callback=fog_finished_callback())

        # Update current product state
        if runner.status == 'successful':
            self._product.vm_exist = True
            self._product.vm_status = True
            self._product.terraform_ip = self.terraform_ip
            self._product.terraform_vm_name = self.terraform_vm_name
            self._product.terraform_login = self.terraform_login
            self._product.terraform_password = self.terraform_password
            self._product.terraform_domain_name = self.terraform_domain_name
            self._product.terraform_gateway = self.terraform_gateway
            self._product.terraform_netmask = self.terraform_netmask
            self._product.terraform_dns_search = self.terraform_dns_search
            self._product.terraform_dns_servers = self.terraform_dns_servers
            self._product.terraform_cpu = self.terraform_cpu
            self._product.terraform_ram = self.terraform_ram
            self._product.terraform_os = self.terraform_os
            self._product.terraform_app = True
            logger.info("Setup Terraform vm done")
        else:
            logger.error("Ansible Terraform vm setup playbook: failed")

    def build_product(self) -> None:
        response = os.system("ping -c 1 " + self.terraform_ip)

        if self._product.vm_exist:

            if not self._product.vm_status:
                logger.error("VMstatus error")
                raise VMStatusError("VM status incorrect")
            if not self._product.terraform_app:
                raise TerraformAppError("Terraform App status incorrect")
            if self.test_product():
                logger.info("Configuration for Terraform is already setup")
                return None
            else:
                logger.info("Terraform vm need to update")
                self.create_terraform_vm()

        else:

            logger.info("Terraform vm doesn't exist")
            logger.info("Starting IP available check ")
            if response != 0:
                logger.info("IP available")
                self.create_terraform_vm()
            else:
                logger.error("IP doesn't availability")

    def annotate_product(self) -> None:
        pass


class TerraformCleanupBuilder(TerraformBuilder):

    def __init__(self, product: TerraformProduct, configurator: ConfiguratorInterface) -> None:
        super().__init__(product, configurator)

    def product(self) -> TerraformProduct:
        return self._product

    def prepare_inv_file(self):
        inventory = super().prepare_inv_file()

        inventory['all']['hosts']['engine'] = \
            {"ansible_host": self._configurator.get_cloud_provider_ip(),
             "ansible_password": self._configurator.get_cloud_provider_engine_bm_password(),
             "ansible_port": 22,
             "ansible_user": self._configurator.get_cloud_provider_engine_bm_login()}
        return inventory

    def delete_terraform_vm(self):
        inventory = self.prepare_inv_file()
        ansible_vars = {'ovirt_domain_name': self._configurator.get_cloud_provider_domain(),
                        'ovirt_user': self._configurator.get_cloud_provider_login(),
                        'ovirt_password': self._configurator.get_cloud_provider_password(),
                        'engine_password': self._configurator.get_cloud_provider_password(),
                        'machine_name': self.terraform_vm_name,
                        'infra_part': consts.terraform_script_directory_path}

        os.system(" ssh-keygen -R \"{}\"".format(self.terraform_ip))
        runner = ansible_runner.run(project_dir=consts.path_to_deployment_playbooks,
                                    playbook=consts.playbook_terraform_cleanup, extravars=ansible_vars,
                                    inventory=inventory,
                                    status_handler=ansible_status_handler, finished_callback=fog_finished_callback())

        # Update current product state
        if runner.status == 'successful':
            self.update_product()
            logger.info("Cleanup Terraform vm done")
        else:
            logger.error("Ansible Terraform vm cleanup playbook ends without successful status")

    def update_product(self):
        self._product.vm_exist = False
        self._product.vm_status = False
        self._product.terraform_ip = None
        self._product.terraform_vm_name = None
        self._product.terraform_login = None
        self._product.terraform_password = None
        self._product.terraform_domain_name = None
        self._product.terraform_gateway = None
        self._product.terraform_netmask = None
        self._product.terraform_dns_search = None
        self._product.terraform_dns_servers = None
        self._product.terraform_cpu = None
        self._product.terraform_ram = None
        self._product.terraform_os = None
        self._product.terraform_app = False

    def test_product(self) -> bool:
        if not self._product.vm_exist and \
                not self._product.vm_status and \
                not self._product.terraform_app and \
                self._product.terraform_ip is None and \
                self._product.terraform_vm_name is None and \
                self._product.terraform_login is None and \
                self._product.terraform_password is None and \
                self._product.terraform_domain_name is None and \
                self._product.terraform_gateway is None and \
                self._product.terraform_netmask is None and \
                self._product.terraform_dns_search is None and \
                self._product.terraform_dns_servers is None and \
                self._product.terraform_cpu is None and \
                self._product.terraform_ram is None and \
                self._product.terraform_os is None and \
                not self._product.terraform_app:
            return True
        else:
            return False

    def build_product(self) -> None:
        if self.test_product():
            logger.info("Configuration for Terraform is already cleanup")
            return
        else:
            logger.info("Starting Terraform cleanup")
            self.delete_terraform_vm()


class TerraformApplyTemplate(TerraformBuilder):

    def __init__(self, product: TerraformProduct, configurator: ConfiguratorInterface) -> None:
        super().__init__(product, configurator)

    def product(self) -> TerraformProduct:
        return self._product

    def apply_template(self):
        inventory = self.prepare_inv_file()

        # run terraform playbook to apply Terraform template
        logger.info("Start playbook to setup Terraform vm")
        os.system(" ssh-keygen -R \"{}\"".format(self.terraform_ip))
        runner = ansible_runner.run(project_dir=consts.path_to_deployment_playbooks,
                                    playbook=consts.playbook_terraform_apply_template,
                                    inventory=inventory,
                                    status_handler=ansible_status_handler, finished_callback=fog_finished_callback())

    def build_product(self) -> None:
        self.apply_template()

    def annotate_product(self) -> None:
        pass
