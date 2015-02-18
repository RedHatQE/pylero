# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals
import pylarion.base_polarion as bp
import pylarion.enum_option_id as eoi
import pylarion.user as u


class WorkRecord(bp.BasePolarion):
    """Object to handle the Polarion WSDL tns5:WorkRecord class

    Attributes (for specific details, see Polarion):
        comment (string)
        date (date)
        work_record_id (string)
        time_spent (duration)
        type (eoi.EnumOptionId)
        user (User)
"""
    _cls_suds_map = {"comment": "comment",
                     "date": "date",
                     "work_record_id": "id",
                     "time_spent": "timeSpent",
                     "type": {"field_name": "type", "cls": eoi.EnumOptionId},
                     "user": {"field_name": "user", "cls": u.User},
                     "uri": "_uri",
                     "_unresolved": "_unresolved"}
    _obj_client = "builder_client"
    _obj_struct = "tns5:WorkRecord"


class ArrayOfWorkRecord(bp.BasePolarion):
    _obj_client = "builder_client"
    _obj_struct = "tns5:ArrayOfWorkRecord"
