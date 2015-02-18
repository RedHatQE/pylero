# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals
import pylarion.base_polarion as bp
import pylarion.enum_option_id as eoi
import pylarion.user as u


class Approval(bp.BasePolarion):
    """Object to handle the Polarion WSDL tns5:Approval class

    Attributes (for specific details, see Polarion):
        status (eoi.EnumOptionId)
        user (User)
"""
    _cls_suds_map = {"status": {"field_name": "status",
                                "cls": eoi.EnumOptionId},
                     "user": {"field_name": "user", "cls": u.User},
                     "uri": "_uri",
                     "_unresolved": "_unresolved"}
    _obj_client = "builder_client"
    _obj_struct = "tns5:Approval"


class ArrayOfApproval(bp.BasePolarion):
    _obj_client = "builder_client"
    _obj_struct = "tns5:ArrayOfApproval"
