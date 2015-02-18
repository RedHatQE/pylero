# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals
import pylarion.base_polarion as bp
import pylarion.properties as prop


class PriorityOpt(bp.BasePolarion):
    """Object to handle the Polarion WSDL tns5:PriorityOpt class

    Attributes (for specific details, see Polarion):
        default (boolean)
        enum_id (string)
        float (float)
        hidden (boolean)
        priority_opt_id (string)
        name (string)
        phantom (boolean)
        properties (Properties)
        sequence_number (int)
"""
    _cls_suds_map = {"default": "default",
                     "enum_id": "enumId",
                     "float": "float",
                     "hidden": "hidden",
                     "priority_opt_id": "id",
                     "name": "name",
                     "phantom": "phantom",
                     "properties": {"field_name": "properties",
                                    "cls": prop.Properties},
                     "sequence_number": "sequenceNumber",
                     "uri": "_uri",
                     "_unresolved": "_unresolved"}
    _obj_client = "builder_client"
    _obj_struct = "tns5:PriorityOpt"
