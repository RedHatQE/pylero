# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals
import pylarion.base_polarion as bp


class PriorityOptionId(bp.BasePolarion):
    """Object to handle the Polarion WSDL tns5:PriorityOptionId class

    Attributes (for specific details, see Polarion):
        id (string)
"""
    _cls_suds_map = {"id": "id",
                     "uri": "_uri",
                     "_unresolved": "_unresolved"}
    _obj_client = "builder_client"
    _obj_struct = "tns5:PriorityOptionId"


class ArrayOfPriorityOptionId(bp.BasePolarion):
    _obj_client = "builder_client"
    _obj_struct = "tns5:ArrayOfPriorityOptionId"
