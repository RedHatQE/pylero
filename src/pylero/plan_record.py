# -*- coding: utf8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from pylero.base_polarion import BasePolarion
from pylero.work_item import _WorkItem


class PlanRecord(BasePolarion):
    """Object to handle the Polarion WSDL tns6:PlanRecord class

    Attributes:
        item (_WorkItem)
"""
    _cls_suds_map = {"item":
                     {"field_name": "item",
                      "cls": _WorkItem},
                     "uri": "_uri",
                     "_unresolved": "_unresolved"}
    _obj_client = "builder_client"
    _obj_struct = "tns6:PlanRecord"


class ArrayOfPlanRecord(BasePolarion):
    _obj_client = "builder_client"
    _obj_struct = "tns6:ArrayOfPlanRecord"
