variable "tenantName" {
  default = "terraformDemo"
}
variable "aciUser" {
  default = "automation"
}
variable "aciPrivateKey" { 
  default = "ansible.key"
}
variable "aciCertName" {
  default = "ansible.crt"
}
variable "aciUrl" {
  default = "https://fab1-apic1.cam.ciscolabs.com"
}

variable "bd_subnet" {
  type    = "string"
  default = "1.1.1.1/24"
}
variable "provider_profile_dn" {
  default = "uni/vmmp-VMware"
}
