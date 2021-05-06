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


class OvirtProduct(ProductInterface):
    """
        The main function of the Product is a check
         that analyzes the actually deployed infrastructure and fills in
         the Product fields in accordance with the current state
         of the deployed computing infrastructure.
    """

    def __init__(self, configurator: ConfiguratorInterface):
        self.engine_BM_IP = None
        self.engine_BM_login = None
        self.engine_BM_password = None
        self.ovirt_domain_name = None
        self.ovirt_login = None
        self.ovirt_password = None
        self.ovirt_templates = None
        self.__check_state_by_conf(configurator)

    def __check_state_by_conf(self, configurator: ConfiguratorInterface):
        # Check if BM ssh connection available
        logger.info("Start checking ssh connection")
        if check_ssh(ip=configurator.get_cloud_provider_ip(), login=configurator.get_cloud_provider_engine_bm_login(),
                     password=configurator.get_cloud_provider_engine_bm_password()):
            self.engine_BM_IP = configurator.get_cloud_provider_ip()
            self.engine_BM_login = configurator.get_cloud_provider_engine_bm_login()
            self.engine_BM_password = configurator.get_cloud_provider_engine_bm_password()
        else:
            return
        logger.info("Check ssh connection: Done")

        # Check if oVirt is available
        # load inventory template

        # fill up inventory template with terraform and engine variables
        inventory = json.loads(consts.template_fog_inventory)
        inventory['all']['hosts']['engine'] = {"ansible_host": self.engine_BM_IP,
                                               "ansible_password": self.engine_BM_password,
                                               "ansible_port": 22,
                                               "ansible_user": self.engine_BM_login}

        # define vars for playbook
        ovirt_vars = {'ovirt_domain_name': configurator.get_cloud_provider_domain(),
                      'ovirt_user': configurator.get_cloud_provider_login(),
                      'ovirt_password': configurator.get_cloud_provider_password()}

        # run playbook to check oVirt for availability
        logger.info("Start checking oVirt availability")
        runner = ansible_runner.run(
            project_dir=consts.path_to_deployment_playbooks,
            playbook=consts.playbook_ovirt_check,
            inventory=inventory,
            extravars=ovirt_vars)

        if runner.status == 'successful':
            logger.info("oVirt is available")
            self.ovirt_domain_name = configurator.get_cloud_provider_domain()
            self.ovirt_login = configurator.get_cloud_provider_login()
            self.ovirt_password = configurator.get_cloud_provider_password()
        else:
            logger.info("oVirt is unavailable")
            return

        # Get list of templates from oVirt
        # run playbook to get list of templates from oVirt
        logger.info("Start playbook to get list of templates from oVirt")
        runner = ansible_runner.run(
            project_dir=consts.path_to_deployment_playbooks,
            playbook=consts.playbook_ovirt_get_template_list,
            inventory=inventory,
            extravars=ovirt_vars)

        if runner.status == 'successful':
            logger.info("Get list of templates from oVirt: successfully recieved")
            # load oVit templates json
            with open('ovirt/templates.json') as file:
                ovirt_templates_json_str = file.read()
            ovirt_templates_json = json.loads(ovirt_templates_json_str)
            self.ovirt_templates = []
            for item in ovirt_templates_json:
                self.ovirt_templates.append(item['name'])
        else:
            logger.info("Get list of templates from oVirt: failed")

    def __eq__(self, other):
        if isinstance(other, OvirtProduct):
            return self.engine_BM_IP == other.engine_BM_IP and \
                   self.engine_BM_login == other.engine_BM_login and \
                   self.engine_BM_password == other.engine_BM_password and \
                   self.ovirt_domain_name == other.ovirt_domain_name and \
                   self.ovirt_login == other.ovirt_login and \
                   self.ovirt_password == other.ovirt_password and \
                   Counter(self.ovirt_templates) == Counter(other.ovirt_templates)
        return False
