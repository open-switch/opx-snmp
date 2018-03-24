###########################################################################
#
# Helper functions for the CPS API
#
###########################################################################

import cps
import cps_utils
import cps_object

###########################################################################
#
# Do CPS API get request
#

def cps_get(q, obj, attrs={}):
    resp = []
    return resp if cps.get([cps_object.CPSObject(obj,
                                                 qual=q,
                                                 data=attrs
                                             ).get()
                        ], resp
    ) else None

###########################################################################
#
# Extract the given attribute from a CPS API get response
#

def cps_attr_data_get(obj, attr):
    d = obj['data']
    if attr not in d:
        return None
    return cps_utils.cps_attr_types_map.from_data(attr, d[attr])

###########################################################################
#
# Extract the given key attribute from a CPS API get response
#

def cps_key_attr_data_get(obj, attr):
    d = obj['data']
    if 'cps/key_data' in d and attr in d['cps/key_data']:
        return cps_utils.cps_attr_types_map.from_data(attr, d['cps/key_data'][attr])
    if attr not in d:
        return None
    return cps_utils.cps_attr_types_map.from_data(attr, d[attr])
