*********************************************
Notas de integración de enviromux-mini en OMD
*********************************************

.. footer:: ###Page###
.. contents::
.. section-numbering::

ENVIROMUX-MINI data
===================

:IP: 10.0.0.49 (static)
:MAC: 00:0C:82:01:16:71
:Web interface: Administrator/admin
:SNMP community: public
:SNMP Trap destination: undefined

:Firmaware version: 1.41


SNMP OIDs
=========

De check_nti_snmp.pl vemos que los OID están en el rango .1.3.6.1.4.1.3699, así que para ver que pinta tienen (recordar que por defecto snmpwalk por defecto solo recorre el stansard-MIB)::

	$> snmpwalk -v1 -c 'public' -m '' -M '' -On -Ob -OQ -Ot 10.0.0.49 1.3.6.1.4.1.3699
	.1.3.6.1.4.1.3699.1.1.3.1.0 = "76 31 2E 33 2E 32 00 "
	.1.3.6.1.4.1.3699.1.1.3.1.1.1.0 = 655350
	.1.3.6.1.4.1.3699.1.1.3.1.1.2.0 = 0
	.1.3.6.1.4.1.3699.1.1.3.1.2.1.0 = 221
	.1.3.6.1.4.1.3699.1.1.3.1.2.2.0 = 0
	.1.3.6.1.4.1.3699.1.1.3.1.3.1.0 = 655350
	.1.3.6.1.4.1.3699.1.1.3.1.3.2.0 = 0
	.1.3.6.1.4.1.3699.1.1.3.1.4.1.0 = 420
	.1.3.6.1.4.1.3699.1.1.3.1.4.2.0 = 0
	.1.3.6.1.4.1.3699.1.1.3.1.5.1.0 = 0
	.1.3.6.1.4.1.3699.1.1.3.1.5.2.0 = 0
	.1.3.6.1.4.1.3699.1.1.3.1.6.1.0 = 0
	.1.3.6.1.4.1.3699.1.1.3.1.6.2.0 = 0
	.1.3.6.1.4.1.3699.1.1.3.1.7.1.0 = 0
	.1.3.6.1.4.1.3699.1.1.3.1.7.2.0 = 0
	.1.3.6.1.4.1.3699.1.1.3.1.8.1.0 = 0
	.1.3.6.1.4.1.3699.1.1.3.1.8.2.0 = 0
	.1.3.6.1.4.1.3699.1.1.3.1.9.1.0 = 0
	.1.3.6.1.4.1.3699.1.1.3.1.9.2.0 = 0
	.1.3.6.1.4.1.3699.1.1.3.2.1.1.0 = "ENVIROMUX-MINI"
	.1.3.6.1.4.1.3699.1.1.3.2.1.2.0 = "CPD-1"
	.1.3.6.1.4.1.3699.1.1.3.2.1.3.0 = "10.0.0.49"
	.1.3.6.1.4.1.3699.1.1.3.2.1.4.0 = "255.255.254.0"
	.1.3.6.1.4.1.3699.1.1.3.2.1.5.0 = "10.0.0.1"
	.1.3.6.1.4.1.3699.1.1.3.2.1.6.0 = "192.168.1.2"
	.1.3.6.1.4.1.3699.1.1.3.2.2.1.0 = "Temperature #1"
	.1.3.6.1.4.1.3699.1.1.3.2.2.2.0 = "Celsius"
	.1.3.6.1.4.1.3699.1.1.3.2.2.3.0 = "5.0"
	.1.3.6.1.4.1.3699.1.1.3.2.2.4.0 = "38.0"
	.1.3.6.1.4.1.3699.1.1.3.2.3.1.0 = "Temperature #2"
	.1.3.6.1.4.1.3699.1.1.3.2.3.2.0 = "Celsius"
	.1.3.6.1.4.1.3699.1.1.3.2.3.3.0 = "5.0"
	.1.3.6.1.4.1.3699.1.1.3.2.3.4.0 = "38.0"
	.1.3.6.1.4.1.3699.1.1.3.2.4.1.0 = "Humidity #1"
	.1.3.6.1.4.1.3699.1.1.3.2.4.2.0 = "20.0"
	.1.3.6.1.4.1.3699.1.1.3.2.4.3.0 = "75.0"
	.1.3.6.1.4.1.3699.1.1.3.2.5.1.0 = "Humidity #2"
	.1.3.6.1.4.1.3699.1.1.3.2.5.2.0 = "20.0"
	.1.3.6.1.4.1.3699.1.1.3.2.5.3.0 = "75.0"
	.1.3.6.1.4.1.3699.1.1.3.2.6.1.0 = "Dry Contact #1"
	.1.3.6.1.4.1.3699.1.1.3.2.6.2.0 = 1
	.1.3.6.1.4.1.3699.1.1.3.2.7.1.0 = "Dry Contact #2"
	.1.3.6.1.4.1.3699.1.1.3.2.7.2.0 = 1
	.1.3.6.1.4.1.3699.1.1.3.2.8.1.0 = "Dry Contact #3"
	.1.3.6.1.4.1.3699.1.1.3.2.8.2.0 = 1
	.1.3.6.1.4.1.3699.1.1.3.2.9.1.0 = "Dry Contact #4"
	.1.3.6.1.4.1.3699.1.1.3.2.9.2.0 = 1
	.1.3.6.1.4.1.3699.1.1.3.2.10.1.0 = "Water #1"
	.1.3.6.1.4.1.3699.1.1.3.2.10.2.0 = 1
	.1.3.6.1.4.1.3699.1.1.3.3.0 = "31 2E 34 31 00 00 "
	End of MIB


y ahí ya vemos los datos sin problemas, tal y como están reflejados en el check_nti_snmp.pl.

Del libro `Nagios 3 Enterprise Network Monitoring Including Plug-Ins and Hardware Devices, Elsevier 2008`, página 236 y siguientes::

    temperatureSensor1CurrentValue: 1.3.6.1.4.1.3699.1.1.3.1.1.1
    temperatureSensor1Alert: 1.3.6.1.4.1.3699.1.1.3.1.1.2
    temperatureSensor2CurrentValue: 1.3.6.1.4.1.3699.1.1.3.1.2.1
    temperatureSensor2Alert: 1.3.6.1.4.1.3699.1.1.3.1.2.2
    humiditySensor1CurrentValue: 1.3.6.1.4.1.3699.1.1.3.1.3.1
    humiditySensor1Alert: 1.3.6.1.4.1.3699.1.1.3.1.3.2
    humiditySensor2CurrentValue: 1.3.6.1.4.1.3699.1.1.3.1.4.1
    humiditySensor2Alert: 1.3.6.1.4.1.3699.1.1.3.1.4.2
    dryContact1Status: 1.3.6.1.4.1.3699.1.1.3.1.5.1
    dryContact1Alert: 1.3.6.1.4.1.3699.1.1.3.1.5.2
    dryContact2Status: 1.3.6.1.4.1.3699.1.1.3.1.6.1
    dryContact2Alert: 1.3.6.1.4.1.3699.1.1.3.1.6.2
    dryContact3Status: 1.3.6.1.4.1.3699.1.1.3.1.7.1
    dryContact3Alert: 1.3.6.1.4.1.3699.1.1.3.1.7.2
    dryContact4Status: 1.3.6.1.4.1.3699.1.1.3.1.8.1
    dryContact4Alert: 1.3.6.1.4.1.3699.1.1.3.1.8.2
    waterStatus: 1.3.6.1.4.1.3699.1.1.3.1.9.1
    waterAlert: 1.3.6.1.4.1.3699.1.1.3.1.9.2
    temperatureSensor1Name: 1.3.6.1.4.1.3699.1.1.3.2.2.1
    temperatureSensor1Unit: 1.3.6.1.4.1.3699.1.1.3.2.2.2
    temperatureSensor1LowThreshold: 1.3.6.1.4.1.3699.1.1.3.2.2.3
    temperatureSensor1HighThreshold: 1.3.6.1.4.1.3699.1.1.3.2.2.4
    temperatureSensor2Name: 1.3.6.1.4.1.3699.1.1.3.2.3.1
    temperatureSensor2Unit: 1.3.6.1.4.1.3699.1.1.3.2.3.2
    temperatureSensor2LowThreshold: 1.3.6.1.4.1.3699.1.1.3.2.3.3
    temperatureSensor2HighThreshold: 1.3.6.1.4.1.3699.1.1.3.2.3.4
    humiditySensor1Name: 1.3.6.1.4.1.3699.1.1.3.2.4.1
    humiditySensor1LowThreshold: 1.3.6.1.4.1.3699.1.1.3.2.4.2
    humiditySensor1HighThreshold: 1.3.6.1.4.1.3699.1.1.3.2.4.3
    humiditySensor2Name: 1.3.6.1.4.1.3699.1.1.3.2.5.1
    humiditySensor2LowThreshold: 1.3.6.1.4.1.3699.1.1.3.2.5.2
    humiditySensor2HighThreshold: 1.3.6.1.4.1.3699.1.1.3.2.5.3
    dryContact1Name: 1.3.6.1.4.1.3699.1.1.3.2.6.1
    dryContact1AlertStatus: 1.3.6.1.4.1.3699.1.1.3.2.6.2
    dryContact2Name: 1.3.6.1.4.1.3699.1.1.3.2.7.1
    dryContact2AlertStatus: 1.3.6.1.4.1.3699.1.1.3.2.7.2
    dryContact3Name: 1.3.6.1.4.1.3699.1.1.3.2.8.1
    dryContact3AlertStatus: 1.3.6.1.4.1.3699.1.1.3.2.8.2
    dryContact4Name: 1.3.6.1.4.1.3699.1.1.3.2.9.1
    dryContact4AlertStatus: 1.3.6.1.4.1.3699.1.1.3.2.9.2
    waterName: 1.3.6.1.4.1.3699.1.1.3.2.10.1
    waterAlertStatus: 1.3.6.1.4.1.3699.1.1.3.2.10.2


Por ejemplo::

	inigo:ENVIROMUX-MINI> snmpwalk -v1 -c 'public' -m '' -M '' -On -Ob -OQ -Ot 10.0.0.49 1.3.6.1.4.1.3699.1.1.3.1.2.1
	.1.3.6.1.4.1.3699.1.1.3.1.2.1.0 = 224

i.e. 22.4 grados celsius!

Quizas lo mas fácil sea hacer un script en python que haga el snmp y devuelva algo del tipo::

	<<enviromux>>
	OK - Temp#1 22.4 deg. Celsius|temp=22.4;;;;|
	OK - Humidity#1 46% humidity|humidity=46;;;;;|
	etc...

¿Esto se lo traga fácilmente check_mk? Mirarlo pues sería la forma mas fácil. Mucho mas que hacer un script a integrar en check_mk, claro.

La alternativa a esto es hacer un legacy check por parámetro y meterlo a mano en main.ck, que tampoco es para tanto pues de momento son 5 checks (temp, hum, water, CRAC1, CRAC2).

Hacerlo nosotros uno a uno es debido a que parece que lo generado por el script check_nti_snmp.pl no devuelve performance paramenters en formato estandar, si no podríamos hacerlo directamente con él::

	inigo:ENVIROMUX-MINI> ./check_nti_snmp.pl -H 10.0.0.49 -m single -C public -p enviromuxMini -L temperatureSensor2 -i 1
	OK - Temperature #2 22.2Celsius |Temperature_#2=22.2Celsius;;;; 

Sobra el ``Celsius`` del final.

Podemos mirar directamente los parámetros con check_snmp de nagios::

	OMD[cfm]:~/lib/nagios/plugins$ ./check_snmp  -H 10.0.0.49 -C public -P 1 -o 1.3.6.1.4.1.3699.1.1.3.1.2.1.0
	SNMP OK - 222 | iso.3.6.1.4.1.3699.1.1.3.1.2.1.0=222 

o mas sencillo::

	OMD[cfm]:~/etc/nagios$ /omd/sites/cfm/version/lib/nagios/plugins/check_snmp -H 10.0.0.49 -o 1.3.6.1.4.1.3699.1.1.3.1.2.1.0
	SNMP OK - 224 | iso.3.6.1.4.1.3699.1.1.3.1.2.1.0=224 


Sensors
-------

Temperatura/humedad: el puerto #1 es el derecho y el #2 el izquierdo.

dryContact1:
    1 = contacto cerrado
    0 = contacto abierto
    nombre del sensor
    .1.3.6.1.4.1.3699.1.1.3.2.6.1.0 = "Dry Contact #1"
    Alarma cuando estado sea (0)
    .1.3.6.1.4.1.3699.1.1.3.2.6.2.0 = 0
    Estado del sensor (1)
    .1.3.6.1.4.1.3699.1.1.3.1.5.1.0 = 1

dryContact{1,2,3,4}, waterSensor:
    1 = contacto cerrado
    0 = contacto abierto
    nombre del sensor
    .1.3.6.1.4.1.3699.1.1.3.2.{6,7,8,9,10}.1.0 = "Dry Contact #1"
    Alarma cuando estado sea (0)
    .1.3.6.1.4.1.3699.1.1.3.2.{6,7,8,9,10}.2.0 = 0
    Estado del sensor (1)
    .1.3.6.1.4.1.3699.1.1.3.1.{5,6,7,8,9}.1.0 = 1

temperatureSensor1:
    .1.3.6.1.4.1.3699.1.1.3.2.2.1.0 = "Temperature #1"
    .1.3.6.1.4.1.3699.1.1.3.2.2.2.0 = "Celsius"
    .1.3.6.1.4.1.3699.1.1.3.2.2.3.0 = "5.0"
    .1.3.6.1.4.1.3699.1.1.3.2.2.4.0 = "38.0"
    .1.3.6.1.4.1.3699.1.1.3.1.1.1.0 = 240

temperatureSensor2
    .1.3.6.1.4.1.3699.1.1.3.2.3.1.0 = "Temperature #2"
    .1.3.6.1.4.1.3699.1.1.3.2.3.2.0 = "Celsius"
    .1.3.6.1.4.1.3699.1.1.3.2.3.3.0 = "5.0"
    .1.3.6.1.4.1.3699.1.1.3.2.3.4.0 = "38.0"
    .1.3.6.1.4.1.3699.1.1.3.1.2.1.0 = 241

humiditySensor1:
    .1.3.6.1.4.1.3699.1.1.3.2.4.1.0 = "Humidity #1"
    .1.3.6.1.4.1.3699.1.1.3.2.4.2.0 = "20.0"
    .1.3.6.1.4.1.3699.1.1.3.2.4.3.0 = "75.0"
    .1.3.6.1.4.1.3699.1.1.3.1.3.1.0 = 390

humiditySensor2:
    .1.3.6.1.4.1.3699.1.1.3.2.5.1.0 = "Humidity #2"
    .1.3.6.1.4.1.3699.1.1.3.2.5.2.0 = "30.0"
    .1.3.6.1.4.1.3699.1.1.3.2.5.3.0 = "75.0"
    .1.3.6.1.4.1.3699.1.1.3.1.4.1.0 = 390


Checks normales en Nagios
=========================

Primero hacemos checks normales de nagios tal y como hicimos con el NAS. Es decir, definimos el host y todo a mano en nuestra configuración de nagios, independientemente de check_mk. Luego multisite lo mostrará sin problemas; es solo la configuración de los checks lo que es independiente de check_mk.


Para comprobar por ejemplo la temperatura del sensor Temperature#2 hacemos::

    OMD[cfm]:~$ snmpget -c public -v1 10.0.0.49  1.3.6.1.4.1.3699.1.1.3.1.1.1.0
    SNMPv2-SMI::enterprises.3699.1.1.3.1.1.1.0 = INTEGER: 244

Esto lo haremos a traes de un script en python que recoja lo que haga falta
dependiendo de las opciones.

Ejemplo para obtener los datos::

    In [34]: temp = os.popen("snmpget -v1 -c 'public' 10.0.0.49 1.3.6.1.4.1.3699.1.1.3.1.1.1.0", "r").readline()

    In [35]: temp
    Out[35]: 'SNMPv2-SMI::enterprises.3699.1.1.3.1.1.1.0 = INTEGER: 238\n'

    In [36]: temp.strip().split()[-1]
    Out[36]: '238'

    In [37]: float(temp.strip().split()[-1])/10
    Out[37]: 23.800000000000001

    In [38]: print( "%2.1f" %(float(temp.strip().split()[-1])/10) )
    23.8

O definiendo las variables adecuadas::

    In [39]: command = "snmpget -v1 -c %s %s %s" %(community, ip, oid)
    In [40]: temp = os.popen(command, "r").readline()


Tras un cierto curro ya tenemos el script ``check_enviromux.py`` que nos genera la salida adecuada (ver la ayuda ``-h``)::

    inigo:ENVIROMUX-MINI> ./check_enviromux.py 10.0.0.49 -s temperature1 -w 35 -c 40
    OK - Temperature #1 sensor reading is 22.6 Celsius|Temperature_#1=22.6;35.0;40.0;0.;45.
    inigo:ENVIROMUX-MINI> ./check_enviromux.py 10.0.0.49 -s humidity1 -w40 -c 70
    WARNING - Humidity #1 sensor reading is 42.0 %|Humidity_#1=42.0%;40.0;70.0;20.;85.
    inigo:ENVIROMUX-MINI> ./check_enviromux.py 10.0.0.49 -s water
    OK - No water detected
    inigo:ENVIROMUX-MINI> ./check_enviromux.py 10.0.0.49 -s contact1
    CRITICAL - Dry Contact #1: contact is CLOSED!


Configuración de Nagios
-----------------------

Por un lado tendremos la configuración del host y servicios en nagios y por otro la configuración de la graficación de los datos en pnp4nagios.

La primera la hacemos directamente en un archivo ``enviromux.cfg``

La segunda es mas complicada y la detallamos a continuación.


PNP4Nagios
~~~~~~~~~~

Veamos el ejemplo de la temperatura. El chequeo lo hemos definido como::

    define service{
    	use 			generic-service
    	host_name 		Enviromux-TEST
    	service_description 	Temperature #1
    	check_command 		check_enviromux!public!temperature1!30!38

Cada vez que Nagios ejecuta un comando (en este caso ``check_enviromux``) busca el template correspondiente con el nombre ``check_enviromux.php`` en este caso. Si no lo encuentra usa por defecto el template ``default.php``. Los templates se encuentran en ``share/templates.dist`` los incluidos con PNP4Nagios y en ``share/templates`` los creados por nosotros y que no se deben actualizar al actualizar PNP4Nagios.

El problema en este caso es que tenemos varios checks que utilizan el mismo comando, ``check_enviromux``. Lo que se hace en estos casos es un custom template. Para ello en el archivo de configuración ``etc/check_commands/check_enviromux.cfg`` se le dice que en caso en que llame al comando, debe utilizar para buscar el template por ejempl el segundo argumento de la llamada (en este caso buscaría pues el template ``temperature1.php``, pero se pueden hacer combinaciones tipo ``check_enviromux_template1.php`` y cosas así). Esto está muy bien explicado en `este blog`_ y en la documentación oficial de PNP4Nagios, en la sección de `custom templates`_.

.. _`este blog`: http://askaralikhan.blogspot.com/2010/01/creating-custom-template-in-pnp4nagios.html
.. _`custom templates`: http://docs.pnp4nagios.org/pnp-0.6/tpl_custom

En realidad lo que busca PNP4Nagios al ejecutar un comando que devuelve perfdata es un fichero ``perfdata/hostname/check_name.xml``. Este fichero lo genera parece que nagio automáticamente y en el está indicado qué template php debe utilizar en la sección ``<TEMPLATE> ... </TEMPLATE>``. En él podemos comprobar que el tema esté bien configurado. En el caso de *OMD* estos ficheros están en ``~/var/pnp4nagios/perfdata``. **Los datos rdd** también se encuentran en esa ruta.

check_mk checks
===============

Para los checks nativos de check_mk tenemos la duda inicial de si hacer todo en un mismo check. Después de examinar otros checks veo que no hay problema en hacerlo, excepto por el tema de los niveles de alerta.

Si queremos que los chequéos sean simultáneos tenemos dos opciones:

a. que los niveles de alerta estén hard-coded *malo*,  o bien

b. utilizar los niveles de alerta definidos en el mismo enviromux a través del interface web.

Esta última opción no estaría mal excepto por el hecho de que los niveles de alerta de temperatura se definen como a<t<c en enviromux, y nosotros queremos que para a<t tengamos warning y para t>c critical. Si podemos/queremos no utilizar las alertas propias de enviromux no habría problema.

Si finalmente queremos poner unos parámetros por defecto o modificables desde check_mk entonces habría que separar los chequeos en varios, al menos en grupos de temperatura, humedad, agua y contactos. Luego ya podríamos diferenciar en ellos igual que hace ``df``, dando niveles distintos p.ej. según el disco.

.. warning::
        ¡Ojo tambíen al tema de los gráficos y las barra visual! Puede que también sea mucho mas sencillo con chequeos separados.


multiples sensores snmp
-----------------------

Si queremos leer dos sensores por ejemplo hay que hacerlo (o al menos no veo otra forma por cómo es el mib) siguiendo el ejemplo del chequeo ``cisco_qos`` y haciendo de forma similar (lo de los OID_END no lo entiendo)::

        snmp_info["enviromux_mini"] = \
        [
        #temperatureSensor1
        ( ".1.3.6.1.4.1.3699.1.1.3",
        [ "1.1.1", "1.1.2", "2.2.1", "2.2.2", "2.2.3", "2.2.4" ] ),
        #temperatureSensor2
        ( ".1.3.6.1.4.1.3699.1.1.3",
        [ "1.2.1", "1.2.2", "2.3.1", "2.3.2", "2.3.3", "2.3.4" ] )
        ]

Ojo que esto devuelve una lista de listas de listas, no una lista de listas como en el ejmplo de la documentación::

        OMD[cfm]:~/src$ cmk -I --checks enviromux_mini 10.0.0.49
        [[['231', '0', 'Temperature #1', 'Celsius', '5.0', '38.0']],
         [['655350', '0', 'Temperature #2', 'Celsius', '5.0', '38.0']]]


