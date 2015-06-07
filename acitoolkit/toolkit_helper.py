from acitoolkit.acitoolkit import *
import requests
import sys
import json

def send_to_apic(tenant, URL, LOGIN, PASSWORD):
    # Login to APIC and push the config
    session = Session(URL, LOGIN, PASSWORD, False)
    session.login()
    resp = session.push_to_apic(tenant.get_url(), data=tenant.get_json())
    if resp.ok:
        print 'Success'

def mark_port_untagged(tenant, app, epg, port, URL, LOGIN, PASSWORD):
    pinfo = port.split("/")

    userJson = {'aaaUser': {'attributes': {'name': LOGIN, 'pwd': PASSWORD } } }
    sess = requests.Session()
    rsp = sess.post('{0}/api/mo/aaaLogin.json'.format(URL), data=json.dumps(userJson, sort_keys=True, indent=4, separators=(',', ': ')), verify=False)

    sb = '{0}/api/node/mo/uni/tn-' + tenant.__str__()
    sb = sb.format(URL)
    sb += '/ap-' + app.__str__() + '/'
    sb += 'epg-' + epg.__str__()
    sb += '/rspathAtt-[topology/pod-' + pinfo[0] +'/paths-' + pinfo[1]
    sb += '/pathep-[eth' + pinfo[2] + '/' + pinfo[3] + ']].json'
   

    Json2 = { "fvRsPathAtt": { "attributes": { "mode": "untagged", "tDn": "topology/pod-" + pinfo[0] + "/paths-" + pinfo[1] + "/pathep-[eth" + pinfo[2] +"/" + pinfo[3] + "]" }, "children": [] } }
    rsp = sess.post(sb, data=json.dumps(Json2, sort_keys=True, indent=4, separators=(',', ': ')), verify=False)
   

1;
