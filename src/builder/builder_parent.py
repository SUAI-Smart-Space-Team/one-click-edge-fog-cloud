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



from abc import ABC, abstractmethod
from src.product.ovirt_product import *
from src.product.terraform_product import *


class AnsibleException(Exception):
    pass


def ansible_status_handler(status_data, runner_config):
    logger.info('Send data to web to update status for {}'.format(status_data['status']))
    if status_data['status'] == 'failed':
        raise AnsibleException("Ansible playbook {} return status failed".format(runner_config.playbook))


def fog_finished_callback():
    logger.info("Maybe here will need to update database")


class Builder(ABC):
    """
    The Builder interface specifies methods for creating the different parts of
    the Product objects.
    """

    def __init__(self, product: ProductInterface, configurator: ConfiguratorInterface):
        self._product = product
        self._configurator = configurator

    @property
    @abstractmethod
    def product(self) -> None:
        pass

    @abstractmethod
    def test_product(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def build_product(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def annotate_product(self) -> None:
        raise NotImplementedError
