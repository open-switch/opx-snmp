#!/usr/bin/python

###########################################################################
#
# Handlers for SYSTEM MIB (SNMP MIB-2)
#
###########################################################################

from ConfigParser import SafeConfigParser

# default configurations file

conf_file = '/etc/opx/snmp/opx_snmp.conf'


###########################################################################
#
# Read system variables value from opx_snmp.conf file
#

def sys_value_get(sys_obj):
    if not conf_file:
        print 'no conf file existing'
        sys_obj.exit(-1)
    config = SafeConfigParser()
    config.read(conf_file)
    for system in [s for s in config.sections() if s.startswith('system')]:
        return config.get(system, sys_obj)


###########################################################################
#
# Return a custom value for SysDescr to SNMPAgent
#

def sys_descr_get(sys_obj):
    fp = open('/etc/OPX-release-version', 'r')

    for line in fp:
        if line.startswith('PLATFORM'):
            platform = line.split('=')[-1]
            platform = 'Platform:' + str(platform).strip('\n').replace('"', '')

        if line.startswith('OS_VERSION'):
            os_version = 'NOS:OPX' + line.split('=')[-1].strip('\n').replace('"', '')

    return platform + ', ' + os_version


###########################################################################
#
# Table of handlers, for agent
#

handlers = (
    (('SNMPv2-MIB', 'sysName'), sys_value_get),
    (('SNMPv2-MIB', 'sysDescr'), sys_descr_get),
    (('SNMPv2-MIB', 'sysContact'), sys_value_get),
    (('SNMPv2-MIB', 'sysLocation'), sys_value_get),
    (('SNMPv2-MIB', 'sysServices'), sys_value_get),
    (('SNMPv2-MIB', 'sysObjectID'), sys_value_get),
    )



