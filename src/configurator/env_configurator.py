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


class ENVConfigurator(ConfiguratorInterface):

    """
    The configurator takes data from environment variables.
    """

    @staticmethod
    def get_env_var_by_name(name) -> str:
        input_str = os.environ.get(name)
        if input_str is not None:
            return input_str
        else:
            raise ConfiguratorKeyError("Parameter {} was not provided to environment variables".format(name))

    def get_cloud_provider_ip(self) -> str:

        ip = self.get_env_var_by_name("engine_BM_IP")

        if ip_checker(ip):
            return ip
        else:
            raise ValidationValueError('Incorrect engine_BM_IP : ' + ip)

    def get_cloud_provider_engine_bm_login(self) -> str:

        bm_login = self.get_env_var_by_name("engine_BM_login")

        if name_checker(bm_login):
            return bm_login
        else:
            raise ValidationValueError('Incorrect engine_BM_login : ' + bm_login)

    def get_cloud_provider_engine_bm_password(self) -> str:

        password = self.get_env_var_by_name("engine_BM_password")

        if password_checker(password):
            return password
        else:
            raise ValidationValueError(
                'Incorrect engine_BM_password : ' + password)

    def get_cloud_provider_domain(self) -> str:

        domain = self.get_env_var_by_name("oVirt_domain_name")

        if cloud_provider_domain_check(domain):
            return domain
        else:
            raise ValidationValueError('Incorrect oVirt_domain_name : ' + domain)

    def get_cloud_provider_login(self) -> str:

        login = self.get_env_var_by_name("oVirt_Login")

        if cloud_provider_login_check(login):
            return login
        else:
            raise ValidationValueError('Incorrect oVirt_Login : ' + login)

    def get_cloud_provider_password(self) -> str:

        password = self.get_env_var_by_name("oVirt_Password")

        if password_checker(password):
            return password
        else:
            raise ValidationValueError('Incorrect oVirt_Password : ' + password)

    def get_cloud_provider_templates(self) -> list:

        templates = self.get_env_var_by_name("oVirt_Templates").split(' ')
        template_checker = True

        for template in templates:
            if cloud_provider_templates_check(template) and template in consts.images_links:
                template_checker = True
            else:
                template_checker = False
                break

        if template_checker:
            return templates
        else:
            raise ValidationValueError("oVirt template error in " + str(templates))

    def get_terraform_ip(self) -> str:

        ip = self.get_env_var_by_name("terraform_IP")

        if ip_checker(ip):
            return ip
        else:
            raise ValidationValueError('Incorrect terraform_IP : ' + ip)

    def get_terraform_login(self) -> str:

        login = self.get_env_var_by_name("terraform_login")

        if name_checker(login):
            return login
        else:
            raise ValidationValueError('Incorrect terraform_login : ' + login)

    def get_terraform_password(self) -> str:

        password = self.get_env_var_by_name("terraform_password")

        if password_checker(password):
            return password
        else:
            raise ValidationValueError(
                'Incorrect terraform_password : ' + password)

    def get_terraform_vm_name(self) -> str:
        name = self.get_env_var_by_name("terraform_name")

        if name_checker(name):
            return name
        else:
            raise ValidationValueError('Incorrect terraform_name : ' + name)

    def get_terraform_domain_name(self) -> str:

        domain = self.get_env_var_by_name("terraform_domain_name")

        if cloud_provider_domain_check(domain):
            return domain
        else:
            raise ValidationValueError(
                'Incorrect terraform_domain_name : ' + domain)

    def get_terraform_gateway(self) -> str:

        gateway = self.get_env_var_by_name("terraform_gateway")

        if ip_checker(gateway):
            return gateway
        else:
            raise ValidationValueError('Incorrect terraform_gateway : ' + gateway)

    def get_terraform_netmask(self) -> str:

        netmask = self.get_env_var_by_name("terraform_netmask")

        if ip_checker(netmask):
            return netmask
        else:
            raise ValidationValueError('Incorrect terraform_netmask : ' + netmask)

    def get_terraform_dns_search(self) -> str:

        dns = self.get_env_var_by_name("terraform_dns_search")

        if cloud_provider_domain_check(dns):
            return dns
        else:
            raise ValidationValueError(
                'Incorrect terraform_dns_search : ' + dns)

    def get_terraform_dns_servers(self) -> str:

        dns_servers = self.get_env_var_by_name("terraform_dns_servers")

        if ip_checker(dns_servers):
            return dns_servers
        else:
            raise ValidationValueError('Incorrect terraform_dns_servers : ' + dns_servers)

    def get_terraform_cpu(self) -> str:

        cpu_num = self.get_env_var_by_name("terraform_cpu")

        if hardware_requirements_check(cpu_num):
            return cpu_num
        else:
            raise ValidationValueError('Incorrect terraform_cpu : ' + cpu_num)

    def get_terraform_ram(self) -> str:

        ram = self.get_env_var_by_name("terraform_ram")

        if hardware_requirements_check(ram):
            return ram
        else:
            raise ValidationValueError('Incorrect terraform_ram : ' + ram)

    def get_terraform_os(self) -> str:

        terraform_os = self.get_env_var_by_name("terraform_os")

        if cloud_provider_templates_check(terraform_os):
            return terraform_os
        else:
            raise ValidationValueError('Incorrect terraform_os : ' + terraform_os)
