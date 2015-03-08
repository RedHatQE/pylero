# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals
import pylarion.base_polarion as bp
import pylarion.enum_option_id as eoi


class SignatureData(bp.BasePolarion):
    '''Container for the "tns4:SignatureData type'''
    _cls_suds_map = {"target_status_id": "targetStatusId",
                     "verdict": {"field_name": "verdict",
                                 "cls": eoi.EnumOptionId}}
    _obj_client = "builder_client"
    _obj_struct = "tns5:SignatureData"
