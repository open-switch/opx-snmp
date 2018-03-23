
###########################################################################
#
# Handlers for Interface MIB (IF-MIB)
#
###########################################################################

import cps
import cps_utils
import cps_object

from pysnmp.proto.api import v2c
from pysnmp.proto.rfc1902 import Integer

from opx_snmp.handler_utils import *

###########################################################################
#
# Get the NAS name for the given interface
#

def if_name_get(idx, nextf):
    k = {}
    if idx is not None:
        k['dell-base-if-cmn/if/interfaces/interface/if-index'] = idx
    if nextf:
        k['cps/object-group/get-next'] = 1
    r = cps_get('target',
                'dell-base-if-cmn/if/interfaces/interface',
                k
                )
    if r is None or len(r) == 0:
        return None
    r = r[0]['data']
    return (cps_utils.cps_attr_types_map.from_data('dell-base-if-cmn/if/interfaces/interface/if-index',
                                                   r['dell-base-if-cmn/if/interfaces/interface/if-index']
                                               ),
            cps_utils.cps_attr_types_map.from_data('if/interfaces/interface/name',
                                                   r.get('cps/key_data', r)['if/interfaces/interface/name']
                                               )
            )
    
###########################################################################
#
# Map the NAS name of an interface to the SNMP name
#

def if_name_map(nm):
    if nm is None:
        return None
    if nm.find('null') == 0 or nm.find('npu') == 0:
        return nm
    if nm.find('eth') == 0:
        return 'mgmt1/1/{0}'.format(int(nm[3:]) + 1)
    if nm.find('br') == 0:
        return nm.replace('br', 'vlan', 1)
    if nm.find('bo') == 0:
        return nm.replace('bo', 'port-channel', 1)
    if nm.find('lo') == 0:
        return nm.replace('bo', 'loopback', 1)
    s = nm.split('-')
    result = 'ethernet{0}/{1}/{2}'.format(int(s[0][1], 16),
                                          s[0][2:].lstrip('0'),
                                          s[1].lstrip('0')
    )
    if len(s) > 2 and s[2] != '0':
        result += ':' + s[2].lstrip('0')
    return result

###########################################################################
#
# Helper functions for forming handler results
#

def result_get(name, pr):
    return None if pr is None else (name, pr[1])

def result_get_first(name, pr):
    return None if pr is None else (name + (pr[0],), pr[1])

def result_get_next(name, pr):
    return None if pr is None else (name[0 : -1] + (pr[0],), pr[1])

###########################################################################
#
# Get interface index
#

def _if_idx_get(idx, nextf):
    k = {}
    if idx is not None:
        k['dell-base-if-cmn/if/interfaces/interface/if-index'] = idx
    if nextf:
        k['cps/object-group/get-next'] = 1
    r = cps_attrs_get('target',
                      'dell-base-if-cmn/if/interfaces/interface',
                      k,
                      ['dell-base-if-cmn/if/interfaces/interface/if-index']
                      )
    return None if r is None else r[0]


def if_idx_get(module, name):
    r = _if_idx_get(name[-1], False)
    return None if r is None else result_get(name, (r, Integer(r)))


def if_idx_get_first(module, name):
    r = _if_idx_get(None, True)
    return None if r is None else result_get_first(name, (r, Integer(r)))


def if_idx_get_next(module, name):
    r = _if_idx_get(name[-1], True)
    return None if r is None else result_get_next(name, (r, Integer(r)))

###########################################################################
#
# Get interface description
#

def if_descr_get(module, name):
    r = if_name_get(name[-1], False)
    return None if r is None else result_get(name, (r[0], v2c.OctetString(if_name_map(r[1]))))


def if_descr_get_first(module, name):
    r = if_name_get(None, True)
    return None if r is None else result_get_first(name, (r[0], v2c.OctetString(if_name_map(r[1]))))


def if_descr_get_next(module, name):
    r = if_name_get(name[-1], True)
    return None if r is None else result_get_next(name, (r[0], v2c.OctetString(if_name_map(r[1]))))

###########################################################################
#
# Get interface type
#

# Ideally, these should be extracted from the MIB...
IANAIFTYPE_OTHER            = 1
IANAIFTYPE_ETHERNETCSMACD   = 6
IANAIFTYPE_SOFTWARELOOPBACK = 24
IANAIFTYPE_TUNNEL           = 131
IANAIFTYPE_L2VLAN           = 135
IANAIFTYPE_L3IPVLAN         = 136
IANAIFTYPE_IEEE8023ADLAG    = 161


if_type_map = {"ianaift:ethernetCsmacd":   IANAIFTYPE_ETHERNETCSMACD,
               "base-if:management":       IANAIFTYPE_ETHERNETCSMACD,
               "ianaift:softwareLoopback": IANAIFTYPE_SOFTWARELOOPBACK,
               "ianaift:tunnel":           IANAIFTYPE_TUNNEL,
               "ianaift:l2vlan":           IANAIFTYPE_L2VLAN,
               "ianaift:l3ipvlan":         IANAIFTYPE_L3IPVLAN,
               "ianaift:ieee8023adLag":    IANAIFTYPE_IEEE8023ADLAG
}


def _if_type_get(idx, nextf):
    k = {}
    if idx is not None:
        k['dell-base-if-cmn/if/interfaces/interface/if-index'] = idx
    if nextf:
        k['cps/object-group/get-next'] = 1
    r = cps_attrs_get('target',
                      'dell-base-if-cmn/if/interfaces/interface',
                      k,
                      ['dell-base-if-cmn/if/interfaces/interface/if-index',
                       'if/interfaces/interface/type'
                      ]
    )
    return None if r is None else (r[0], Integer(if_type_map.get(r[1], IANAIFTYPE_OTHER)))


def if_type_get(module, name):
    return result_get(name, _if_type_get(name[-1], False))


def if_type_get_first(module, name):
    return result_get_first(name, _if_type_get(None, True))


def if_type_get_next(module, name):
    return result_get_next(name, _if_type_get(name[-1], True))

###########################################################################
#
# Get interface MTU
#

def _if_mtu_get(idx, nextf):
    k = {}
    if idx is not None:
        k['dell-base-if-cmn/if/interfaces/interface/if-index'] = idx
    if nextf:
        k['cps/object-group/get-next'] = 1
    r = cps_attrs_get('target',
                      'dell-base-if-cmn/if/interfaces/interface',
                      k,
                      ['dell-base-if-cmn/if/interfaces/interface/if-index',
                       'dell-if/if/interfaces/interface/mtu'
                      ]
    )
    if r is None:
        return None
    if r[1] is None:
        return (r[0], Integer(0))
    return (r[0], Integer(r[1]))


def if_mtu_get(module, name):
    return result_get(name, _if_mtu_get(name[-1], False))


def if_mtu_get_first(module, name):
    return result_get_first(name, _if_mtu_get(None, True))


def if_mtu_get_next(module, name):
    return result_get_next(name, _if_mtu_get(name[-1], True))

###########################################################################
#
# Get interface speed
#

def _if_speed_get(idx, nextf):
    idx = _if_idx_get(idx, nextf)
    if idx is None:
        return None
    r = cps_attrs_get('observed',
                      'dell-base-if-cmn/if/interfaces-state/interface',
                      {'if/interfaces-state/interface/if-index': idx}, 
                      ['if/interfaces-state/interface/speed']
    )
    if r is None:
        r = [0]
    return (idx, Integer(r[0]))


def if_speed_get(module, name):
    return result_get(name, _if_speed_get(name[-1], False))


def if_speed_get_first(module, name):
    return result_get_first(name, _if_speed_get(None, True))


def if_speed_get_next(module, name):
    return result_get_next(name, _if_speed_get(name[-1], True))

###########################################################################
#
# Get interface physical address
#

def _if_phys_addr_get(idx, nextf):
    k = {}
    if idx is not None:
        k['dell-base-if-cmn/if/interfaces/interface/if-index'] = idx
    if nextf:
        k['cps/object-group/get-next'] = 1
    r = cps_attrs_get('target',
                      'dell-base-if-cmn/if/interfaces/interface',
                      k,
                      ['dell-base-if-cmn/if/interfaces/interface/if-index',
                       'dell-if/if/interfaces/interface/phys-address'
                      ]
    )
    if r is None:
        return None
    if r[1] is None:
        return (r[0], v2c.OctetString([]))
    return (r[0], v2c.OctetString(map(lambda x: int(x, 16), r[1].split(':'))))

            
def if_phys_addr_get(module, name):
    return result_get(name, _if_phys_addr_get(name[-1], False))


def if_phys_addr_get_first(module, name):
    return result_get_first(name, _if_phys_addr_get(None, True))


def if_phys_addr_get_next(module, name):
    return result_get_next(name, _if_phys_addr_get(name[-1], True))

###########################################################################
#
# Get interface admin status
#

def _if_admin_status_get(idx, nextf):
    idx = _if_idx_get(idx, nextf)
    if idx is None:
        return None
    r = cps_attrs_get('observed',
                      'dell-base-if-cmn/if/interfaces-state/interface',
                      {'if/interfaces-state/interface/if-index': idx}, 
                      ['if/interfaces-state/interface/admin-status']
    )
    return (idx, Integer(1 if r is None else r[0]))


def if_admin_status_get(module, name):
    return result_get(name, _if_admin_status_get(name[-1], False))


def if_admin_status_get_first(module, name):
    return result_get_first(name, _if_admin_status_get(None, True))


def if_admin_status_get_next(module, name):
    return result_get_next(name, _if_admin_status_get(name[-1], True))

###########################################################################
#
# Get interface operational status
#

def _if_oper_status_get(idx, nextf):
    idx = _if_idx_get(idx, nextf)
    if idx is None:
        return None
    r = cps_attrs_get('observed',
                      'dell-base-if-cmn/if/interfaces-state/interface',
                      {'if/interfaces-state/interface/if-index': idx}, 
                      ['if/interfaces-state/interface/oper-status']
    )
    return (idx, Integer(1 if r is None else r[0]))


def if_oper_status_get(module, name):
    return result_get(name, _if_oper_status_get(name[-1], False))


def if_oper_status_get_first(module, name):
    return result_get_first(name, _if_oper_status_get(None, True))


def if_oper_status_get_next(module, name):
    return result_get_next(name, _if_oper_status_get(name[-1], True))

###########################################################################
#
# Get timestamp of last interface state change
# - Not implemented in NAS
#

def if_last_change(idx, nextf):
    idx = _if_idx_get(idx, nextf)
    return None if idx is None else (idx, Integer(0))

def if_last_change_get(module, name):
    return result_get(name, if_last_change(name[-1], False))


def if_last_change_get_first(module, name):
    return result_get_first(name, if_last_change(None, True))


def if_last_change_get_next(module, name):
    return result_get_next(name, if_last_change(name[-1], True))

###########################################################################
#
# Get a statistics counters
#

def if_stat_get(idx, nextf, attr):
    r = if_name_get(idx, nextf)
    if r is None:
        return None
    if_idx  = r[0]
    if_name = r[1]
    if if_name.find('bo') == 0:
        return if_stat_lag_get(if_idx, if_name, attr)
    r = cps_attrs_get('observed',
                      'dell-base-if-cmn/if/interfaces-state/interface/statistics',
                      {'if/interfaces-state/interface/name': if_name},
                      ['if/interfaces-state/interface/statistics/' + attr]
                  )
    if r is None:
        r = [0]
    elif r == []:
        r += [0]
    return (if_idx, Integer(r[0]))


def if_stat_lag_get(if_idx, if_name, attr):
    return (if_idx, 0)                    # TBD; must aggregate stats from LAG members


def if_in_octets_get(module, name):
    return result_get(name, if_stat_get(name[-1], False, 'in-octets'))


def if_in_octets_get_first(module, name):
    return result_get_first(name, if_stat_get(None, True, 'in-octets'))


def if_in_octets_get_next(module, name):
    return result_get_next(name, if_stat_get(name[-1], True, 'in-octets'))


def if_in_ucast_pkts_get(module, name):
    return result_get(name, if_stat_get(name[-1], False, 'in-unicast-pkts'))


def if_in_ucast_pkts_get_first(module, name):
    return result_get_first(name, if_stat_get(None, True, 'in-unicast-pkts'))


def if_in_ucast_pkts_get_next(module, name):
    return result_get_next(name, if_stat_get(name[-1], True, 'in-unicast-pkts'))


def if_in_nucast(module, name):
    return None


def if_in_discards_get(module, name):
    return result_get(name, if_stat_get(name[-1], False, 'in-discards'))


def if_in_discards_get_first(module, name):
    return result_get_first(name, if_stat_get(None, True, 'in-discards'))


def if_in_discards_get_next(module, name):
    return result_get_next(name, if_stat_get(name[-1], True, 'in-discards'))


def if_in_errors_get(module, name):
    return result_get(name, if_stat_get(name[-1], False, 'in-errors'))


def if_in_errors_get_first(module, name):
    return result_get_first(name, if_stat_get(None, True, 'in-errors'))


def if_in_errors_get_next(module, name):
    return result_get_next(name, if_stat_get(name[-1], True, 'in-errors'))


def if_in_unk_protos_get(module, name):
    return result_get(name, if_stat_get(name[-1], False, 'in-unknown-protos'))


def if_in_unk_protos_get_first(module, name):
    return result_get_first(name, if_stat_get(None, True, 'in-unknown-protos'))


def if_in_unk_protos_get_next(module, name):
    return result_get_next(name, if_stat_get(name[-1], True, 'in-unknown-protos'))


def if_out_octets_get(module, name):
    return result_get(name, if_stat_get(name[-1], False, 'out-octets'))


def if_out_octets_get_first(module, name):
    return result_get_first(name, if_stat_get(None, True, 'out-octets'))


def if_out_octets_get_next(module, name):
    return result_get_next(name, if_stat_get(name[-1], True, 'out-octets'))


def if_out_ucast_pkts_get(module, name):
    return result_get(name, if_stat_get(name[-1], False, 'out-unicast-pkts'))


def if_out_ucast_pkts_get_first(module, name):
    return result_get_first(name, if_stat_get(None, True, 'out-unicast-pkts'))


def if_out_ucast_pkts_get_next(module, name):
    return result_get_next(name, if_stat_get(name[-1], True, 'out-unicast-pkts'))


def if_out_discards_get(module, name):
    return result_get(name, if_stat_get(name[-1], False, 'out-discards'))


def if_out_discards_get_first(module, name):
    return result_get_first(name, if_stat_get(None, True, 'out-discards'))


def if_out_discards_get_next(module, name):
    return result_get_next(name, if_stat_get(name[-1], True, 'out-discards'))


def if_out_errors_get(module, name):
    return result_get(name, if_stat_get(name[-1], False, 'out-errors'))


def if_out_errors_get_first(module, name):
    return result_get_first(name, if_stat_get(None, True, 'out-errors'))


def if_out_errors_get_next(module, name):
    return result_get_next(name, if_stat_get(name[-1], True, 'out-errors'))

###########################################################################
#
# Catch-all for deprecated columns

def if_deprecated(module, name):
    return None

###########################################################################
#
# Table of handlers, for agent
#

handlers = (
    (('IF-MIB', 'ifIndex'),           (if_idx_get,             if_idx_get_first,             if_idx_get_next)),
    (('IF-MIB', 'ifDescr'),           (if_descr_get,           if_descr_get_first,           if_descr_get_next)),
    (('IF-MIB', 'ifType'),            (if_type_get,            if_type_get_first,            if_type_get_next)),
    (('IF-MIB', 'ifMtu'),             (if_mtu_get,             if_mtu_get_first,             if_mtu_get_next)),
    (('IF-MIB', 'ifPhysAddress'),     (if_phys_addr_get,       if_phys_addr_get_first,       if_phys_addr_get_next)),
    (('IF-MIB', 'ifSpeed'),           (if_speed_get,           if_speed_get_first,           if_speed_get_next)),
    (('IF-MIB', 'ifPhysAddress'),     (if_phys_addr_get,       if_phys_addr_get_first,       if_phys_addr_get_next)),
    (('IF-MIB', 'ifAdminStatus'),     (if_admin_status_get,    if_admin_status_get_first,    if_admin_status_get_next)),
    (('IF-MIB', 'ifOperStatus'),      (if_oper_status_get,     if_oper_status_get_first,     if_oper_status_get_next)),
    (('IF-MIB', 'ifLastChange'),      (if_last_change_get,     if_last_change_get_first,     if_last_change_get_next)),
    (('IF-MIB', 'ifInOctets'),        (if_in_octets_get,       if_in_octets_get_first,       if_in_octets_get_next)),
    (('IF-MIB', 'ifInUcastPkts'),     (if_in_ucast_pkts_get,   if_in_ucast_pkts_get_first,   if_in_ucast_pkts_get_next)),
    (('IF-MIB', 'ifInNUcastPkts'),    (if_deprecated,          if_deprecated,                if_deprecated)),
    (('IF-MIB', 'ifInDiscards'),      (if_in_discards_get,     if_in_discards_get_first,     if_in_discards_get_next)),
    (('IF-MIB', 'ifInErrors'),        (if_in_errors_get,       if_in_errors_get_first,       if_in_errors_get_next)),
    (('IF-MIB', 'ifInUnknownProtos'), (if_in_unk_protos_get,   if_in_unk_protos_get_first,   if_in_unk_protos_get_next)),
    (('IF-MIB', 'ifOutOctets'),       (if_out_octets_get,      if_out_octets_get_first,      if_out_octets_get_next)),
    (('IF-MIB', 'ifOutUcastPkts'),    (if_out_ucast_pkts_get,  if_out_ucast_pkts_get_first,  if_out_ucast_pkts_get_next)),
    (('IF-MIB', 'ifOutNUcastPkts'),   (if_deprecated,          if_deprecated,                if_deprecated)),
    (('IF-MIB', 'ifOutDiscards'),     (if_out_discards_get,    if_out_discards_get_first,    if_out_discards_get_next)),
    (('IF-MIB', 'ifOutErrors'),       (if_out_errors_get,      if_out_errors_get_first,      if_out_errors_get_next)),
    (('IF-MIB', 'ifOutQLen'),         (if_deprecated,          if_deprecated,                if_deprecated)),
    (('IF-MIB', 'ifSpecific'),        (if_deprecated,          if_deprecated,                if_deprecated))
    )
