# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals
import pylarion.base_polarion as bp
import pylarion.work_item as wi


class PlanRecord(bp.BasePolarion):
    """Object to handle the Polarion WSDL tns6:PlanRecord class

    Attributes (for specific details, see Polarion):
        item (_WorkItem)
"""
    _cls_suds_map = {"item": {"field_name": "item", "cls": wi._WorkItem},
                     "uri": "_uri",
                     "_unresolved": "_unresolved"}
    _obj_client = "builder_client"
    _obj_struct = "tns6:PlanRecord"


class ArrayOfPlanRecord(bp.BasePolarion):
    _obj_client = "builder_client"
    _obj_struct = "tns6:ArrayOfPlanRecord"
