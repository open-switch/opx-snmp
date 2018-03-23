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
# Do a CPS API get request, and extract the given attributes from the response
#

def cps_attrs_get(qual, obj, key, attrs):
    r = cps_get(qual, obj, key)
    if r is None or len(r) == 0:
        return None
    r = r[0]
    li = ()
    for a in attrs:
        li += (cps_attr_data_get(r, a),)
    return li

