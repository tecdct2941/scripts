#!/env/bin/python
 

import sys
import os
import re

from cisco import cli
hostlistfile = "/bootflash/scripts/hostlist.txt"

 

try:
    sys.argv[1]
except IndexError:
    print "Error: Missing argument, need either 'up' or 'down'"
    exit()

if sys.argv[1] == "up":

   # At this point we should have a file containing ports to bring up.
   if os.path.isfile(hostlistfile) == False:
       print "No hostlist found, exiting"
       exit()

   file = open(hostlistfile, "r")
   line = file.readline()

   while line != "":
       stripped = line.rstrip('\n')
       cli("config terminal ; interface %s ; no shutdown" % stripped)
       print "Bringing up interface %s" % stripped
       line = file.readline()

   #We are now done with the hostlist file, lets delete.
   os.remove(hostlistfile)

 

if sys.argv[1] == "down":

    # Uplinks are not yet up, lets see which hosts are active, bring those

    # down and save to a file.


    f = open(hostlistfile, "w")
    print "Generating host list dynamically."
    result = cli("show interface brief | i Eth")
    #print "CLI : %s" % result
    for rline in result.split('\n'):
        #print "rline : %s" % rline
        match = re.match(r'^(Eth[\S]+).*', rline)
        #print "match %s" % match

        if match:
            #Check name against Ethenert2/ we will skip these uplinks.
            match2 = re.match(r'Eth2/.*', match.group(1))
            if match2:
                #print  "contin %s" % match2
                continue

            match3 = re.match(r'Eth1/.*', match.group(1))
            #print "match3 : %s" % match3

            if match3:

                match4 = re.match(r'.*(Administratively down|SFP not inserted).*', rline)
                #print "match4 : %s" % match4
                if match4 == None:

                    f.write(match.group(1))
                    print "Adding : %s to host list" % match.group(1)
                    f.write('\n')
                    cli("config t ; interface %s ; shutdown" % match.group(1))


    f.close()