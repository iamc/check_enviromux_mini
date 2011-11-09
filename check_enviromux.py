#!/usr/bin/env python

import sys
import os
from optparse import OptionParser

VERBOSITY = 0


def parse_options(default_levels):
    """ Get command line options and do some checks over them."""
    usage = "Usage: %prog host [options]"
    desc = ("Reads sensor data from ENVIROMUX_MINI device through SNMP and "
            "gives back NAGIOS formatted check string. Optional Warning and "
            "Critical levels apply only to the queried sensor. If all "
            "sensors are queried simultaneously (-s all) global defaul "
            "values are used.")

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

    check_options(options, args, parser)

    # Check and set warning final values
    if options.warning == None:
        warning = default_warning(options.sensor, default_levels)
    else:
        warning = options.warning

    # Check and set critical final values
    if options.critical == None:
        critical = default_critical(options.sensor, default_levels)
    else:
        critical = options.critical

    # check warning < critical
    if "temp" in options.sensor or "hum" in options.sensor:
        if warning >= critical:
            parser.error("Warning level should be < than critical level.")


    return args[0], options.verbosity, options.community, options.sensor, \
            warning, critical


def check_options(options, args, parser):
    """Check for  command line human errors and do some parsing."""

    # no options for all sensors
    if options.sensor == "all" and (options.warning != None or
                                    options.critical != None):
        parser.error("Critical and warning specific values can only be "
                     "requested for individually queried sensors. When "
                     "querying all sensors simultaneously, default values "
                     "are used.")

    # clasify sensor and check for contact sensors correct w/c options
    if "water" in options.sensor or "contact" in options.sensor:
        if options.warning != None and options.warning not in [0, 1]:
            parser.error("For contact type sensors warning/critical should be "
                         "0 (open contact) or 1 (closed contact).")
        if options.critical != None and options.critical not in [0, 1]:
            parser.error("For contact type sensors warning/critical should be "
                         "0 (open contact) or 1 (closed contact).")
        if options.warning != None  and \
           options.critical != None and \
           options.warning != options.critical:
            parser.error("For contact type sensors critical and warning "
                         "options, if both provided, should be equal.")

        # set both equal if one is set to avoid conflict with defaults later.
        if options.warning != None and options.critical == None:
            options.critical = options.warning
        if options.critical != None and options.warning == None:
            options.warning = options.critical

    # Check for only one argument
    if len(args) == 0:
        parser.error("Please give enviromux-mini device ip or hostname.")
    elif len(args) > 1:
        parser.error("Please give only enviromux-mini device ip or hostname.")


def default_warning(sensor, default_levels):
    """Get default warning value."""
    if sensor == "temperature1":
        warning = default_levels[0]
    elif sensor == "temperature2":
        warning = default_levels[2]
    elif sensor == "humidity1":
        warning = default_levels[4]
    elif sensor == "humidity2":
        warning = default_levels[6]
    elif sensor == "water":
        warning = default_levels[8]
    elif sensor == "contact1":
        warning = default_levels[9]
    elif sensor == "contact2":
        warning = default_levels[10]
    elif sensor == "contact3":
        warning = default_levels[11]
    elif sensor == "contact4":
        warning = default_levels[12]
    else:
        warning = None

    return warning


def default_critical(sensor, default_levels):
    """Ge t default critical value."""
    if sensor == "temperature1":
        critical = default_levels[1]
    elif sensor == "temperature2":
        critical = default_levels[3]
    elif sensor == "humidity1":
        critical = default_levels[5]
    elif sensor == "humidity2":
        critical = default_levels[7]
    elif sensor == "water":
        critical = default_levels[8]
    elif sensor == "contact1":
        critical = default_levels[9]
    elif sensor == "contact2":
        critical = default_levels[10]
    elif sensor == "contact3":
        critical = default_levels[11]
    elif sensor == "contact4":
        critical = default_levels[12]
    else:
        critical = None

    return critical


def vprint(level, *args):
    """Verbosity print.
    Decide according to the given verbosity level if the message will be
    printed to stdout.
    """
    if level <= VERBOSITY:
        for arg in args:
            print arg,
        print


def verbosity_feedback():
    """Give feedback about verbosity level being used."""
    if VERBOSITY == 1:
        vprint(1, "Verbosity Level 1")
    elif VERBOSITY == 2:
        vprint(2, "Verbosity Level 2")
    elif VERBOSITY == 3:
        vprint(3, "Verbosity Level 3 - Debug")


def read_sensor(host, community, sensor):
    """ Retrieve sensor data from enviromux-mini device.  """
    base_oid = ".1.3.6.1.4.1.3699.1.1.3."
    # OID for all sensors [CurrentValue, Name , Units(if available)]
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

    return sensor_name, value_str, unit


def generate_output(sensor, sensor_name, value_str, unit,
                    warning, critical):
    """Generate nagios ouput from sensor data and limits."""
    # return variables
    status = ""
    output = ""
    perfdata = ""

    # define status for contact sersors.
    contact_status = ["open", "closed"]
    water_status = ["No water detected", "water detected"]

    # set performance data limits
    if "temperature" in sensor:
        sensor_min = "0."
        sensor_max = "45."
    elif "humidity" in sensor:
        sensor_min = "20."
        sensor_max = "85."
    else:
        sensor_min = "0"
        sensor_max = "1"

    # check thresholds depending on the type of sensor
    if "temp" in sensor or "hum" in sensor:
        value = float(value_str)
        warn = float(warning)
        crit = float(critical)
        if value <  15.:
            # harcoded lower value. We should never get here neither in
            # temperature nor in humidity. If we do we get at least an
            # unknown status.
            status = "UNKNOWN"
        elif value <= warn:
            status = "OK"
        elif warn < value < crit:
            status = "WARNING"
        elif value > 1000.:
            status = "UNKNOWN"
        elif value >= crit:
            status = "CRITICAL"
        else:
            status = "UNKNOWN"
        output = "%s - %s sensor reading is %s %s"\
            % (status, sensor_name, value_str, unit)
        if "temperature" in sensor:
            unit = ""  # do not add Celsius to perfdata
        perfdata = ("|%s=%s%s;%s;%s;%s;%s" %
                    (sensor_name.replace(" ", "_"), value_str, unit, warning,
                     critical, sensor_min, sensor_max))
    else:
        value = int(value_str)
        warn = int(warning)
        crit = int(critical)
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
                output = "OK - %s: contact is %s" % (sensor_name,
                                  contact_status[value])
        perfdata = ""

    return status, output, perfdata


def main():
    """Main check code.

    We define some general variables here as default warning/critical
    levels.

    """
    global VERBOSITY
    nagios_codes = dict(OK=0, WARNING=1, CRITICAL=2, UNKNOWN=3)

    #  default warning/critical levels: [temp1_w, temp1_c, temp2_w, temp2_c,
    # hum1_w, hum1_c, hum2_w, hum2_c, water, contact1-4]
    #
    # BEWARE!! Due to limitations in optparse module these values are hard
    # coded into the optparse help strings. If you change some value here be
    # sure to reflect the change in the help string accordingly.
    levels = [30., 38., 30., 38., 70., 80., 70., 80., 1, 1, 1, 1, 1]

    # get command line parameters
    host, VERBOSITY, community, sensor, warning, critical = \
        parse_options(levels)

    # Feedback about verbosity level if specified
    verbosity_feedback()

    # Parameters check
    vprint(3, "Parameters:")
    vprint(3,  "host:", host,
            "\nverbosity: ", VERBOSITY,
            "\ncommunity: ", community,
            "\nsensor: ", sensor,
            "\nwarning level", warning,
            "\ncritical level: ", critical)

    if sensor == "all":
        all_sensors = True
        sensors = ["temperature1", "temperature2", "humidity1", "humidity2", \
               "contact1", "contact2", "contact3", "contact4", "water"]
    else:
        all_sensors = False
        sensors = [sensor]

    # TODO: loop over sensors (be one or all) and take care of global output
    # code.

    for sensor in sensors:
        vprint(3, "-----------------------------")
        vprint(3, "Sensor to check: ", sensor)

        # read sensor data and other values
        sensor_name, value_str, unit = read_sensor(host, community, sensor)

        # if looking at all sensors, set default w/c levels
        if all_sensors == True:
            warning = default_warning(sensor, levels)
            critical = default_critical(sensor, levels)

        status, output, perfdata = generate_output(sensor, sensor_name,
                            value_str, unit, warning, critical)

        message = output + perfdata

        vprint(3, "Output message:\n", message)
        vprint(3, "Return code: ", nagios_codes[status])

        print message

    sys.exit(nagios_codes[status])


if __name__ == "__main__":
    main()
