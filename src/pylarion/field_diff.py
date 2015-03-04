# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals
import pylarion.base_polarion as bp


class FieldDiff(bp.BasePolarion):
    """Object to handle the Polarion WSDL tns3:FieldDiff class

    Attributes (for specific details, see Polarion):
        added (ArrayOf_xsd_anyType)
        after (anyType)
        before (anyType)
        collection (boolean)
        field_name (string)
        removed (ArrayOf_xsd_anyType)
"""
    _cls_suds_map = {"added": "added",
                     "after": "after",
                     "before": "before",
                     "collection": "collection",
                     "field_name": "fieldName",
                     "removed": "removed",
                     "uri": "_uri",
                     "_unresolved": "_unresolved"}
    _obj_client = "tracker_client"
    _obj_struct = "tns3:FieldDiff"
