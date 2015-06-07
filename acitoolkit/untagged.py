#!/usr/bin/python

import requests
import sys
import json

user = 'admin'
password = '<password>'
apic = '<ip address>'

import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

userJson = {'aaaUser': {'attributes': {'name': user, 'pwd': password } } }

sess = requests.Session()

rsp = sess.post('https://{0}/api/mo/aaaLogin.json'.format(apic), data=json.dumps(userJson, sort_keys=True, indent=4, separators=(',', ': ')), verify=False)



Json2 = { "fvRsPathAtt": { "attributes": { "mode": "untagged", "tDn": "topology/pod-1/paths-101/pathep-[eth1/5]" }, "children": [] } }

rsp = sess.post('https://10.95.33.232/api/node/mo/uni/tn-Vegas/ap-ACI_Demo/epg-Fedora/rspathAtt-[topology/pod-1/paths-101/pathep-[eth1/5]].json'.format(apic), data=json.dumps(Json2, sort_keys=True, indent=4, separators=(',', ': ')), verify=False)
