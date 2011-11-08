#!/usr/bin/env python

import sys
import os
from optparse import OptionParser

verbosity = 0


def parseOptions(default_levels):
    usage = "Usage: %prog host [options]"
    desc = "Reads sensor data from ENVIROMUX_MINI device through SNMP and \
gives back NAGIOS formatted check string. Optional Warning and Critical \
levels apply only to the queried sensor. If all sensors are queried \
simultaneously (-s all) global defaul values are used."

    parser = OptionParser(usage, description=desc, version="%prog version 0.0")
    parser.add_option("-v", "--verbosity",
        type="int",
        default=0,
        metavar="LEVEL",
        help="set verbosity level to LEVEL; defaults to 0 (quiet), "
             "possible values go up to 3")
    parser.add_option("-C", "--community",
        type="str",
        default="public",
        help="SNMP community [default: %default]")
    parser.add_option("-s", "--sensor",
        type="choice",
        default="all",
        choices=["temperature1", "temperature2", "humidity1", "humidity2",
        "contact1", "contact2", "contact3", "contact4", "water", "all"],
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
             "Water: 1 (water detected), "
             "dry contacts: 0 (open contact)]")

    (options, args) = parser.parse_args()

    # Check for command line human errors
    if options.sensor == "all" and (options.warning or options.critical):
        parser.error("Critical and warning specific values can only be requested"
                     "for individually queried sensors. When querying all sensors"
                     "simultaneously, default values are used.")

    contact_sensors = ["contact1", "contact2", "contact3", "contact4", "water"]
    continous_sensors = ["temperature1", "temperature2", "humidity1", "humidity2"]
    if options.sensor in contact_sensors:
        sensor_type = "contact"
        if options.warning and options.warning not in [0, 1]:
            parser.error("For contact type sensors warning/critical should be"
                         "0 (open contact) or 1 (closed contact).")
        if options.critical and options.critical not in [0, 1]:
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
    if options.warning == None:
        if "temperature" in sensor:
            warning = default_levels[0]
        elif "humidity" in sensor:
            warning = default_levels[2]
        elif "contact" in sensor:
            warning = default_levels[5]
        elif "water" in sensor:
            warning = default_levels[4]
        else:  # leave None if sensor all
            warning = options.warning
    else:
        warning = options.warning

    # Check and set critical final values
    if options.critical == None:
        if "temperature" in sensor:
            critical = default_levels[1]
        elif "humidity" in sensor:
            critical = default_levels[3]
        elif "contact" in sensor:
            critical = default_levels[5]
        elif "water" in sensor:
            critical = default_levels[4]
        else:  # leave None if sensor all
            critical = options.critical
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
    """Give feedback about verbosity level being used."""
    if verbosity == 1:
        vprint(1, "Verbosity Level 1")
    elif verbosity == 2:
        vprint(2, "Verbosity Level 2")
    elif verbosity == 3:
        vprint(3, "Verbosity Level 3 - Debug")


def main():
    global verbosity
    base_oid = ".1.3.6.1.4.1.3699.1.1.3."
    nagios_codes = dict(OK=0, WARNING=1, CRITICAL=2, UNKNOWN=3)
    contact_status = ["open", "closed"]
    water_status = ["No water detected", "water detected"]

    #  default warning/critical levels: temp_w, temp_c, hum_w, hum_c, water, dry_contacts
    # BEWARE!! Due to limitations in optparse module these values are hard coded
    # into the optparse help strings. If you change some value here be sure to reflect
    # the change in the help string accordingly.
    levels = [30., 38., 70., 80., 1, 0]

    # return variables
    status = ""
    message = ""

    # get command line parameters
    host, verbosity, community, sensor, sensor_type, warning, critical = parseOptions(levels)

    # Feedback about verbosity level if specified.
    verbosity_feedback()

    # Parameters check
    vprint(3, "Parameters:")
    vprint(3,  "host:", host,
            "\nverbosity: ", verbosity,
            "\ncommunity: ", community,
            "\nsensor: ", sensor,
            "\nwarning level", warning,
            "\ncritical level: ", critical)
    vprint(3, "Sensor type: ", sensor_type)

    # OID for all sensors [CurrentValue, Name], temperature also has units
    temperature1 = ["1.1.1", "2.2.1", "2.2.2"]
    temperature2 = ["1.2.1", "2.3.1", "2.3.2"]
    humidity1    = ["1.3.1", "2.4.1"]
    humidity2    = ["1.4.1", "2.5.1"]
    contact1     = ["1.5.1", "2.6.1"]
    contact2     = ["1.6.1", "2.7.1"]
    contact3     = ["1.7.1", "2.8.1"]
    contact4     = ["1.8.1", "2.9.1"]
    water        = ["1.9.1", "2.10.1"]

    if sensor == "all":
        sensors = ["temperature1", "temperature2", "humidity1", "humidity2", \
               "contact1", "contact2", "contact3", "contact4", "water"]

    # TODO: loop over sensors (be one or all) and take care of global output
    # code.

    #get sensor name
    oid = base_oid + vars()[sensor][1] + ".0"
    command = "snmpget -v1 -c %s %s %s" % (community, host, oid)
    snmp_out = os.popen(command, "r").readline()
    sensor_name = snmp_out.strip().split('"')[-2]
    vprint(3, "sensor name snmp output: ", snmp_out)
    vprint(3, "sensor name in device: ", sensor_name)

    #get sensor value
    oid = base_oid + vars()[sensor][0] + ".0"
    command = "snmpget -v1 -c %s %s %s" % (community, host, oid)
    snmp_out = os.popen(command, "r").readline()
    value_str = snmp_out.strip().split()[-1]
    vprint(3, "sensor value snmp output: ", snmp_out)
    vprint(3, "sensor value:", value_str)

    # get/set units and other temperature specific sets
    if "temperature" in sensor:
        oid = base_oid + vars()[sensor][2] + ".0"
        command = "snmpget -v1 -c %s %s %s" % (community, host, oid)
        snmp_out = os.popen(command, "r").readline()
        unit = snmp_out.strip().split('"')[-2]
        vprint(3, "sensor units snmp output: ", snmp_out)
        vprint(3, "sensor units:", unit)
        # correct temperature value
        value_str = "%2.1f" % (float(value_str) / 10.)
        vprint(3, "Corrected temperature sensor value:", value_str)
    elif "humidity" in  sensor:
        unit = "%"
        # correct humidty value
        value_str = "%2.1f" % (float(value_str) / 10.)
        vprint(3, "Corrected humidty sensor value:", value_str)
    else:
        unit = ""

    # set performance data limits
    if "temperature" in sensor:
        sensor_min = "0."
        sensor_max = "40."
    elif "humedity" in sensor:
        sensor_min = "20."
        sensor_max = "80."
    else:
        sensor_min = "0"
        sensor_max = "1"

    # check thresohlds depending on the type of sensor
    if sensor_type == "continous":
        value = float(value_str)
        warn = float(warning)
        crit = float(critical)
        if value <= warn:
            status = "OK"
        elif warn < value < crit:
            status = "WARNING"
        elif value >= crit:
            status = "CRITICAL"
        else:
            status = "UNKNOWN"
        output = "%s - %s sensor reading is %s%s "\
            % (status, sensor_name, value_str, unit)
        perfdata = "| %s=%s%s;%s;%s;%s;%s" \
            % (sensor_name, value_str, unit, warning, critical, sensor_min, sensor_max)
    else:
        value = int(value_str)
        warn = int(warning)
        crit = int(critical)
        perfdata = ""
        if "water" in sensor:
            if value == crit:
                status = "CRITICAL"
                output = "%s - %s!" % (status, water_status[value].upper())
            else:
                status = "OK"
                output = "%s - %s" % (status, water_status[value])
        else:
            if value == crit:
                status = "CRITICAL"
                output = "CRITICAL - %s: contact is %s!" % (sensor_name,
                                  contact_status[value].upper())
            else:
                status = "OK"
                output = "OK - %s: contact is %s!" % (sensor_name,
                                  contact_status[value])

    message = output + perfdata

    vprint(3, "Output message:\n", message)
    vprint(3, "Return code: ", nagios_codes[status])

    print message
    sys.exit(nagios_codes[status])


if __name__ == "__main__":
    main()
