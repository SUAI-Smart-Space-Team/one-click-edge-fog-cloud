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




import time

from src.builder.builder_parent import *


class OvirtBuilder(Builder):

    """The builder follows the instructions to create the desired infrastructure for ovirt"""

    def __init__(self, product: OvirtProduct, configurator: ConfiguratorInterface) -> None:

        super().__init__(product, configurator)
        self._product = product

        # load main parameters from configurator
        self.engine_BM_IP = self._configurator.get_cloud_provider_ip()
        self.engine_BM_login = self._configurator.get_cloud_provider_engine_bm_login()
        self.engine_BM_password = self._configurator.get_cloud_provider_engine_bm_password()
        self.ovirt_domain_name = self._configurator.get_cloud_provider_domain()
        self.ovirt_login = self._configurator.get_cloud_provider_login()
        self.ovirt_password = self._configurator.get_cloud_provider_password()

    def test_product(self) -> bool:
        # Check that the configuration matches the product
        if self.engine_BM_IP == self._product.engine_BM_IP and \
                self.engine_BM_login == self._product.engine_BM_login and \
                self.engine_BM_password == self._product.engine_BM_password and \
                self.ovirt_domain_name == self._product.ovirt_domain_name and \
                self.ovirt_login == self._product.ovirt_login and \
                self.ovirt_password == self._product.ovirt_password:
            return True
        else:
            return False

    def prepare_inv_file(self):

        # fill up inventory template with terraform and engine variables
        inventory = json.loads(consts.template_fog_inventory)
        inventory['all']['hosts']['engine'] = {"ansible_host": self.engine_BM_IP,
                                               "ansible_password": self.engine_BM_password,
                                               "ansible_port": 22,
                                               "ansible_user": self.engine_BM_login}
        return inventory

    def product(self) -> OvirtProduct:
        return self._product

    def build_product(self) -> None:
        pass

    def annotate_product(self) -> None:
        pass


class OvirtCleanupBuilder(OvirtBuilder):

    def __init__(self, product: OvirtProduct, configurator: ConfiguratorInterface) -> None:
        super().__init__(product, configurator)

    def product(self) -> OvirtProduct:
        return self._product

    def test_product(self) -> bool:
        # Check that the configuration matches the product
        # In cleanup case product must be empty or only BM available
        if self._product.ovirt_domain_name is None and \
                self._product.ovirt_login is None and \
                self._product.ovirt_password is None:
            return True
        else:
            return False

    def build_product(self) -> None:

        # Check that the configuration matches the product
        if self.test_product():
            logger.info("Configuration for removed oVirt is already setup")
            return

        inventory = self.prepare_inv_file()

        logger.info("Start playbook to cleanup oVirt")
        runner = ansible_runner.run(
            project_dir=consts.path_to_deployment_playbooks, playbook=consts.playbook_ovirt_cleanup,
            inventory=inventory,
            status_handler=ansible_status_handler,
            finished_callback=fog_finished_callback())

        # wait 3 min, else bug with proxy
        time.sleep(180)

        # Update current product state: reset product parameters
        if runner.status == 'successful':
            self._product.ovirt_domain_name = None
            self._product.ovirt_login = None
            self._product.ovirt_password = None
            self._product.ovirt_templates = None
            logger.info("Cleanup done")
        else:
            logger.error("Ansible ovirt cleanup playbook: failed")

    def annotate_product(self) -> None:
        pass


class OvirtSetupBuilder(OvirtBuilder):

    def __init__(self, product: OvirtProduct, configurator: ConfiguratorInterface) -> None:
        super().__init__(product, configurator)

    def product(self) -> OvirtProduct:
        return self._product

    def build_product(self) -> None:

        # Check that the configuration matches the product
        if self.test_product():
            logger.info("Configuration for oVirt is already setup")
            return

        # Create answers file for oVirt installation
        with open('ovirt/template_ovirt_answers.yml', "r") as template_file:
            template = template_file.read()
        with open('ovirt/ovirt_answers', "w") as answers_file:
            answers_file.write(template.format(self.ovirt_password,
                                               self.ovirt_domain_name))

        inventory = self.prepare_inv_file()
        ansible_vars = {'ovirt_domain_name': self.ovirt_domain_name,
                        'ovirt_user': self.ovirt_login,
                        'ovirt_password': self.ovirt_password,
                        'engine_password': self.engine_BM_password}

        logger.info("Start playbook to setup oVirt")
        runner = ansible_runner.run(project_dir=consts.path_to_deployment_playbooks,
                                    playbook=consts.playbook_ovirt_setup,
                                    extravars=ansible_vars, inventory=inventory,
                                    status_handler=ansible_status_handler, finished_callback=fog_finished_callback())

        # Update current product state
        if runner.status == 'successful':
            self.update_product()
            logger.info("Setup done")
        else:
            logger.error("Ansible ovirt setup playbook: failed")

    def update_product(self):
        self._product.engine_BM_IP = self.engine_BM_IP
        self._product.BM_login = self.engine_BM_login
        self._product.engine_BM_password = self.engine_BM_password
        self._product.ovirt_domain_name = self.ovirt_domain_name
        self._product.ovirt_login = self.ovirt_login
        self._product.ovirt_password = self.ovirt_password
        self._product.ovirt_templates = ['Blank']  # add default oVirt template

    def annotate_product(self) -> None:
        pass


class OvirtAddTemplateBuilder(OvirtBuilder):

    def __init__(self, product: OvirtProduct, configurator: ConfiguratorInterface) -> None:
        super().__init__(product, configurator)

        # load addition parameters from configurator
        self.ovirt_templates = self._configurator.get_cloud_provider_templates()
        self.template_domain_name = configurator.get_terraform_domain_name()
        self.template_gateway = configurator.get_terraform_gateway()
        self.template_netmask = configurator.get_terraform_netmask()
        self.template_dns_search = configurator.get_terraform_dns_search()
        self.template_dns_servers = configurator.get_terraform_dns_servers()
        self.template_login = configurator.get_terraform_login()
        self.template_password = configurator.get_terraform_password()
        self.template_ip = configurator.get_terraform_ip()
        self.template_cpu = configurator.get_terraform_cpu()
        self.template_ram = configurator.get_terraform_ram()

    def test_product(self) -> bool:
        # Check that the configuration matches the product
        if super().test_product() and [template for template in self.ovirt_templates
                                       if template not in self._product.ovirt_templates] == []:
            return True
        else:
            return False

    def build_product(self) -> None:
        # Check if previous required steps are complete (oVirt installed)
        if not super().test_product():
            logger.error("Previous required steps are complete: oVirt hasn't install")
            return

        # Check that the configuration matches the product
        if self.test_product():
            logger.info("Configuration for oVirt templates is already setup")
            return

        inventory = self.prepare_inv_file()

        for template in self.ovirt_templates:
            if template not in self._product.ovirt_templates:
                image_link = consts.images_links[template]
                # define vars for playbook
                # The terraform settings are used to create the template.
                ansible_vars = {'ovirt_domain_name': self.ovirt_domain_name,
                                'ovirt_user': self.ovirt_login,
                                'ovirt_password': self.ovirt_password,
                                'template_dns_servers': self.template_dns_servers,
                                'template_dns_search': self.template_dns_search,
                                'template_ip': self.template_ip,
                                'template_netmask': self.template_netmask,
                                'template_gateway': self.template_gateway,
                                'template_domain_name': self.template_domain_name,
                                'template_login': self.template_login,
                                'template_password': self.template_password,
                                'template_ram': self.template_ram,
                                'template_cpu': self.template_cpu,
                                'template_name': template,
                                'template_link': image_link,
                                'template_path': image_link[image_link.index("CentOS"):]
                                }
                logger.info("Start playbook to add {} template in oVirt".format(template))
                ansible_runner.run(project_dir=consts.path_to_deployment_playbooks,
                                   playbook=consts.playbook_ovirt_create_template,
                                   extravars=ansible_vars, inventory=inventory,
                                   status_handler=ansible_status_handler,
                                   finished_callback=fog_finished_callback())

        # Update current product state
        for template in self.ovirt_templates:
            if template not in self._product.ovirt_templates:
                self._product.ovirt_templates.append(template)
