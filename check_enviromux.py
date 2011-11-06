#!/usr/bin/env python

import sys, os
from optparse import OptionParser

BASE_OID = ".1.3.6.1.4.1.3699.1.1.3"

def ParseOptions():
    usage = "Usage: %prog host [options]"
    desc = """\
Read sensor data from ENVIROMUX_MINI device through SNMP and gives back NAGIOS
formatted check string. Warning and critical options apply to the queried sensor.
If all sensors are queried simultaneously defaul values are used."""
    parser = OptionParser(usage, description=desc, version="%prog version 0.0")
    parser.add_option("-C", "--community",
        type="str",
        default="public",
        help="SNMP community [default: %default]")
    parser.add_option("-s", "--sensor",
        type="choice",
        default="all",
        choices=["temp1","water","all"],
        help='Sensor to query. Possible values: temp1 water all  [default: %default]')
    parser.add_option("-w", "--warning",
        type="float",
        help="Warning levels for individually queried SENSOR "
             "[defaults: "
             "Temperature: 30, "
             "Humidity: 70%, "
             "Water: no warning level (use same as critical), "
             "dry contacts: no warning level (use same as critical)]")
    parser.add_option("-c", "--critical",
        type="float",
        help="Critical levels for individually queried SENSOR "
             "[defaults: "
             "Temperature: 38C, "
             "Humidity: 80%, "
             "Water: 1 (closed), "
             "dry contacts: 0 (open)]")

    (options, args) = parser.parse_args()
    
    contact_sensors = ["water"]
    
    if options.sensor == "all" and (options.warning or options.critical):
        parser.error("Critical and warning specific values can only be requested"
                     "for individually queried sensors. When querying all sensors"
                     "simultaneously defaults are used.")

    if options.sensor in contact_sensors:
        if options.warning and options.warning not in [0,1]:
            parser.error("For contact type sensors warning/critical should be"
                         "0 (open contact) or 1 (closed contact).")
        if options.critical and options.critical not in [0,1]:
            parser.error("For contact type sensors warning/critical should be"
                         "0 (open contact) or 1 (closed contact).")
        if options.warning != None  and \
           options.critical != None and \
           options.warning != options.critical:
            parser.error("For contact type sensors critical and warning options, "
                         "if both provided, should be equal.")

    if len(args) != 1:
        parser.error("Please give enviromux-mini device ip or hostname.")

    return args[0], options.community, options.sensor, options.warning, options.critical


def temp1(community, ip):
    # Get temperature value
    oid  = BASE_OID+"1.1.1.0"
    command = "snmpget -v1 -c %s %s %s" % (community, ip, oid)
    raw = os.popen(command, "r").readline()
    temp = "%2.1" %(float(temp.strip().split()[-1]/10.));

    # get temperature units
    oid = BASE_OID+"2.2.2.0"
    command = "snmpget -v1 -c %s %s %s" % (community, ip, oid)
    raw = os.popen(command, "r").readline()
    unit = temp.strip().split('"')[-2]


    pass


def vprint(level, message):
    """Verbosity print.

    Decide according to the given verbosity level if the message will be
    printed to stdout.
    """

    if level <= verbosity:
        print message


if __name__ == "__main__":
    #  default warning/critical levels: temp_w, temp_c, hum_w, hum_c, water, dry_contacts[1-4]
    # BEWARE!! Due to limitations in optparse module these vaules are hard coded
    # into optparse help strings. If you change some value here be sure to reflect
    # the new default value int the help there.
    levels = [30., 38., 70., 80., 1, 0, 0, 0, 0]
    ip, comm, sensor, warn, crit = ParseOptions()
    print "ip, comm, sensor, warn, crit"
    print ip, comm, sensor, warn, crit
    sys.exit(1)
    

