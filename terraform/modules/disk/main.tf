# Find the storagedomains id by name
data "ovirt_storagedomains" "storagedomain" {
  search = {
    #criteria       = "name = ${var.storage_domain_name}"
    criteria       = var.storage_domain_name
    # max             = 1
    case_sensitive  = false
  }
}

resource "ovirt_disk" "disk" {
  name              = var.name
  alias             = var.name
  size              = var.size
  format            = var.format
  storage_domain_id = data.ovirt_storagedomains.storagedomain.storagedomains[0].id
  sparse            = var.sparse
  shareable         = var.shareable
}

resource "ovirt_disk_attachment" "diskattachment" {
  vm_id                = var.vm_id
  disk_id              = ovirt_disk.disk.id
  active               = var.active
  bootable             = var.bootable
  interface            = var.interface
  read_only            = var.read_only
  use_scsi_reservation = var.use_scsi_reservation
}