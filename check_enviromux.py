#!/usr/bin/env python

import sys, os
from optparse import OptionParser

verbosity = 0

def ParseOptions(default_levels):
    usage = "Usage: %prog host [options]"
    desc = "Reads sensor data from ENVIROMUX_MINI device through SNMP and \
gives back NAGIOS formatted check string. Optional Warning and Critical \
levels apply only to the queried sensor. If all sensors are queried \
simultaneously (-s all) global defaul values are used."

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
        choices = ["temperature1", "temperature2", "humidity1", "humidity2",
        "contact1", "contact2", "contact3", "contact4","water", "all"],
        help="Sensor to query. Possible values: temperature1 "
             "temperature2 humidity1 humidity2 contact1 contact2 "
             "contact3 contact4 water all [default: %default]")
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

    # Check for command line human errors
    if options.sensor == "all" and (options.warning or options.critical):
        parser.error("Critical and warning specific values can only be requested"
                     "for individually queried sensors. When querying all sensors"
                     "simultaneously defaults are used.")
    
    contact_sensors = ["contact1", "contact2", "contact3", "contact4","water"]
    continous_sensors = ["temperature1", "temperature2", "humidity1", "humidity2"]
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

    # Check for only one argument
    if len(args) == 0:
        parser.error("Please give enviromux-mini device ip or hostname.")
    elif len(args) > 1:
        parser.error("Please give only enviromux-mini device ip or hostname.")

    # Check and set warning final values
    sensor = options.sensor
    if not options.warning:
        if "temperature" in sensor:
            warning = default_levels[0]
        elif "humidity" in sensor:
            warning = default_levels[2]
        elif "contact" in sensor:
            warning = default_levels[5]
        elif "water" in sensor:
            warning = default_levels[4]
        else: # we never should get here
            parser.error("Something went wrong when checking default warning level."
                        "Please report bug.")
    else:
        warning = options.warning

    # Check and set critical final values
    if not options.critical:
        if "temperature" in sensor:
            critical = default_levels[1]
        elif "humidity" in sensor:
            critical = default_levels[3]
        elif "contact" in sensor:
            critical = default_levels[5]
        elif "water" in sensor:
            critical = default_levels[4]
        else: # we never should get here
            parser.error("Something went wrong when checking default critical level."
                        "Please report bug.")
    else:
        critical = options.critical

    return args[0], options.verbosity, options.community, options.sensor, \
            sensor_type, warning, critical


def vprint(level, *args):
    """Verbosity print.
    Decide according to the given verbosity level if the message will be
    printed to stdout.
    """
    if level <= verbosity:
        for arg in args:
            print arg,
        print

def verbosity_feedback():
    if verbosity == 1:
        vprint(1,"Verbosity Level 1")
    elif verbosity == 2:
        vprint(2,"Verbosity Level 2")
    elif verbosity == 3:
        vprint(3,"Verbosity Level 3 - Debug")


def main():
    global verbosity
    BASE_OID = ".1.3.6.1.4.1.3699.1.1.3."
    nagios_codes = dict(OK=0, WARNING=1, CRITICAL=2, UNKNOWN=3)

    #  default warning/critical levels: temp_w, temp_c, hum_w, hum_c, water, dry_contacts
    # BEWARE!! Due to limitations in optparse module these values are hard coded
    # into the optparse help strings. If you change some value here be sure to reflect
    # the change in the help string accordingly.
    levels = [30., 38., 70., 80., 1, 0]

    # return variables
    code = 0
    message = ""

    # get command line parameters
    host, verbosity, community, sensor, sensor_type, warning, critical = ParseOptions(levels)

    # Feedback about verbosity level if specified.
    verbosity_feedback()

    # Parameters check
    vprint (3, "Parameters:")
    vprint (3,  "host:", host,
            "\nverbosity: ",verbosity,
            "\ncommunity: ",community,
            "\nsensor: ",sensor,
            "\nwarning level", warning,
            "\ncritical level: ",critical)
    vprint (3, "Sensor type: ", sensor_type)

    # OID for all sensors [CurrentValue, Name], temperature also has units
    sensors = ["temperature1", "temperature2", "humidity1", "humidity2", \
               "contact1", "contact2", "contact3", "contact4","water"]
    temperature1 = ["1.1.1", "2.2.1", "2.2.2"]
    temperature2 = ["1.2.1", "2.3.1", "2.3.2"]
    humidity1    = ["1.3.1", "2.4.1"]
    humidity2    = ["1.4.1", "2.5.1"]
    contact1     = ["1.5.1", "2.6.1"]
    contact2     = ["1.6.1", "2.7.1"]
    contact3     = ["1.7.1", "2.8.1"]
    contact4     = ["1.8.1", "2.9.1"]
    water        = ["1.9.1", "2.10.1"]

    #get sensor name
    oid = BASE_OID + vars()[sensor][1]+".0"
    command =  "snmpget -v1 -c %s %s %s" %(community, host, oid)
    snmp_out = os.popen(command, "r").readline()
    sensor_name = snmp_out.strip().split('"')[-2]
    vprint (3, "sensor name snmp output: ", snmp_out)
    vprint (3, "sensor name in device: ", sensor_name)

    #get sensor value
    oid = BASE_OID + vars()[sensor][0]+".0"
    command =  "snmpget -v1 -c %s %s %s" %(community, host, oid)
    snmp_out = os.popen(command, "r").readline()
    value_str = snmp_out.strip().split()[-1]
    vprint (3, "sensor value snmp output: ", snmp_out)
    vprint (3, "sensor value:", value_str)

    # get/set units and other temperature specific sets
    if sensor == "temperature1":
        oid = BASE_OID + vars()[sensor][2]+".0"
        command =  "snmpget -v1 -c %s %s %s" %(community, host, oid)
        snmp_out = os.popen(command, "r").readline()
        unit_str = snmp_out.strip().split('"')[-2]
        vprint (3, "sensor units snmp output: ", snmp_out)
        vprint (3, "sensor units:", unit_str)

        # correct temperature value
        value_str = "%2.1f" %(float(value_str)/10.)
        vprint (3, "Corrected temperature sensor value:", value_str)

    # check thresohlds depending on the type of sensor
    if sensor_type == "continous":





    sys.exit(1)


if __name__ == "__main__":
    main()

