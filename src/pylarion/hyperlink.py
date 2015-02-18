# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals
import pylarion.base_polarion as bp
import pylarion.enum_option_id as eoi


class Hyperlink(bp.BasePolarion):
    """Object to handle the Polarion WSDL tns5:Hyperlink class

    Attributes (for specific details, see Polarion):
        role (eoi.EnumOptionId)
        uri (string)
"""
    _cls_suds_map = {"role": {"field_name": "role", "cls": eoi.EnumOptionId},
                     "uri": "uri",
                     "uri": "_uri",
                     "_unresolved": "_unresolved"}
    _obj_client = "builder_client"
    _obj_struct = "tns5:Hyperlink"


class ArrayOfHyperlink(bp.BasePolarion):
    _obj_client = "builder_client"
    _obj_struct = "tns5:ArrayOfHyperlink"
