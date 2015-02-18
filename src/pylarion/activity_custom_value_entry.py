# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals
import pylarion.base_polarion as bp
import pylarion.activity_custom_value as acv


class ActivityCustomValueEntry(bp.BasePolarion):
    """Object to handle the Polarion WSDL tns3:ActivityCustomValueEntry class

    Attributes (for specific details, see Polarion):
        custom_values (ActivityCustomValue)
        key (string)
"""
    _cls_suds_map = {"custom_values": {"field_name": "customValues",
                                       "cls": acv.ActivityCustomValue},
                     "key": "key",
                     "uri": "_uri",
                     "_unresolved": "_unresolved"}
    _obj_client = "tracker_client"
    _obj_struct = "tns3:ActivityCustomValueEntry"
