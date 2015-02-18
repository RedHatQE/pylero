# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals
import pylarion.base_polarion as bp


class ActivitySource(bp.BasePolarion):
    """Object to handle the Polarion WSDL tns3:ActivitySource class

    Attributes (for specific details, see Polarion):
        activity_source_id (string)
        prefix (string)
        types (ArrayOf_xsd_string)
"""
    _cls_suds_map = {"activity_source_id": "id",
                     "prefix": "prefix",
                     "types": "types",
                     "uri": "_uri",
                     "_unresolved": "_unresolved"}
    _obj_client = "tracker_client"
    _obj_struct = "tns3:ActivitySource"
