#!/usr/bin/env python

import os
from optparse import OptionParser

BASE_OID = ".1.3.6.1.4.1.3699.1.1.3"

def ParseOptions():
    usage = "Usage: %prog [options] input_file"
    parser = OptionParser(usage)
    parser.set_defaults(kmin=1)
    parser.add_option("-k", type="int",
            help ="K number to compute [default: %default]")

    (options, args) = parser.parse_args()

    if len(args) != 1:
        parser.error("Please give data filename.")
    elif os.path.isfile(args[0]) is False:
        parser.error("File <%s> does not exist."%args[0])

    k = options.k

    input_fn = args[0]
    input_f = open(input_fn)
    input_d = input_f.readlines()
    kmax_f = int(float(input_d[3].split()[0]))
    if k > kmax_f:
        sys.exit("k indicated is bigger than in input_file. Check it!")

    return input_fn, k

def temp1(community, ip):
    # Get temperature value
    oid  = BASE_OID+"1.1.1.0"
    command = "snmpget -v1 -c %s %s %s" % (community, ip, oid)
    raw = os.popen(command, "r").readline()
    temp = "%2.1" %(float(temp.strip().split()[-1]/10.)

    # get temperature units
    oid = BASE_OID+"2.2.2.0"
    command = "snmpget -v1 -c %s %s %s" % (community, ip, oid)
    raw = os.popen(command, "r").readline()
    unit = temp.strip().split('"')[-2]



if __name__ == "__main__":
    input_fn, k = ParseOptions()
    kub_h0(input_fn, k)
~

