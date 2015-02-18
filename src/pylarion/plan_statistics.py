# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals
import pylarion.base_polarion as bp


class PlanStatistics(bp.BasePolarion):
    """Object to handle the Polarion WSDL tns3:PlanStatistics class

    Attributes (for specific details, see Polarion):
        done (float)
        done_as_string (string)
        ideal_progress (float)
        ideal_progress_as_string (string)
        number_of_planned (int)
        number_of_resolved (int)
        number_of_unresolved (int)
        planned (float)
        planned_as_string (string)
        progress (float)
        progress_as_string (string)
        todo (float)
        todo_as_string (string)
"""
    _cls_suds_map = {"done": "done",
                     "done_as_string": "doneAsString",
                     "ideal_progress": "idealProgress",
                     "ideal_progress_as_string": "idealProgressAsString",
                     "number_of_planned": "numberOfPlanned",
                     "number_of_resolved": "numberOfResolved",
                     "number_of_unresolved": "numberOfUnresolved",
                     "planned": "planned",
                     "planned_as_string": "plannedAsString",
                     "progress": "progress",
                     "progress_as_string": "progressAsString",
                     "todo": "todo",
                     "todo_as_string": "todoAsString",
                     "uri": "_uri",
                     "_unresolved": "_unresolved"}
    _obj_client = "planning_client"
    _obj_struct = "tns3:PlanStatistics"
