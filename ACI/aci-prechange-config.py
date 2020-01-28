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
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# log into an APIC and create a directory object
ls = cobra.mit.session.LoginSession('https://10.67.185.102', 'admin', '123Cisco123')
md = cobra.mit.access.MoDirectory(ls)
md.login()

# the top level object on which operations will be made
# Confirm the dn below is for your top dn
topDn = cobra.mit.naming.Dn.fromString('uni/tn-Camillo/BD-BD2')
topParentDn = topDn.getParent()
topMo = md.lookupByDn(topParentDn)

# build the request using cobra syntax
fvBD = cobra.model.fv.BD(topMo, multiDstPktAct=u'bd-flood', mcastAllow=u'no', ipv6McastAllow=u'no', limitIpLearnToSubnets=u'yes', unicastRoute=u'yes', unkMcastAct=u'flood', v6unkMcastAct=u'flood', descr=u'', hostBasedRouting=u'no', llAddr=u'::', nameAlias=u'', type=u'regular', ipLearning=u'yes', vmac=u'not-applicable', mac=u'00:22:BD:F8:19:FF', epMoveDetectMode=u'', ownerTag=u'', intersiteBumTrafficAllow=u'no', annotation=u'', ownerKey=u'', name=u'BD2', epClear=u'no', unkMacUcastAct=u'proxy', arpFlood=u'no', intersiteL2Stretch=u'no', OptimizeWanBandwidth=u'no')
fvSubnet = cobra.model.fv.Subnet(fvBD, name=u'', descr=u'', ctrl=u'', ip=u'2.0.0.1/8', preferred=u'no', virtual=u'no', nameAlias=u'', annotation=u'')
fvRsMldsn = cobra.model.fv.RsMldsn(fvBD, tnMldSnoopPolName=u'', annotation=u'')
fvRsIgmpsn = cobra.model.fv.RsIgmpsn(fvBD, tnIgmpSnoopPolName=u'', annotation=u'')
fvRsCtx = cobra.model.fv.RsCtx(fvBD, annotation=u'', tnFvCtxName=u'VRF1')
fvRsBdToEpRet = cobra.model.fv.RsBdToEpRet(fvBD, resolveAct=u'resolve', annotation=u'', tnFvEpRetPolName=u'')
fvRsBDToNdP = cobra.model.fv.RsBDToNdP(fvBD, annotation=u'', tnNdIfPolName=u'')


# commit the generated code to APIC
pprint(toXMLStr(topMo))
c = cobra.mit.request.ConfigRequest()
c.addMo(topMo)
md.commit(c)

