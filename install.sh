#!/bin/bash
pip3 install -r requirements.txt
ansible-galaxy collection install ovirt.ovirt
ansible-galaxy install ovirt.engine-setup
ansible-galaxy install fubarhouse.golang
pip3 install ansible-runner loguru paramiko

