# -*- coding: utf8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from pylero.base_polarion import BasePolarion
from pylero.enum_option_id import EnumOptionId
from pylero.user import User


class Approval(BasePolarion):
    """Object to handle the Polarion WSDL tns5:Approval class

    Attributes:
        status (EnumOptionId)
        user (User)
"""
    _cls_suds_map = {
        "status":
            {"field_name": "status",
             "cls": EnumOptionId,
             "enum_id": "approval-status"},
        "user_id":
            {"field_name": "user",
             "cls": User},
        "uri": "_uri",
        "_unresolved": "_unresolved"}
    _obj_client = "builder_client"
    _obj_struct = "tns5:Approval"


class ArrayOfApproval(BasePolarion):
    _obj_client = "builder_client"
    _obj_struct = "tns5:ArrayOfApproval"
