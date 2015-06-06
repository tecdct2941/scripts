#!/usr/bin/python
#
# Copyright (C) 2015 Cisco Systems Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0 
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# This script can be run with the help option to print command line help:
#
# ./getDeviceNameRaw.py -h
#
# If you do not enter command line options, it will interactively prompt
# for input. Password will be hidden in interactive input.
# Sample run without entering password on CLI:
#
# Note this script uses the requests library which can be brought in
# through the python package manager "pip".

import requests
import json
import sys
import logging
import getpass
from optparse import OptionParser

# Gather CLI and interactive input options
optp = OptionParser()
optp.add_option("-i", "--IP", dest="IP",
             help="IP address to connect to")
optp.add_option("-u", "--USER", dest="USER",
              help="Username")
optp.add_option("-p", "--PASS", dest="PASS",
              help="Password")
opts, args = optp.parse_args()

if opts.IP is None:
     url='http://' + raw_input("IP Address: ") + '/ins'
else:
     url='http://' + opts.IP + '/ins'

if opts.USER is None:
     user = raw_input("Username: ")
else:
     user = opts.USER

if opts.PASS is None:
     passer = getpass.getpass("Password: ")
else:
     passer = opts.PASS


# Setup JSON-RPC for show version
myheaders={'content-type':'application/json-rpc'}
payload=[
  {
    "jsonrpc": "2.0",
    "method": "cli",
    "params": {
      "cmd": "show hostname",
      "version": 1
    },
    "id": 1
  }
]

#Send payload to network element, and print response
response = requests.post(url,data=json.dumps(payload), headers=myheaders,auth=(user,passer)).json()
print json.dumps(response, indent=4, sort_keys=True)
