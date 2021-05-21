# Disk resource variables
variable "name" {
  default = ""
}
variable "size" {
  default = ""
}
variable "format" {
 default = "cow"
}
variable "storage_domain_name" {
  default = "Local"
}
variable "sparse" {
 default = "true"
}
variable "shareable" {
  default = "false"
}

# Disk attachment
variable "vm_id" {
 default = ""
}
variable "disk_id" {
  default = ""
}
variable "active" {
  default = "true"
}
variable "bootable" {
  default = "false"
}
variable "interface" {
  default = "virtio_scsi"
}
variable "pass_discard" {
  default = ""
}
variable "read_only" {
  default =  "false"
}
variable "use_scsi_reservation" {
  default = "false"
}