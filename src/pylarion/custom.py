# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals
import pylarion.base_polarion as bp


class Custom(bp.BasePolarion):
    '''Object to manage Polarion TestManagement WS tns4:Custom'''
    _cls_suds_map = {"key": "key", "value": "value"}
    _obj_client = "test_management_client"
    _obj_struct = "tns4:Custom"


class ArrayOfCustom(bp.BasePolarion):
    _obj_client = "test_management_client"
    _obj_struct = "tns4:ArrayOfCustom"
