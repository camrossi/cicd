variable "vsphere_user" {
  default = "administrator@aws.local"
}
variable "vsphere_password" {
  default = "C15co123!"
}
variable "vsphere_server" {
  default = "10.0.99.22"
}
variable "ssh_user" {
  default = "cisco"
}
variable "ssh_password" {
  default = "cisco"
}
variable "dnsServers" {
  type = "list"
  default = ["10.0.50.21"]
}

variable "vmPrefix" {
  default = "terraform"
}