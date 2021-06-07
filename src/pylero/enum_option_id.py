# -*- coding: utf8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from pylero.base_polarion import BasePolarion


class EnumOptionId(BasePolarion):
    """An object to manage Polarion TestManagement tns4:EnumOptionId"""
    _cls_suds_map = {"enum_id": "id"}
    _id_field = "enum_id"
    _obj_client = "test_management_client"
    _obj_struct = "tns4:EnumOptionId"

    def __init__(self, enum_id=None, suds_object=None):
        super(EnumOptionId, self).__init__(enum_id, suds_object)


class ArrayOfEnumOptionId(BasePolarion):
    """An object to manage Polarion TestManagement tns4:ArrayOfEnumOptionId"""
    _obj_client = "test_management_client"
    _obj_struct = "tns4:ArrayOfEnumOptionId"
    _cls_inner = EnumOptionId
