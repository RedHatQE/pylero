# -*- coding: utf8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from pylero.base_polarion import BasePolarion
from pylero.text import Text


class TimePoint(BasePolarion):
    """Object to handle the Polarion WSDL tns5:TimePoint class

    Attributes:
        closed (boolean)
        description (Text)
        earliest_planned_start (date)
        time_point_id (string)
        name (string)
        time (date)
"""
    _cls_suds_map = {"closed": "closed",
                     "description":
                     {"field_name": "description",
                      "cls": Text},
                     "earliest_planned_start": "earliestPlannedStart",
                     "time_point_id": "id",
                     "name": "name",
                     "time": "time",
                     "uri": "_uri",
                     "_unresolved": "_unresolved"}
    _obj_client = "builder_client"
    _obj_struct = "tns5:TimePoint"
