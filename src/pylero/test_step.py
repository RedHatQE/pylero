# -*- coding: utf8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from pylero.base_polarion import BasePolarion
from pylero.text import ArrayOfText
from pylero.text import Text


class TestStep(BasePolarion):
    """Object to handle the Polarion WSDL tns3:TestStep class

    Attributes:
        values (ArrayOfText)
"""
    _cls_suds_map = {
        "values":
            {"field_name": "values",
             "is_array": True,
             "cls": Text,
             "arr_cls": ArrayOfText,
             "inner_field_name": "Text"}}
    _obj_client = "test_management_client"
    _obj_struct = "tns3:TestStep"


class ArrayOfTestStep(BasePolarion):
    _obj_client = "test_management_client"
    _obj_struct = "tns3:ArrayOfTestStep"
