# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals
from pylarion.base_polarion import BasePolarion


class PriorityOptionId(BasePolarion):
    """Object to handle the Polarion WSDL tns5:PriorityOptionId class

    Attributes:
        id (string)
"""
    _cls_suds_map = {"id": "id",
                     "uri": "_uri",
                     "_unresolved": "_unresolved"}
    _obj_client = "builder_client"
    _obj_struct = "tns5:PriorityOptionId"


class ArrayOfPriorityOptionId(BasePolarion):
    _obj_client = "builder_client"
    _obj_struct = "tns5:ArrayOfPriorityOptionId"
