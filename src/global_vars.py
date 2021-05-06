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




"""
Contains global vars which using in project.
"""

path_to_deployment_playbooks = 'deployment_playbooks'

playbook_ovirt_setup = 'ovirt_playbooks/ovirt_setup.yml'
playbook_ovirt_cleanup = 'ovirt_playbooks/ovirt_cleanup.yml'
playbook_ovirt_check = 'ovirt_playbooks/ovirt_check.yml'
playbook_ovirt_delete_specific_vm = 'ovirt_playbooks/ovirt_delete_vm.yml'
playbook_ovirt_get_template_list = 'ovirt_playbooks/ovirt_templates_list.yml'
playbook_ovirt_create_template = 'ovirt_playbooks/ovirt_create_template.yml'
playbook_ovirt_get_vms_list = 'ovirt_playbooks/ovirt_vms_list.yml'
playbook_ovirt_get_nics_list = 'ovirt_playbooks/ovirt_get_nic.yml'

playbook_terraform_cleanup = 'terraform_playbooks/terraform_cleanup.yml'
playbook_terraform_setup = 'terraform_playbooks/terraform_setup.yml'
playbook_terraform_apply_template = 'terraform_playbooks/terraform_apply_vm_template.yml'

# default machine names
ovirt_machine_role = "ovirt server"
terraform_machine_role = "terraform"
terraform_script_directory_path = "main_fog"

template_fog_inventory = '{"all": {"hosts": {}}, "children": {}}'

images_links = {
    "centos76": "https://cloud.centos.org/altarch/7/images/CentOS-7-x86_64-GenericCloud.qcow2"
}