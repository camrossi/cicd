#!/usr/bin/env python

# list of packages that should be imported for this code to work
import cobra.mit.access
import cobra.mit.naming
import cobra.mit.request
import cobra.mit.session
import cobra.model.fv
import cobra.model.vns
import cobra.model.vz
from cobra.internal.codec.xmlcodec import toXMLStr

# log into an APIC and create a directory object
ls = cobra.mit.session.LoginSession('https://10.67.185.102', 'admin', '123Cisco123')
md = cobra.mit.access.MoDirectory(ls)
md.login()

# the top level object on which operations will be made
# Confirm the dn below is for your top dn
topDn = cobra.mit.naming.Dn.fromString('uni/tn-automationDemo')
topParentDn = topDn.getParent()
topMo = md.lookupByDn(topParentDn)

# build the request using cobra syntax
fvTenant = cobra.model.fv.Tenant(topMo, ownerKey=u'', name=u'automationDemo', descr=u'created by Amazing Automation', nameAlias=u'', ownerTag=u'', annotation=u'')
vzBrCP = cobra.model.vz.BrCP(fvTenant, ownerKey=u'', name=u'Web', descr=u'', targetDscp=u'unspecified', intent=u'install', nameAlias=u'', ownerTag=u'', prio=u'unspecified', annotation=u'')
vzSubj = cobra.model.vz.Subj(vzBrCP, revFltPorts=u'yes', descr=u'', prio=u'unspecified', targetDscp=u'unspecified', nameAlias=u'', consMatchT=u'AtleastOne', annotation=u'', provMatchT=u'AtleastOne', name=u'Subject')
vzRsSubjFiltAtt = cobra.model.vz.RsSubjFiltAtt(vzSubj, action=u'permit', priorityOverride=u'default', directives=u'', annotation=u'', tnVzFilterName=u'allow_icmp')
vzRsSubjFiltAtt2 = cobra.model.vz.RsSubjFiltAtt(vzSubj, action=u'permit', priorityOverride=u'default', directives=u'', annotation=u'', tnVzFilterName=u'allow_https')
vzBrCP2 = cobra.model.vz.BrCP(fvTenant, ownerKey=u'', name=u'admin', descr=u'', targetDscp=u'unspecified', intent=u'install', nameAlias=u'', ownerTag=u'', prio=u'unspecified', annotation=u'')
vzSubj2 = cobra.model.vz.Subj(vzBrCP2, revFltPorts=u'yes', descr=u'', prio=u'unspecified', targetDscp=u'unspecified', nameAlias=u'', consMatchT=u'AtleastOne', annotation=u'', provMatchT=u'AtleastOne', name=u'Subject')
vzRsSubjFiltAtt3 = cobra.model.vz.RsSubjFiltAtt(vzSubj2, action=u'permit', priorityOverride=u'default', directives=u'', annotation=u'', tnVzFilterName=u'allow_ssh')
vnsSvcCont = cobra.model.vns.SvcCont(fvTenant, annotation=u'')
fvCtx = cobra.model.fv.Ctx(fvTenant, ownerKey=u'', name=u'vrf1', descr=u'', nameAlias=u'', knwMcastAct=u'permit', pcEnfDir=u'ingress', ipDataPlaneLearning=u'enabled', ownerTag=u'', annotation=u'', pcEnfPref=u'enforced', bdEnforcedEnable=u'no')
fvRsVrfValidationPol = cobra.model.fv.RsVrfValidationPol(fvCtx, tnL3extVrfValidationPolName=u'', annotation=u'')
vzAny = cobra.model.vz.Any(fvCtx, matchT=u'AtleastOne', name=u'', descr=u'', prefGrMemb=u'disabled', nameAlias=u'', annotation=u'')
fvRsOspfCtxPol = cobra.model.fv.RsOspfCtxPol(fvCtx, annotation=u'', tnOspfCtxPolName=u'')
fvRsCtxToEpRet = cobra.model.fv.RsCtxToEpRet(fvCtx, annotation=u'', tnFvEpRetPolName=u'')
fvRsCtxToExtRouteTagPol = cobra.model.fv.RsCtxToExtRouteTagPol(fvCtx, annotation=u'', tnL3extRouteTagPolName=u'')
fvRsBgpCtxPol = cobra.model.fv.RsBgpCtxPol(fvCtx, tnBgpCtxPolName=u'', annotation=u'')
fvBD = cobra.model.fv.BD(fvTenant, multiDstPktAct=u'bd-flood', mcastAllow=u'no', ipv6McastAllow=u'no', limitIpLearnToSubnets=u'yes', unicastRoute=u'yes', unkMcastAct=u'flood', v6unkMcastAct=u'flood', descr=u'', hostBasedRouting=u'no', llAddr=u'::', nameAlias=u'', type=u'regular', ipLearning=u'yes', vmac=u'not-applicable', mac=u'00:22:BD:F8:19:FF', epMoveDetectMode=u'', ownerTag=u'', intersiteBumTrafficAllow=u'no', annotation=u'', ownerKey=u'', name=u'bd1', epClear=u'no', unkMacUcastAct=u'proxy', arpFlood=u'no', intersiteL2Stretch=u'no', OptimizeWanBandwidth=u'no')
fvSubnet = cobra.model.fv.Subnet(fvBD, name=u'', descr=u'', ctrl=u'nd', ip=u'1.1.1.1/24', preferred=u'no', virtual=u'no', nameAlias=u'', annotation=u'')
fvRsMldsn = cobra.model.fv.RsMldsn(fvBD, tnMldSnoopPolName=u'', annotation=u'')
fvRsIgmpsn = cobra.model.fv.RsIgmpsn(fvBD, tnIgmpSnoopPolName=u'', annotation=u'')
fvRsCtx = cobra.model.fv.RsCtx(fvBD, annotation=u'', tnFvCtxName=u'vrf1')
fvRsBdToEpRet = cobra.model.fv.RsBdToEpRet(fvBD, resolveAct=u'resolve', annotation=u'', tnFvEpRetPolName=u'')
fvRsBDToNdP = cobra.model.fv.RsBDToNdP(fvBD, annotation=u'', tnNdIfPolName=u'')
vzFilter = cobra.model.vz.Filter(fvTenant, ownerKey=u'', name=u'allow_https', descr=u'', nameAlias=u'', ownerTag=u'', annotation=u'')
vzEntry = cobra.model.vz.Entry(vzFilter, tcpRules=u'', arpOpc=u'unspecified', applyToFrag=u'no', dToPort=u'8080', descr=u'', nameAlias=u'', matchDscp=u'unspecified', prot=u'tcp', icmpv4T=u'unspecified', sFromPort=u'unspecified', stateful=u'yes', icmpv6T=u'unspecified', sToPort=u'unspecified', etherT=u'ip', dFromPort=u'8080', annotation=u'', name=u'https')
vzFilter2 = cobra.model.vz.Filter(fvTenant, ownerKey=u'', name=u'allow_icmp', descr=u'', nameAlias=u'', ownerTag=u'', annotation=u'')
vzEntry2 = cobra.model.vz.Entry(vzFilter2, tcpRules=u'', arpOpc=u'unspecified', applyToFrag=u'no', dToPort=u'unspecified', descr=u'', nameAlias=u'', matchDscp=u'unspecified', prot=u'icmp', icmpv4T=u'unspecified', sFromPort=u'unspecified', stateful=u'yes', icmpv6T=u'unspecified', sToPort=u'unspecified', etherT=u'ip', dFromPort=u'unspecified', annotation=u'', name=u'icmp')
vzFilter3 = cobra.model.vz.Filter(fvTenant, ownerKey=u'', name=u'allow_ssh', descr=u'', nameAlias=u'', ownerTag=u'', annotation=u'')
vzEntry3 = cobra.model.vz.Entry(vzFilter3, tcpRules=u'', arpOpc=u'unspecified', applyToFrag=u'no', dToPort=u'22', descr=u'', nameAlias=u'', matchDscp=u'unspecified', prot=u'tcp', icmpv4T=u'unspecified', sFromPort=u'unspecified', stateful=u'yes', icmpv6T=u'unspecified', sToPort=u'unspecified', etherT=u'ip', dFromPort=u'22', annotation=u'', name=u'ssh')
fvRsTenantMonPol = cobra.model.fv.RsTenantMonPol(fvTenant, annotation=u'', tnMonEPGPolName=u'')
fvAp = cobra.model.fv.Ap(fvTenant, ownerKey=u'', name=u'app1', descr=u'', nameAlias=u'', ownerTag=u'', prio=u'unspecified', annotation=u'')
fvAEPg = cobra.model.fv.AEPg(fvAp, shutdown=u'no', isAttrBasedEPg=u'no', matchT=u'AtleastOne', name=u'admin', descr=u'', fwdCtrl=u'', prefGrMemb=u'exclude', exceptionTag=u'', floodOnEncap=u'disabled', nameAlias=u'', hasMcastSource=u'no', prio=u'unspecified', annotation=u'', pcEnfPref=u'unenforced')
fvRsPathAtt = cobra.model.fv.RsPathAtt(fvAEPg, tDn=u'topology/pod-1/paths-204/pathep-[eth1/4]', descr=u'', primaryEncap=u'unknown', instrImedcy=u'lazy', mode=u'regular', encap=u'vlan-3992', annotation=u'')
fvRsDomAtt = cobra.model.fv.RsDomAtt(fvAEPg, epgCos=u'Cos0', classPref=u'encap', netflowPref=u'disabled', lagPolicyName=u'', tDn=u'uni/phys-Fab2', instrImedcy=u'lazy', encap=u'unknown', switchingMode=u'native', encapMode=u'auto', primaryEncapInner=u'unknown', numPorts=u'0', portAllocation=u'none', netflowDir=u'both', primaryEncap=u'unknown', annotation=u'', bindingType=u'none', secondaryEncapInner=u'unknown', delimiter=u'', epgCosPref=u'disabled', untagged=u'no', customEpgName=u'', resImedcy=u'immediate')
fvRsDomAtt2 = cobra.model.fv.RsDomAtt(fvAEPg, epgCos=u'Cos0', classPref=u'encap', netflowPref=u'disabled', lagPolicyName=u'', tDn=u'uni/vmmp-VMware/dom-ACI', instrImedcy=u'lazy', encap=u'unknown', switchingMode=u'native', encapMode=u'auto', primaryEncapInner=u'unknown', numPorts=u'0', portAllocation=u'none', netflowDir=u'both', primaryEncap=u'unknown', annotation=u'', bindingType=u'none', secondaryEncapInner=u'unknown', delimiter=u'', epgCosPref=u'disabled', untagged=u'no', customEpgName=u'', resImedcy=u'lazy')
fvRsCons = cobra.model.fv.RsCons(fvAEPg, tnVzBrCPName=u'admin', intent=u'install', annotation=u'', prio=u'unspecified')
fvRsCustQosPol = cobra.model.fv.RsCustQosPol(fvAEPg, annotation=u'', tnQosCustomPolName=u'')
fvRsBd = cobra.model.fv.RsBd(fvAEPg, annotation=u'', tnFvBDName=u'bd1')
fvAEPg2 = cobra.model.fv.AEPg(fvAp, shutdown=u'no', isAttrBasedEPg=u'no', matchT=u'AtleastOne', name=u'epg1', descr=u'', fwdCtrl=u'', prefGrMemb=u'exclude', exceptionTag=u'', floodOnEncap=u'disabled', nameAlias=u'', hasMcastSource=u'no', prio=u'unspecified', annotation=u'', pcEnfPref=u'unenforced')
fvRsProv = cobra.model.fv.RsProv(fvAEPg2, tnVzBrCPName=u'admin', matchT=u'AtleastOne', intent=u'install', annotation=u'', prio=u'unspecified')
fvRsDomAtt3 = cobra.model.fv.RsDomAtt(fvAEPg2, epgCos=u'Cos0', classPref=u'encap', netflowPref=u'disabled', lagPolicyName=u'', tDn=u'uni/vmmp-VMware/dom-ACI', instrImedcy=u'lazy', encap=u'unknown', switchingMode=u'native', encapMode=u'auto', primaryEncapInner=u'unknown', numPorts=u'0', portAllocation=u'none', netflowDir=u'both', primaryEncap=u'unknown', annotation=u'', bindingType=u'none', secondaryEncapInner=u'unknown', delimiter=u'', epgCosPref=u'disabled', untagged=u'no', customEpgName=u'', resImedcy=u'lazy')
fvRsCons2 = cobra.model.fv.RsCons(fvAEPg2, tnVzBrCPName=u'Web', intent=u'install', annotation=u'', prio=u'unspecified')
fvRsCustQosPol2 = cobra.model.fv.RsCustQosPol(fvAEPg2, annotation=u'', tnQosCustomPolName=u'')
fvRsBd2 = cobra.model.fv.RsBd(fvAEPg2, annotation=u'', tnFvBDName=u'bd1')
fvAEPg3 = cobra.model.fv.AEPg(fvAp, shutdown=u'no', isAttrBasedEPg=u'no', matchT=u'AtleastOne', name=u'epg2', descr=u'', fwdCtrl=u'', prefGrMemb=u'exclude', exceptionTag=u'', floodOnEncap=u'disabled', nameAlias=u'', hasMcastSource=u'no', prio=u'unspecified', annotation=u'', pcEnfPref=u'unenforced')
fvRsProv2 = cobra.model.fv.RsProv(fvAEPg3, tnVzBrCPName=u'Web', matchT=u'AtleastOne', intent=u'install', annotation=u'', prio=u'unspecified')
fvRsProv3 = cobra.model.fv.RsProv(fvAEPg3, tnVzBrCPName=u'admin', matchT=u'AtleastOne', intent=u'install', annotation=u'', prio=u'unspecified')
fvRsDomAtt4 = cobra.model.fv.RsDomAtt(fvAEPg3, epgCos=u'Cos0', classPref=u'encap', netflowPref=u'disabled', lagPolicyName=u'', tDn=u'uni/vmmp-VMware/dom-ACI', instrImedcy=u'lazy', encap=u'unknown', switchingMode=u'native', encapMode=u'auto', primaryEncapInner=u'unknown', numPorts=u'0', portAllocation=u'none', netflowDir=u'both', primaryEncap=u'unknown', annotation=u'', bindingType=u'none', secondaryEncapInner=u'unknown', delimiter=u'', epgCosPref=u'disabled', untagged=u'no', customEpgName=u'', resImedcy=u'lazy')
fvRsCustQosPol3 = cobra.model.fv.RsCustQosPol(fvAEPg3, annotation=u'', tnQosCustomPolName=u'')
fvRsBd3 = cobra.model.fv.RsBd(fvAEPg3, annotation=u'', tnFvBDName=u'bd1')


# commit the generated code to APIC
c = cobra.mit.request.ConfigRequest()
c.addMo(topMo)
md.commit(c)

