# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals
import pylarion.base_polarion as bp


class ActivityCustomValue(bp.BasePolarion):
    """Object to handle the Polarion WSDL tns3:ActivityCustomValue class

    Attributes (for specific details, see Polarion):
        values (ArrayOf_xsd_string)
"""
    _cls_suds_map = {"values": "values",
                     "uri": "_uri",
                     "_unresolved": "_unresolved"}
    _obj_client = "tracker_client"
    _obj_struct = "tns3:ActivityCustomValue"
