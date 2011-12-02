****************************
Enviromux-mini nagios plugin
****************************

:Author: Inigo Aldazabal
:Contact: inigo_aldazabal@ehu.es
:Date: 2011/12/02

NAGIOS check for `enviromux-mini`_ sensor using SNMP.

.. _`enviromux-mini`: http://www.networktechinc.com/enviro-mini.html

Files description
=================

We have the plugin itself, a nagios configuration example with host, commands and services descriptions, and a pnp4nagios configuration example with some plot templates.

Nagios
------

Nagios files.

:check_enviromux_mini.py:  check itself. See -h for help.

:enviromux.cfg: nagios configuration example. Adapt to your own needs.


pnp4nagios
----------

pnp4nagios plotting example configuration.

:check_enviromux_mini.cfg: pnp4nagios template name extraction from the nagios command used (check_enviromux_mini in this case).

:check_enviromux_mini_humidity1.php: sample humity plot for ``humidity1`` check.

:check_enviromux_mini_temperature1.php: sample temperature plor for ``temperature1`` check.


Files placement
===============

In OMD (`Open Monitoring Distribution`_, if you are not using it you should! ;-) files should be placed like::

	~/local/lib/nagios/plugins/check_enviromux_mini    # .py removed
	~/etc/nagios/conf.d/enviromux.cfg
	~/pnp4nagios/pnp4nagios/check_commands/check_enviromux_mini.cfg
	~/pnp4nagios/templates/check_enviromux_mini_humidity1.php
	~/pnp4nagios/templates/check_enviromux_mini_temperature1.php

In a regular nagios installation check for the equivalent paths.

.. _`Open Monitoring Distribution`: http://omdistro.org/

