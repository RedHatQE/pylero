# -*- coding: utf8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from pylero.base_polarion import BasePolarion
from pylero.properties import Properties


class EnumOption(BasePolarion):
    """Object to handle the Polarion WSDL tns5:EnumOption class

    Attributes:
        default (boolean)
        enum_id (string)
        hidden (boolean)
        enum_option_id (string)
        name (string)
        phantom (boolean)
        properties (Properties)
        sequence_number (int)"""

    _cls_suds_map = {
        "default": "default",
        "enum_id": "enumId",
        "hidden": "hidden",
        "enum_option_id": "id",
        "name": "name",
        "phantom": "phantom",
        "properties": {"field_name": "properties", "cls": Properties},
        "sequence_number": "sequenceNumber",
        "uri": "_uri",
        "_unresolved": "_unresolved",
    }
    _obj_client = "builder_client"
    _obj_struct = "tns5:EnumOption"
