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
import requests
import sys
import json
import getpass

#import requests.packages.urllib3
#requests.packages.urllib3.disable_warnings()

URL = 'https://<ip address>'
LOGIN = 'admin'
PASSWORD = getpass.getpass('Password:')

#login
userJson = {'aaaUser': {'attributes': {'name': LOGIN, 'pwd': PASSWORD } } }
sess = requests.Session()
rsp = sess.post('{0}/api/mo/aaaLogin.json'.format(URL), data=json.dumps(userJson, sort_keys=True, indent=4, separators=(',', ': ')), verify=False)


#Delete tenant tnDemo
Json2 = { "polUni": { "attributes": { "dn": "uni", "status": "modified"}, "children":[ {"fvTenant":{"attributes":{"dn":"uni/tn-tnDemo","status":"deleted"},"children":[]}}]}}

rsp = sess.post('{0}/api/node/mo/uni.json'.format(URL), data=json.dumps(Json2, sort_keys=True, indent=4, separators=(',', ': ')), verify=False)
