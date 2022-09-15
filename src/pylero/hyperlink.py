# -*- coding: utf8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from pylero.base_polarion import BasePolarion
from pylero.enum_option_id import EnumOptionId


class Hyperlink(BasePolarion):
    """Object to handle the Polarion WSDL tns5:Hyperlink class

    Attributes:
        role (EnumOptionId)
        uri (string)"""

    _cls_suds_map = {
        "role": {
            "field_name": "role",
            "cls": EnumOptionId,
            "enum_id": "hyperlink-role",
        },
        "uri": "uri",
    }
    _obj_client = "builder_client"
    _obj_struct = "tns5:Hyperlink"


class ArrayOfHyperlink(BasePolarion):
    _obj_client = "builder_client"
    _obj_struct = "tns5:ArrayOfHyperlink"
