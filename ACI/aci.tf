provider "aci" {
  username = "${var.aciUser}"
  private_key = "${var.aciPrivateKey}"
  cert_name = "${var.aciCertName}"
  insecure = true
  url = "${var.aciUrl}"
}

resource "aci_tenant" "demo" {
  name = "${var.tenantName}"
  description = "created by terraform"
}

resource "aci_vrf" "vrf1" {
  tenant_dn = "${aci_tenant.demo.id}"
  name      = "vrf1"
}

resource "aci_bridge_domain" "bd1" {
  tenant_dn          = "${aci_tenant.demo.id}"
  relation_fv_rs_ctx = "${aci_vrf.vrf1.name}"
  name               = "bd1"
}

resource "aci_subnet" "bd1_subnet" {
  bridge_domain_dn = "${aci_bridge_domain.bd1.id}"
  ip               = "${var.bd_subnet}"
}

resource "aci_application_profile" "app1" {
  tenant_dn = "${aci_tenant.demo.id}"
  name      = "app1"
}

data "aci_vmm_domain" "vds" {
  provider_profile_dn = "${var.provider_profile_dn}"
  name                = "ACI"
}

resource "aci_application_epg" "epg1" {
  application_profile_dn = "${aci_application_profile.app1.id}"
  name                   = "epg1"
  relation_fv_rs_bd      = "${aci_bridge_domain.bd1.name}"
  relation_fv_rs_dom_att = ["${data.aci_vmm_domain.vds.id}"]
  relation_fv_rs_cons    = ["${aci_contract.contract_epg1_epg2.name}"]
  relation_fv_rs_prov    = ["${aci_contract.contract_admin.name}"]
}

resource "aci_application_epg" "epg2" {
  application_profile_dn = "${aci_application_profile.app1.id}"
  name                   = "epg2"
  relation_fv_rs_bd      = "${aci_bridge_domain.bd1.name}"
  relation_fv_rs_dom_att = ["${data.aci_vmm_domain.vds.id}"]
  relation_fv_rs_prov    = ["${aci_contract.contract_epg1_epg2.name}","${aci_contract.contract_admin.name}"]
}

#resource "aci_application_epg" "admin" {
#  application_profile_dn = "${aci_application_profile.app1.id}"
#  name                   = "admin"
#  relation_fv_rs_bd      = "${aci_bridge_domain.bd1.name}"
#  relation_fv_rs_dom_att = ["${data.aci_vmm_domain.vds.id}"]
#  relation_fv_rs_cons    = ["${aci_contract.contract_admin.name}"]
#}
#
#resource "aci_rest" "rest_pysdom" {
#  path       = "/api/node/mo/${aci_application_epg.admin.id}/rsdomAtt-[uni/phys-Fab2].json"
#  class_name = "fvRsDomAtt"
#  content = {
#                         "bindingType"= "none"
#                         "classPref"= "encap"
#                         "dn"= "uni/tn-terraformDemo/ap-app1/epg-admin/rsdomAtt-[uni/phys-Fab2]"
#                         "encapMode"= "auto"
#                         "epgCos"= "Cos0"
#                         "epgCosPref"= "disabled"
#                         "instrImedcy"= "lazy"
#                         "netflowDir"= "both"
#                         "netflowPref"= "disabled"
#                         "numPorts"= "0"
#                         "portAllocation"= "none"
#                         "resImedcy"= "immediate"
#                         "switchingMode"= "native"
#                         "tDn"= "uni/phys-Fab2"
#                         "untagged"= "no"
#              }
#}

#  path       = "/api/node/mo/${aci_application_epg.admin.id}/rspathAtt-[topology/pod-1/paths-204/pathep-[eth1/4]].json"
#  class_name = "fvRsPathAtt"
#  content = {
#          "dn"= "uni/tn-terraformDemo/ap-app1/epg-admin/rspathAtt-[topology/pod-1/paths-204/pathep-[eth1/4]]"
#          "encap"= "vlan-3992"
#          "instrImedcy"= "lazy"
#          "mode"= "regular"
#          "primaryEncap"= "unknown"
#          "tDn"= "topology/pod-1/paths-204/pathep-[eth1/4]"
#        }
#}
#
#resource "aci_contract" "contract_admin" {
#  tenant_dn = "${aci_tenant.demo.id}"
#  name      = "admin"
#}
#
#resource "aci_contract_subject" "admin_subject" {
#  contract_dn                  = "${aci_contract.contract_admin.id}"
#  name                         = "Subject"
#  relation_vz_rs_subj_filt_att = ["${aci_filter.allow_ssh.name}"]
#}

resource "aci_contract" "contract_epg1_epg2" {
  tenant_dn = "${aci_tenant.demo.id}"
  name      = "Web"
}

resource "aci_contract_subject" "Web_subject1" {
  contract_dn                  = "${aci_contract.contract_epg1_epg2.id}"
  name                         = "Subject"
  relation_vz_rs_subj_filt_att = ["${aci_filter.allow_https.name}","${aci_filter.allow_icmp.name}"]
}

resource "aci_filter" "allow_https" {
  tenant_dn = "${aci_tenant.demo.id}"
  name      = "allow_https"
}
resource "aci_filter" "allow_ssh" {
  tenant_dn = "${aci_tenant.demo.id}"
  name      = "allow_ssh"
}
resource "aci_filter" "allow_icmp" {
  tenant_dn = "${aci_tenant.demo.id}"
  name      = "allow_icmp"
}

resource "aci_filter_entry" "https" {
  name        = "https"
  filter_dn   = "${aci_filter.allow_https.id}"
  ether_t     = "ip"
  prot        = "tcp"
  d_from_port = "8080"
  d_to_port   = "8080"
  stateful    = "yes"
}

resource "aci_filter_entry" "ssh" {
  name        = "ssh"
  filter_dn   = "${aci_filter.allow_ssh.id}"
  ether_t     = "ip"
  prot        = "tcp"
  d_from_port = "22"
  d_to_port   = "22"
  stateful    = "yes"
}

resource "aci_filter_entry" "icmp" {
  name        = "icmp"
  filter_dn   = "${aci_filter.allow_icmp.id}"
  ether_t     = "ip"
  prot        = "icmp"
  stateful    = "yes"
}

