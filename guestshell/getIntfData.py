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
# ./getIntfData.py -h
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
      "cmd": "show int mgmt0",
      "version": 1
    },
    "id": 1
  }
]

#Send payload to network element, and print response
response = requests.post(url,data=json.dumps(payload), headers=myheaders,auth=(user,passer)).json()

intf = response['result']['body']['TABLE_interface']['ROW_interface']

name = intf['interface']
pkts_in = intf['vdc_lvl_in_pkts']
bytes_in = intf['vdc_lvl_in_bytes']
pkts_out = intf['vdc_lvl_out_pkts']
bytes_out = intf['vdc_lvl_out_bytes']

outter = "\n interface:\t" + name + ",\n packets_in:\t" + str(pkts_in)
outter += ",\n bytes_in:\t" + str(bytes_in) + ",\n packets_out:\t"
outter += str(pkts_out) + ",\n bytes_out:\t" + str(bytes_out) + ""

print outter + "\n";
