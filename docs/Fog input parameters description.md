# Fog input parameters description

## Note 

Here we provide only a description of all Fog input parameters. Information about modules and their required parameters is described in [README](../README.md). The parameters provided below can be represented as [JSON file](Fog_json_example.json) or list of [environment variables](.env) (use `export $(cat .env | egrep -v "(^#.*|^$)" | xargs)` for export).

## Parameters

| **Environment variable** | JSON                                                         | Description                                                  |
| :----------------------- | ------------------------------------------------------------ | :----------------------------------------------------------- |
| `engine_BM_IP`           | `{"infrastructure_config":[{"name": "Ovirt",..."network": {"ip": "YourIP"}}]}` | Machine IP address for  oVirt deployment                     |
| `engine_BM_login`        | `{"infrastructure_config":[{"name": "Ovirt",..."credential": {"login": "YourLogin",...}}]}` | Machine login for  oVirt deployment                          |
| `engine_BM_password`     | `{"infrastructure_config":[{"name": "Ovirt",..."credential": {...,"password": "YourPasswd"}}]}` | Machine password for  oVirt deployment                       |
| `oVirt_Login`            | `{"cloud_provider":"credential": {"login": "YourLogin@internal",...},...}` | The login of the oVirt user. For example: *admin@internal*   |
| `oVirt_Password`         | `{"cloud_provider":"credential": {"password": "YourPasswd",...},...}` | The password of the oVirt user.                              |
| `oVirt_Templates`        | every `"operation_system": {   "name": "template_name" }` in `infrastructure_config` |  A list of names for templates, separated by spaces. There is template available by default `centos76`. |
| `terraform_IP`           | `{"infrastructure_config":[{"name": "Terraform",..."network": {"ip": "YourIP"}}]}` | Virtual machine IP address for  Terraform deployment. IP address has to be free and available in the network. |
| `terraform_login`        | `{"infrastructure_config":[{"name": "Terraform",..."credential": {"login": "YourLogin",...}}]}` | User login to be used during Terraform VM deployment.        |
| `terraform_password`     | `{"infrastructure_config":[{"name": "Terraform",..."credential": {...,"password": "YourPasswd"}}]}` | User password to be set for user specified by `terraform_login` parameter. |
| `terraform_name`         | `{"infrastructure_config":[{"name": "Terraform",...}]}`      | Name of the Terraform VM to manage.                          |
| `terraform_domain_name`  | `{"infrastructure_config":[{"name": "Terraform",..."network": {"dns_name": "terraform.dev.local"}}]}` | Hostname to be set to Terraform VM when deployed.            |
| `terraform_gateway`      | `{"infrastructure_config":[{"name": "Terraform",..."network": {"gateway": "10.0.0.1"}}]}` | Gateway to be set to network interface of Terraform VM.      |
| `terraform_netmask`      | `{"infrastructure_config":[{"name": "Terraform",..."network": {"netmask": "255.255.0.0"}}]}` | Netmask to be set to network interface of Terraform VM.      |
| `terraform_dns_search`   | `{"infrastructure_config":[{"name": "Terraform",..."network": {"dns_search": "dev.local"}}]}` | DNS search domains to be configured on Terraform VM.         |
| `terraform_dns_servers`  | `{"infrastructure_config":[{"name": "Terraform",..."network": {"dns_servers": "10.0.0.1"}}]}` | DNS servers to be configured on Terraform VM.                |
| `terraform_cpu`          | `{"infrastructure_config":[{"name": "Terraform",..."resource": {"cpu": "2"}}]}` | Number of virtual CPUs cores of the Terraform VM.            |
| `terraform_ram`          | `{"infrastructure_config":[{"name": "Terraform",..."resource": {"ram": "5120"}}]}` | Amount of memory of the Terraform VM in bytes.               |
| `terraform_os`           | `{"infrastructure_config":[{"name": "Terraform",..."operation_system": {"name": "centos 7.6"}}]}` | Name of the template, which should be used to create Terraform VM. One of the values in the `oVirt_Templates` list. |
