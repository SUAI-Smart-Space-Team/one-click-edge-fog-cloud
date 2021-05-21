# Find the clusters
data "ovirt_clusters" "cluster" {
  name_regex = var.cluster_name
  search = {
    max            = 1
  }
}

data "ovirt_templates" "template_filter" {
  search = {
    criteria       = var.vm_template_name
    max            = 1
    case_sensitive = false
  }
}

resource "ovirt_vm" "vm" {
  name                 = var.vm_name
#  clone                = "false"
#  high_availability    = "true"
  cluster_id           = data.ovirt_clusters.cluster.clusters[0].id
  template_id          = data.ovirt_templates.template_filter.templates[0].id
  memory               = var.vm_memory
  cores                = var.vm_cpu_cores
  sockets              = var.vm_cpu_sockets
  threads              = var.vm_cpu_threads

  initialization {
    authorized_ssh_key = var.vm_authorized_ssh_key
    host_name          = var.vm_hostname
    timezone           = var.vm_timezone
    user_name          = var.vm_user_name
    custom_script      = var.vm_custom_script
    dns_search         = var.vm_dns_search
    dns_servers        = var.vm_dns_servers

  }
}
