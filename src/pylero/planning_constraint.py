# -*- coding: utf8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from pylero.base_polarion import BasePolarion
from pylero.enum_option_id import EnumOptionId


class PlanningConstraint(BasePolarion):
    """Object to handle the Polarion WSDL tns5:PlanningConstraint class

    Attributes:
        constraint (EnumOptionId)
        date (dateTime)"""

    _cls_suds_map = {
        "constraint": {"field_name": "constraint", "cls": EnumOptionId},
        "date": "date",
        "uri": "_uri",
        "_unresolved": "_unresolved",
    }
    _obj_client = "builder_client"
    _obj_struct = "tns5:PlanningConstraint"


class ArrayOfPlanningConstraint(BasePolarion):
    _obj_client = "builder_client"
    _obj_struct = "tns5:ArrayOfPlanningConstraint"
