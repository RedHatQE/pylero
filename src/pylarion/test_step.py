# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals
import pylarion.base_polarion as bp
import pylarion.text as t


class TestStep(bp.BasePolarion):
    """Object to handle the Polarion WSDL tns3:TestStep class

    Attributes (for specific details, see Polarion):
        values (ArrayOfText)
"""
    _cls_suds_map = {"values": {"field_name": "values",
                                "is_array": True,
                                "cls": t.Text,
                                "arr_cls": t.ArrayOfText,
                                "inner_field_name": "Text"},
                     "uri": "_uri",
                     "_unresolved": "_unresolved"}
    _obj_client = "test_management_client"
    _obj_struct = "tns3:TestStep"


class ArrayOfTestStep(bp.BasePolarion):
    _obj_client = "test_management_client"
    _obj_struct = "tns3:ArrayOfTestStep"
