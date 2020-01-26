
import cnae
import logging
import time
import argparse
import getpass
from pprint import pprint
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from time import sleep



# Enble logging at debug level
logger = logging.getLogger('cnae')
logger.setLevel(logging.INFO)

def get_args():
    parser = argparse.ArgumentParser(description="Prepare an NAE appliace for Demo Time!")
    parser.add_argument('-u', dest='user', help='Username, default: admin', default='admin')
    parser.add_argument('-d', dest='domain', help='Login Domain, defaul: Local',default='Local')
    parser.add_argument('-i', dest='nae_ip', help='IP address of the NAE Appliance',required=True)
    parser.add_argument('-p', dest='nae_password', help='IP address of the NAE Appliance',required=True)
    args = parser.parse_args()
    return args


requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
args= get_args()
#Create NAE Object
nae = cnae.NAE (args.nae_ip)

#Log in to NAE with user and password
nae.login(args.user, args.nae_password,args.domain)

PCV_Name = "Success"
config = '''
{
      "bd_change": {
        "action": "ADD",
        "dn": "uni/tn-Camillo/BD-BD2",
        "optimize_wan_bandwidth": "no",
        "type": "regular",
        "arp_flood": "no",
        "ip_learning": "yes",
        "limit_ip_learn_to_subnets": "yes",
        "unk_mac_ucast_act": "proxy",
        "unicast_route": "yes",
        "multi_dst_pkt_act": "bd-flood",
        "unk_mcast_act": "flood",
        "multi_cast_allow": "no",
        "vrf_name": "VRF1"
      }
    },
    {
      "network_subnet_change": {
        "action": "ADD",
        "dn": "uni/tn-Camillo/BD-BD2/subnet-2.0.0.1/8",
        "scope": "private",
        "make_this_primary_ip_address": "no",
        "treat_as_virtual_ip_address": "no",
        "subnet_control": "nd"
      }
    }
'''
nae.createPreChange("FAB2",PCV_name, config)

analysis_result = nae.getPreChangeResult("FAB2",PCV_name,False)

while "RUNNING" == analysis_result:
    sleep(10)
    analysis_result =  nae.getPreChangeResult("FAB2",PCV_name,False)


if analysis_result:
    #SUCCESS
    exit()
else:
    #FAIL
    exit(1) 


