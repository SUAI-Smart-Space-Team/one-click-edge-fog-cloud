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
from collections import Counter
from enum import Enum
import socket
from time import sleep
import ansible_runner
from loguru import logger
from src.configurator.configurator_parent import ConfiguratorInterface
from paramiko import SSHClient, AutoAddPolicy, BadHostKeyException, AuthenticationException, SSHException
import json
import src.global_vars as consts


def check_ssh(ip, login, password, initial_wait=0, interval=0, retries=1):
    ssh = SSHClient()
    ssh.set_missing_host_key_policy(AutoAddPolicy())

    sleep(initial_wait)

    for x in range(retries):
        try:
            ssh.connect(ip, username=login, password=password)
            ssh.close()
            return True
        except (BadHostKeyException, AuthenticationException,
                SSHException, socket.error) as e:
            logger.info(e)
            sleep(interval)
    return False


def sftp_exists(sftp, path):
    try:
        sftp.stat(path)
        return True
    except IOError as e:
        if e[0] == 2:
            return False
        else:
            raise e


class ProductInterface(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __eq__(self, other):
        raise NotImplementedError
