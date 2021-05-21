# Disk attachment
variable "disk_name" {
 default = ""
}
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