# Fog Deployment based  on oVirt 4.3  

Fog is a tool that makes it easy to deploy multiple collaborative infrastructure products,
you don't need any special knowledge and deep understanding components.
You can pass parameters to the input and get a ready-made infrastructure deployed 
on your server and ready for work. Fog uses an infrastructure-as-code approach, 
so you can use the source files, extend them, and reuse them as you see fit. It's easy to develop, maintain, and share.
### This release supports the deployment of the following components
- [x] [oVirt](https://www.ovirt.org)
- [x] [Terraform](https://www.terraform.io)
- [ ] [Kubernetes](https://kubernetes.io)
- [ ] [Docker](https://www.docker.com)
- [ ] [Kafka](https://kafka.apache.org)
- [ ] [Pravega](https://pravega.io)

## Requirements

- oVirt Python SDK version 4.3
- Ansible version 2.9
- Ansible [Runner](https://ansible-runner.readthedocs.io/en/stable/intro.html) for Python
- oVirt Ansible [Collection](https://galaxy.ansible.com/ovirt/ovirt) 
- GO Ansible [Roles](https://github.com/fubarhouse/ansible-role-golang)
- CentOS 7
- [Hardware Requirements](https://www.ovirt.org/documentation/installing_ovirt_as_a_standalone_manager_with_local_databases/#hardware-requirements_SM_localDB_deploy)

## Usage

#### Choose module

```
usage: main.py [-h] [-v] (-j JSON | -e) {ovirt,terraform,infra} ...

Manage Fog infrastructure.

positional arguments:
  {ovirt,terraform,infra}
                        Choose module
    ovirt               ovirt module
    terraform           terraform module
    infra               infra module include all above

optional arguments:
  -j JSON, --json JSON  The path to the json configuration file
  -e, --env             Choose environment variables for input of configuration

```

#### Choose action for oVirt module

```
usage: main.py ovirt [-h] (--setup | --cleanup | --template)

optional arguments:
  -h, --help  show this help message and exit
  --setup     Setup oVirt
  --cleanup   Cleanup oVirt
  --template  Add templates to oVirt listed in the input configuration
```

#### Choose action for Terraform module

```
usage: main.py terraform [-h] (--setup | --cleanup | --create_vm)

optional arguments:
  -h, --help   show this help message and exit
  --setup      Setup Terraform
  --cleanup    Cleanup Terraform
  --create_vm  Create VMs listed in the input configuration
```

#### Choose action for infrastructure module

````
usage: main.py infra [-h] (--setup | --cleanup)

optional arguments:
  -h, --help  show this help message and exit
  --setup     Setup whole infrastructure
  --cleanup   Cleanup whole infrastructure
````

**Example:**

Setup module oVirt with input parameters from environment variables

```
python main.py -e ovirt --setup
```

## Configuration 

Each module required set of input parameters. All parameters described in [docs](https://github.com/SUAI-Smart-Space-Team/one-click-edge-fog-cloud/blob/main/docs/Fog%20input%20parameters%20description.md). The required parameters for the modules are listed below.

#### **oVirt**

| Action   | Required parameters                                          |
| -------- | ------------------------------------------------------------ |
| setup    | `engine_BM_IP`, `engine_BM_login`,`engine_BM_password`,`oVirt_domain_name`, `oVirt_Login`, `oVirt_Password` |
| cleanup  | `engine_BM_IP`, `engine_BM_login`,`engine_BM_password`,`oVirt_domain_name`, `oVirt_Login`, `oVirt_Password` |
| template | `engine_BM_IP`, `engine_BM_login`,`engine_BM_password`,`oVirt_domain_name`, `oVirt_Login`, `oVirt_Password` `oVirt_Templates` |

#### **Terraform**

| Action    | Required parameters                                          |
| --------- | ------------------------------------------------------------ |
| setup     | `engine_BM_IP`, `engine_BM_login`,`engine_BM_password`,`oVirt_domain_name`, `oVirt_Login`, `oVirt_Password` `terraform_IP terraform_login` `terraform_password` `terraform_name` `terraform_domain_name` `terraform_gateway`  `terraform_netmask`  `terraform_dns_search` `terraform_dns_servers` `terraform_cpu` `terraform_ram`  `terraform_os` |
| cleanup   | `engine_BM_IP`, `engine_BM_login`,`engine_BM_password`,`oVirt_domain_name`, `oVirt_Login`, `oVirt_Password` `terraform_IP terraform_login` `terraform_password` `terraform_name` |
| create_vm | `engine_BM_IP`, `engine_BM_login`,`engine_BM_password`,`oVirt_domain_name`, `oVirt_Login`, `oVirt_Password` `terraform_IP terraform_login` `terraform_password` `terraform_name` |

