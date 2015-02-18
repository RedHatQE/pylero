# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals
import pylarion.base_polarion as bp
import pylarion.enum_option_id as eoi
from pylarion.test_step import TestStep
from pylarion.test_step import ArrayOfTestStep


class TestSteps(bp.BasePolarion):
    """Object to handle the Polarion WSDL tns3:TestSteps class

    Attributes (for specific details, see Polarion):
        keys (ArrayOfeoi.EnumOptionId)
        steps (ArrayOfTestStep)
"""
    _cls_suds_map = {"keys": {"field_name": "keys",
                              "is_array": True,
                              "cls": eoi.EnumOptionId,
                              "arr_cls": eoi.ArrayOfEnumOptionId,
                              "inner_field_name": "eoi.EnumOptionId"},
                     "steps": {"field_name": "steps",
                               "is_array": True,
                               "cls": TestStep,
                               "arr_cls": ArrayOfTestStep,
                               "inner_field_name": "TestStep"},
                     "uri": "_uri",
                     "_unresolved": "_unresolved"}
    _obj_client = "test_management_client"
    _obj_struct = "tns3:TestSteps"
