variable "vsphere_user" {
  default = "administrator@vsphere.local"
}
variable "vsphere_password" {
  default = "123Cisco123!"
}
variable "vsphere_server" {
  default = "vc2.cam.ciscolabs.com"
}
variable "ssh_user" {
  default = "cisco"
}
variable "ssh_password" {
  default = "123Cisco123"
}
variable "dnsServers" {
  type = "list"
  default = ["192.168.66.1"]
}

variable "vmPrefix" {
  default = "terraform"
}
