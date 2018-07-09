# opx-snmp



This file describes the SNMP agent implementation for OpenSwitch OPX.  The engine used is PySNMP, which is a lightweight Python-based extensible agent with rich functionality.  The agent implementation is also available in Python. Version 2 is currently supported, and will continue to be the default version of the agent.  Version 3 support will be available in the next release. The infrastructure supports implementation of any number of standard and proprietary MIBs, and users can extend it to support traps, snmpsets, and so on.



 



## Code organization



 



The SNMP agent code is organized into three areas:



 



* Engine code - provided by PySNMP libraries and users
generally don't  make changes to it

* Core agent - single Python file SNMPAgent serves as
the glue between the PySNMP engine and user-specific handlers that fetch data
from the backend. When a user implements a new MIB, they can make minimal code
changes (a few lines) here.

* Handlers - files contain all switch-specific code to get data
from the lower protocol layers of the switch. When new MIBs are introduced,
this is where the bulk of the code changes are expected.







 



 



## Code location on switch



 



Compiled MIBS:                 /usr/lib/python2.7/dist-packages/opx-snmp



Handlers:                            /usr/lib/python2.7/dist-packages/opx-snmp



Handlers utilities:              /usr/lib/python2.7/dist-packages/opx-snmp



Core agent:                        /usr/sbin/SNMPAgent



 



## Implemented MIBs:



 



* Interface table



 



## Add your own MIB



 



1. Compile your standard or proprietary MIB using
the compiler provided by PySNMP mibdump.py.  This generates an xyz-mib.py
file, which is a Python-ized form of the MIB that the PySNMP engine can
understand.

2. Place the generated xyz-mib.py file in a
location known to PySNMP (in the /usr/lib/python2.7/dist-packages/opx-snmp
directory). 

3. Replace all references to MibTableColumn with CustomMibTableColumn
in the generated xyz-mib.py file. Use the IF-MIB.py file in the same directory
as the example. This step ensures that when a get or getnext request is
received, it is redirected to your custom function, so that you can call the
appropriate handler routine.

4. Load the MIB to make the agent aware of it.
Enhance the loadMibs() function in the core agent SNMPAgent to include your new
MIB file.

5. Write your own handler functions to get data
from the backend for the MIB you are implementing.  Use the
/usr/lib/python2.7/dist-packages/opx-snmp/if_handlers.py file as an
example.  The 'handlers' dictionary at the end of the file is important. 
Place your new xyz_handler.py file in the same directory.

6. If any common utilities will be implemented
that other handler files can take advantage of, place them in handler_utils.py
file in the same directory. 

7. Make the agent aware of your new handler
functions.  Enhance the section under "load handlers" in SNMPAgent file to
do this.

8. Restart the agent. You should now be able to
do snmpget, snmpgetnext, and snmpwalk on this agent.

















 




