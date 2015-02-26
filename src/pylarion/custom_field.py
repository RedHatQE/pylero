# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals
import pylarion.base_polarion as bp
from pylarion.enum_option_id import EnumOptionId


class CustomField(bp.BasePolarion):
    """Object to handle the Polarion WSDL tns3:CustomField class

    Attributes (for specific details, see Polarion):
        key (string)
        parent_item_uri (string)
        value (anyType)
"""
    _cls_suds_map = {"key": "key",
                     "parent_item_uri": "parentItemURI",
                     "value": {"field_name": "value", "cls": EnumOptionId},
                     "uri": "_uri",
                     "_unresolved": "_unresolved"}
    _obj_client = "tracker_client"
    _obj_struct = "tns3:CustomField"
