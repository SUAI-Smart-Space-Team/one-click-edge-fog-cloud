
provider "ovirt" {
    url = var.ovirt_url
    username  = var.ovirt_username
    password  = var.ovirt_password
	insecure = true
}


module "masternode" { 
    source                 = "../modules/vms"
    vm_name                = "masternode"
	vm_nic_device          = "eth0" 
	vm_nic_ip_address      = "10.228.1.144" 
	vm_dns_servers         = "10.228.0.1" 
	vm_dns_search          = "dev.local" 
	vm_nic_netmask         = "255.255.0.0" 
	vm_nic_gateway         = "10.228.0.1" 
	vm_template_name       = "centos76"
	vm_memory              = "8192" 
	vm_hostname            = "masternodehost" 
	vm_cpu_cores           = "4" 
}

module "masternode_disk01" {
    source              = "../modules/disk"
    name                = "masternode_disk01"
    size                = "40"
    vm_id               = "${module.masternode.id}"
}

module "workernode1" { 
    source                 = "../modules/vms"
    vm_name                = "workernode1"
	vm_nic_device          = "eth0" 
	vm_nic_ip_address      = "10.228.1.145" 
	vm_dns_servers         = "10.228.0.1"
	vm_dns_search          = "dns"
	vm_nic_netmask         = "255.255.0.0" 
	vm_nic_gateway         = "10.228.0.1" 
	vm_template_name       = "centos76"
	vm_memory              = "8192" 
	vm_hostname            = "workernode1host" 
	vm_cpu_cores           = "4" 
}

module "workernode1_disk01" {
    source              = "../modules/disk"
    name                = "workernode1_disk01"
    size                = "40"
    vm_id               = "${module.workernode1.id}"
}

module "workernode2" { 
    source                 = "../modules/vms"
    vm_name                = "workernode2"
	vm_nic_device          = "eth0" 
	vm_nic_ip_address      = "10.228.1.146" 
	vm_dns_servers         = "10.228.0.1" 
	vm_dns_search          = "dns"
	vm_nic_netmask         = "255.255.0.0" 
	vm_nic_gateway         = "10.228.0.1" 
	vm_template_name       = "centos76"
	vm_memory              = "8192" 
	vm_hostname            = "workernode2host" 
	vm_cpu_cores           = "4" 
}

module "workernode2_disk01" {
    source              = "../modules/disk"
    name                = "workernode2_disk01"
    size                = "40"
    vm_id               = "${module.workernode2.id}"
}
