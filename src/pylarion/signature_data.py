# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals
from pylarion.base_polarion import BasePolarion
from pylarion.enum_option_id import EnumOptionId


class SignatureData(BasePolarion):
    '''Container for the "tns4:SignatureData type'''
    _cls_suds_map = {"target_status_id": "targetStatusId",
                     "verdict":
                     {"field_name": "verdict",
                      "cls": EnumOptionId}}
    _obj_client = "builder_client"
    _obj_struct = "tns5:SignatureData"
