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



import abc
import json
import os
import re

import src.global_vars as consts


class ConfiguratorKeyError(KeyError):
    pass


class ValidationValueError(ValueError):
    pass


class ConfiguratorInterface(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_cloud_provider_ip(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def get_cloud_provider_engine_bm_login(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def get_cloud_provider_engine_bm_password(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def get_cloud_provider_domain(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def get_cloud_provider_login(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def get_cloud_provider_password(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def get_cloud_provider_templates(self) -> list:
        raise NotImplementedError

    @abc.abstractmethod
    def get_terraform_ip(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def get_terraform_login(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def get_terraform_password(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def get_terraform_vm_name(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def get_terraform_domain_name(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def get_terraform_gateway(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def get_terraform_netmask(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def get_terraform_dns_search(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def get_terraform_dns_servers(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def get_terraform_cpu(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def get_terraform_ram(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def get_terraform_os(self) -> str:
        raise NotImplementedError


def ip_checker(env_str) -> bool:
    if re.match(r'^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25['
                r'0-5])$', env_str):
        return True
    else:
        return False


def name_checker(env_str) -> bool:
    if re.match(r'^[a-zA-Z0-9-_]{3,}$', env_str):
        return True
    else:
        return False


def password_checker(env_str) -> bool:
    if re.match(r'^[a-zA-Z0-9!#$@%?()_-]{3,}$', env_str):
        return True
    else:
        return False


def cloud_provider_templates_check(env_str) -> bool:
    if re.match(r'^[a-zA-Z0-9_!#?/&^%]{3,}$', env_str):
        return True
    else:
        return False


def cloud_provider_login_check(env_str) -> bool:
    if re.match(r'^[a-zA-Z0-9_]{3,}@internal$', env_str):
        return True
    else:
        return False


def cloud_provider_domain_check(env_str) -> bool:
    if re.match(r'^(?!\-)(?:[a-zA-Z\d\-]{0,62}[a-zA-Z\d]\.){1,126}(?!\d+)[a-zA-Z\d]{1,63}$', env_str):
        return True
    else:
        return False


def hardware_requirements_check(env_str) -> bool:
    if env_str.isdigit() and int(env_str) > 0:
        return True
    else:
        return False


