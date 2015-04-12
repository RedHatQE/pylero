# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals
from pylarion.base_polarion import BasePolarion


class CustomField(BasePolarion):
    """Object to handle the Polarion WSDL tns3:CustomField class

    Attributes:
        key (string)
        parent_item_uri (string)
        value (anyType)
"""
    _cls_suds_map = {"key": "key",
                     "parent_item_uri": "parentItemURI",
                     "value": "value"}
    _obj_client = "tracker_client"
    _obj_struct = "tns3:CustomField"
