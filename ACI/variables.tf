variable "tenantName" {
  default = "terraformDemo"
}
variable "aciUser" {
  default = "ansible"
}
variable "aciPrivateKey" { 
  default = "ansible.key"
}
variable "aciCertName" {
  default = "ansible"
}
variable "aciUrl" {
  default = "https://10.0.99.11"
}

variable "bd_subnet" {
  type    = "string"
  default = "1.1.1.1/24"
}
variable "provider_profile_dn" {
  default = "uni/vmmp-VMware"
}
