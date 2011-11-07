#!/usr/bin/env python

import sys, os
from optparse import OptionParser
import logging
import StringIO

BASE_OID = ".1.3.6.1.4.1.3699.1.1.3"

_verbosity = 0

def ParseOptions():
    usage = "Usage: %prog host [options]"
    desc = """\
Reads sensor data from ENVIROMUX_MINI device through SNMP and gives back NAGIOS
formatted check string. Optional Warning and Critical levels apply only to the
queried sensor. If all sensors are queried simultaneously (-s all) global defaul
values are used."""
    parser = OptionParser(usage, description=desc, version="%prog version 0.0")
    parser.add_option("-v", "--verbosity",
        type="int",
        default=0,
        metavar = "LEVEL",
        help="set verbosity level to LEVEL; defaults to 0 (quiet), "
             "possible values go up to 3")
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
        help="Warning level for individually queried SENSOR "
             "[defaults: "
             "Temperature: 30, "
             "Humidity: 70%, "
             "Water: None (if neccesary, use same as critical), "
             "dry contacts: None (if neccesary, use same as critical)]")
    parser.add_option("-c", "--critical",
        type="float",
        help="Critical level for individually queried SENSOR "
             "[defaults: "
             "Temperature: 38C, "
             "Humidity: 80%, "
             "Water: 1 (closed), "
             "dry contacts: 0 (open)]")

    (options, args) = parser.parse_args()


    if options.sensor == "all" and (options.warning or options.critical):
        parser.error("Critical and warning specific values can only be requested"
                     "for individually queried sensors. When querying all sensors"
                     "simultaneously defaults are used.")

    contact_sensors = ["water"]
    continous_sensors = ["temp"]
    if options.sensor in contact_sensors:
        sensor_type = "contact"
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
    elif options.sensor in continous_sensors:
        sensor_type = "continous"
    elif options.sensor == "all":
        sensor_type = "all"
    else:
        parser.error("Something went wrong with the sensor type. Please report bug.")

    if len(args) == 0:
        parser.error("Please give enviromux-mini device ip or hostname.")
    elif len(args) > 1:
        parser.error("Please give only enviromux-mini device ip or hostname.")


    return args[0], options.verbosity, options.community, options.sensor, \
            sensor_type, options.warning, options.critical


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


def vprint(level, *args):
    """Verbosit y print.
    Decide according to the given verbosity level if the message will be
    printed to stdout.
    """
    if level <= verbosity:
        for arg in args:
            print arg,
        print


if __name__ == "__main__":
    #  default warning/critical levels: temp_w, temp_c, hum_w, hum_c, water, dry_contacts[1-4]
    # BEWARE!! Due to limitations in optparse module these values are hard coded
    # into the optparse help strings. If you change some value here be sure to reflect
    # the change in the help string accordingly.
    wc_levels = [30., 38., 70., 80., 1, 0, 0, 0, 0]
    ip, verbosity, comm, sensor, sensor_type, warn, crit = ParseOptions()

    # Feedback about verbosity level if specified.
    if verbosity == 1:
        vprint(1,"Verbosity Level 1")
    elif verbosity == 2:
        vprint(2,"Verbosity Level 2")
    elif verbosity == 3:
        vprint(3,"Verbosity Level 3 - Debug")
    
    # use a StringIO object to easily "print" to strings to pass them to vprint.
    vprint (3, "Parameters:")
    vprint (3,  "host:", ip, 
            "\nverbosity: ",verbosity,
            "\ncommunity: ",comm,
            "\nsensor: ",sensor,
            "\nwarning level", warn,
            "\ncritical level: ",crit)
    vprint (3, "Sensor type: ", sensor_type)

    # OID for all sensors

    sys.exit(1)

