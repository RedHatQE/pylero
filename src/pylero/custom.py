# -*- coding: utf8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from pylero.base_polarion import BasePolarion
from pylero.enum_option_id import EnumOptionId


class Custom(BasePolarion):
    """Object to manage Polarion TestManagement WS tns4:Custom

    Attributes:
        key (string)
        value (EnumOptionId)
"""
    _cls_suds_map = {"key": "key",
                     "value":
                     {"field_name": "value",
                      "cls": EnumOptionId}
                     }
    _obj_client = "test_management_client"
    _obj_struct = "tns4:Custom"

    def __init__(self, key=None, value=None, suds_object=None):
        super(self.__class__, self).__init__(None, suds_object)
        if key:
            self.key = key
            self.value = value


class ArrayOfCustom(BasePolarion):
    _obj_client = "test_management_client"
    _obj_struct = "tns4:ArrayOfCustom"
