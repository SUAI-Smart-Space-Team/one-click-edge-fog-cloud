# Find the disk id by name
data "ovirt_disks" "filtered_disks" {
  search = {
    criteria       = var.disk_name
    # max            = 2
    case_sensitive = false
  }
}

resource "ovirt_disk_attachment" "diskattachment" {
  vm_id                = var.vm_id
  disk_id              = data.ovirt_disks.filtered_disks.disks[0].id
  active               = var.active
  bootable             = var.bootable
  interface            = var.interface
  read_only            = var.read_only
  use_scsi_reservation = var.use_scsi_reservation
}