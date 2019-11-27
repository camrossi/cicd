provider "vsphere" {
  user           = "${var.vsphere_user}"
  password       = "${var.vsphere_password}"
  vsphere_server = "${var.vsphere_server}"

  # If you have a self-signed cert
  allow_unverified_ssl = true
}

data "vsphere_datacenter" "dc" {
  name = "STLD"
}

data "vsphere_datastore" "datastore" {
  name          = "BM01"
  datacenter_id = "${data.vsphere_datacenter.dc.id}"
}

data "vsphere_distributed_virtual_switch" "dvs" {
  name          = "ACI"
  datacenter_id = "${data.vsphere_datacenter.dc.id}"
}

data "vsphere_network" "pg1" {
  name          = "terraformDemo|app1|epg1"
  datacenter_id = "${data.vsphere_datacenter.dc.id}"
}

data "vsphere_network" "pg2" {
  name          = "terraformDemo|app1|epg2"
  datacenter_id = "${data.vsphere_datacenter.dc.id}"
}

data "vsphere_compute_cluster" "cluster" {
  name          = "Cluster"
  datacenter_id = "${data.vsphere_datacenter.dc.id}"
}

data "vsphere_virtual_machine" "template" {
  name          = "Ubuntu-18-04"
  datacenter_id = "${data.vsphere_datacenter.dc.id}"
}


locals {
  pgmap = {
    "vm1" = "${data.vsphere_network.pg1.id}"
    "vm2" = "${data.vsphere_network.pg2.id}"
  }
  ipmap = {
    "vm1" = "1.1.1.100"
    "vm2" = "1.1.1.200"
  }
  gateway = "1.1.1.1"
  domain = "cam.ciscolabs.com"
  prefixlen = "24"
}


resource "vsphere_virtual_machine" "vm" {
  count = 2
  name             = "${var.vmPrefix}${count.index + 1}"
  resource_pool_id = "${data.vsphere_compute_cluster.cluster.resource_pool_id}"
  datastore_id     = "${data.vsphere_datastore.datastore.id}"

  num_cpus = 2
  memory   = 1024
  guest_id = "${data.vsphere_virtual_machine.template.guest_id}"

  scsi_type = "${data.vsphere_virtual_machine.template.scsi_type}"

  network_interface {
    network_id   = "${local.pgmap["vm${count.index + 1}"]}"
    adapter_type = "${data.vsphere_virtual_machine.template.network_interface_types[0]}"
  }

  disk {
    label            = "disk0"
    size             = "${data.vsphere_virtual_machine.template.disks.0.size}"
    eagerly_scrub    = "${data.vsphere_virtual_machine.template.disks.0.eagerly_scrub}"
    thin_provisioned = "${data.vsphere_virtual_machine.template.disks.0.thin_provisioned}"
  }

  provisioner "file" {
     source      = "app.py"
     destination = "/home/cisco/app.py"
     connection {
        type          = "ssh"
        user          = "cisco"
        password      = "123Cisco123"
     }
   }
   provisioner "file" {
     source      = "acilogo.jpg"
     destination = "/home/cisco/acilogo.jpg"
     connection {
        type          = "ssh"
        user          = "cisco"
        password      = "123Cisco123"
     }
   }
   
   provisioner "remote-exec" {
     inline = [
       "mkdir /home/cisco/static",
       "mv /home/cisco/acilogo.jpg /home/cisco/static/",
       "echo 'python /home/cisco/app.py 2>&1 &' > /home/cisco/start_app.sh",
       "chmod u+x /home/cisco/start_app.sh",
       "sleep 5"
     ]
     connection {
        type          = "ssh"
        user          = "cisco"
        password      = "123Cisco123"
     }
  } 

  clone {
    template_uuid = "${data.vsphere_virtual_machine.template.id}"

    customize {
      timeout = 5
      linux_options {
        host_name = "${var.vmPrefix}${count.index + 1}"
        domain    = "${local.domain}"
      }

      network_interface {
        ipv4_address = "${local.ipmap["vm${count.index + 1}"]}"
        ipv4_netmask = "${local.prefixlen}"
      }

      ipv4_gateway = "${local.gateway}"
      dns_server_list = "${var.dnsServers}"
    }
  }
}

