# -*- coding: utf8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from pylero.base_polarion import BasePolarion
from pylero.properties import Properties


class PriorityOpt(BasePolarion):
    """Object to handle the Polarion WSDL tns5:PriorityOpt class

    Attributes:
        default (boolean)
        enum_id (string)
        float (float)
        hidden (boolean)
        priority_opt_id (string)
        name (string)
        phantom (boolean)
        properties (Properties)
        sequence_number (int)"""

    _cls_suds_map = {
        "default": "default",
        "enum_id": "enumId",
        "float": "float",
        "hidden": "hidden",
        "priority_opt_id": "id",
        "name": "name",
        "phantom": "phantom",
        "properties": {"field_name": "properties", "cls": Properties},
        "sequence_number": "sequenceNumber",
        "uri": "_uri",
        "_unresolved": "_unresolved",
    }
    _obj_client = "builder_client"
    _obj_struct = "tns5:PriorityOpt"
