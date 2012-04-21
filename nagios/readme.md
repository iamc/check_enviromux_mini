check_enviromux_mini - Enviromux-mini nagios plugin
===================================================

Nagios check for ENVIROMUX MINI server room environment monitoring system.

Contact
  ~ [inigo\_aldazabal@ehu.es][]

NAGIOS check for [enviromux-mini][] sensor using SNMP.


Files description
-----------------

We have the plugin itself, a nagios configuration example with host,
commands and services descriptions, and a pnp4nagios configuration
example with some plot templates.

### Nagios

Nagios files.

check\_enviromux\_mini.py
  ~ check itself. See -h for help.

enviromux.cfg
  ~ nagios configuration example. Adapt to your own needs.

### pnp4nagios

pnp4nagios plotting example configuration.

check\_enviromux\_mini.cfg
  ~ pnp4nagios template name extraction from the nagios command used
    (check\_enviromux\_mini in this case).

check\_enviromux\_mini\_humidity1.php
  ~ sample humity plot for `humidity1` check.

check\_enviromux\_mini\_temperature1.php
  ~ sample temperature plor for `temperature1` check.

Files placement
---------------

In OMD ([Open Monitoring Distribution][], if you are not using it you
should! ;-) files should be placed like:

    ~/local/lib/nagios/plugins/check_enviromux_mini    # .py removed
    ~/etc/nagios/conf.d/enviromux.cfg
    ~/pnp4nagios/pnp4nagios/check_commands/check_enviromux_mini.cfg
    ~/pnp4nagios/templates/check_enviromux_mini_humidity1.php
    ~/pnp4nagios/templates/check_enviromux_mini_temperature1.php

In a regular nagios installation check for the equivalent paths.

  [inigo\_aldazabal@ehu.es]: mailto:inigo_aldazabal@ehu.es
  [enviromux-mini]: http://www.networktechinc.com/enviro-mini.html
  [Open Monitoring Distribution]: http://omdistro.org/

