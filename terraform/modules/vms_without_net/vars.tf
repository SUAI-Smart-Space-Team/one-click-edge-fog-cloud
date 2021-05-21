# Basic
variable "vm_name" {
  description = " A unique name for the VM"
  default     = ""
}
variable "cluster_name" {
  description = "The name of cluster the VM belongs to"
  default     = "Default"
}
variable "vm_template_name" {
  description = "The name of template the VM based on"
  default     = "centos"
}
variable "vm_memory" {
  description = "The amount of memory of the VM (in metabytes)"
  default     = "4096"
}
variable "vm_cpu_cores" {
  description = "The amount of cores"
  default     = "2"
}
variable "vm_cpu_sockets" {
  description = "The amount of sockets"
  default     = "1"
}
variable "vm_cpu_threads" {
  description = " The amount of threads"
  default     = "1"
}

# VM initialization

variable "vm_authorized_ssh_key" {
  description = "The ssh key for the VM"
  default     = ""
}
variable "vm_hostname" {
  description = "The hostname for the VM"
  default     = ""
}
variable "vm_timezone" {
  description = "The timezone for the VM"
  default     = ""
}
variable "vm_user_name" {
  description = "The user name for the VM"
  default     = ""
}
variable "vm_custom_script" {
  description = "Set the custom script for the VM"
  default     = ""
}
variable "vm_dns_search" {
  description = "The dns server for the VM"
  default     = ""
}
variable "vm_dns_servers" {
  description = "The dns server for the VM"
  default     = ""
}

# Initialization - Nic Configurations
variable "vm_nic_device" {
  description = "The vNIC to apply this configuration."
  default     = ""
}
variable "vm_nic_boot_proto" {
  description = "The boot protocol for the vNIC configuration."
  default     = "static"
}
variable "vm_nic_ip_address" {
  description = "The IP address for the vNIC"
  default     = ""
}
variable "vm_nic_gateway" {
  description = "The gateway for the vNIC"
  default     = ""
}
variable "vm_nic_netmask" {
  description = "The netmask for the vNIC"
  default     = ""
}
variable "vm_nic_on_boot" {
  description = "The flag to indicate whether the vNIC will be activated at VM booting"
  default     = "true"
}