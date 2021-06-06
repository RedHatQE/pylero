# -*- coding: utf8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from pylero.base_polarion import BasePolarion
from pylero.enum_option_id import EnumOptionId


class SignatureData(BasePolarion):
    """Object to handle the Polarion WSDL tns5:SignatureData class

    Attributes:
        target_status_id (string)
        verdict (EnumOptionId)
"""
    _cls_suds_map = {"target_status_id": "targetStatusId",
                     "verdict":
                     {"field_name": "verdict",
                      "cls": EnumOptionId}}
    _obj_client = "builder_client"
    _obj_struct = "tns5:SignatureData"
