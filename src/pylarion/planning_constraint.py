# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals
import pylarion.base_polarion as bp
import pylarion.enum_option_id as eoi


class PlanningConstraint(bp.BasePolarion):
    """Object to handle the Polarion WSDL tns5:PlanningConstraint class

    Attributes (for specific details, see Polarion):
        constraint (eoi.EnumOptionId)
        date (dateTime)
"""
    _cls_suds_map = {"constraint": {"field_name": "constraint",
                                    "cls": eoi.EnumOptionId},
                     "date": "date",
                     "uri": "_uri",
                     "_unresolved": "_unresolved"}
    _obj_client = "builder_client"
    _obj_struct = "tns5:PlanningConstraint"


class ArrayOfPlanningConstraint(bp.BasePolarion):
    _obj_client = "builder_client"
    _obj_struct = "tns5:ArrayOfPlanningConstraint"
