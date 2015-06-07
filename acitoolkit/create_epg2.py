#!/usr/bin/python

# Copyright (c) 2014 Cisco Systems
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#
from acitoolkit.acitoolkit import *
#from credentials import *

import requests
import sys
import json
import getpass

import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

URL = 'https://<ip address>'
LOGIN = 'admin' 
PASSWORD = getpass.getpass('Password:')

def send_to_apic(tenant):
    # Login to APIC and push the config
    session = Session(URL, LOGIN, PASSWORD, False)
    session.login()
    resp = session.push_to_apic(tenant.get_url(), data=tenant.get_json())
    if resp.ok:
        print 'Success'

# Basic Connectivity Example
# Equivalent to connecting to ports to the same VLAN

# Create a tenant
tenant = Tenant('tnDemo')

# Create a Context and a BridgeDomain
context = Context('vrfDemo', tenant)
context.set_allow_all(False)
bd = BridgeDomain('bdDemo', tenant)
bd.add_context(context)
gateway = Subnet('gateway',bd)
gateway.set_addr('10.30.10.1/24')
bd.add_subnet(gateway)


# Create an App Profile and an EPG
app = AppProfile('anpDemo', tenant)
epg = EPG('epgDB', app)

# Attach the EPG to interfaces using VLAN 60 as the encap
if1 = Interface('eth','1','102','1','2')
l2if = L2Interface('vlan_on_eth/1/102/1/2', 'vlan', '31')
l2if.attach(if1)


epg.attach(l2if)
epg.add_bd(bd)



# Dump the necessary configuration
print 'URL:', tenant.get_url()
print 'JSON:', tenant.get_json()

send_to_apic(tenant)

# Clean up
#tenant.mark_as_deleted()
#send_to_apic(tenant)

# Now lets make the ports untagged:
#login 
userJson = {'aaaUser': {'attributes': {'name': LOGIN, 'pwd': PASSWORD } } }
sess = requests.Session()
rsp = sess.post('{0}/api/mo/aaaLogin.json'.format(URL), data=json.dumps(userJson, sort_keys=True, indent=4, separators=(',', ': ')), verify=False)


Json2 = { "fvRsPathAtt": { "attributes": { "mode": "untagged", "tDn": "topology/pod-1/paths-102/pathep-[eth1/2]" }, "children": [] } }
rsp = sess.post('{0}/api/node/mo/uni/tn-tnDemo/ap-anpDemo/epg-epgDB/rspathAtt-[topology/pod-1/paths-102/pathep-[eth1/2]].json'.format(URL), data=json.dumps(Json2, sort_keys=True, indent=4, separators=(',', ': ')), verify=False)
