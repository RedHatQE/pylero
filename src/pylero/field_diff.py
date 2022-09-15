# -*- coding: utf8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from pylero.base_polarion import BasePolarion


class FieldDiff(BasePolarion):
    """Object to handle the Polarion WSDL tns3:FieldDiff class

    Attributes:
        added (ArrayOf_xsd_anyType)
        after (anyType)
        before (anyType)
        collection (boolean)
        field_name (string)
        removed (ArrayOf_xsd_anyType)"""

    _cls_suds_map = {
        "added": "added",
        "after": "after",
        "before": "before",
        "collection": "collection",
        "field_name": "fieldName",
        "removed": "removed",
        "uri": "_uri",
        "_unresolved": "_unresolved",
    }
    _obj_client = "tracker_client"
    _obj_struct = "tns3:FieldDiff"
