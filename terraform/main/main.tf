insecure true
provider "ovirt" {
  url = var.ovirt_url
  username  = var.ovirt_username
  password  = var.ovirt_password
}

# Create VM call temp02
module "vm_example" {
  source            = "../modules/vms"
  vm_name           = "vm_example"
  vm_hostname       = "vm_example.dev.local"
  vm_memory         = "2048"
  vm_cpu_cores      = "2"
  vm_timezone       = "Africa/Nairobi"
  vm_template_name  = "centos76"
  vm_nic_device     = "eth0"
  vm_nic_ip_address = "10.228.0.103"
  vm_dns_servers    = "10.228.0.1"
  vm_dns_search     = "dev.local"
  vm_nic_netmask    = "255.255.0.0"
}


## Create and attach Disk to VM temp02
module "vm_example_disk01" {
  source              = "../modules/disk"
  name                = "vm_example_disk01"
  size                = "10"
  storage_domain_name = "Local"
  vm_id               = "${module.vm_example.id}"
}

