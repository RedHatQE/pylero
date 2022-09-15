# -*- coding: utf8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from pylero.base_polarion import BasePolarion
from pylero.enum_option_id import ArrayOfEnumOptionId
from pylero.enum_option_id import EnumOptionId
from pylero.test_step import ArrayOfTestStep
from pylero.test_step import TestStep


class TestSteps(BasePolarion):
    """Object to handle the Polarion WSDL tns3:TestSteps class

    Attributes:
        keys (ArrayOfEnumOptionId)
        steps (ArrayOfTestStep)"""

    _cls_suds_map = {
        "keys": {
            "field_name": "keys",
            "is_array": True,
            "cls": EnumOptionId,
            "arr_cls": ArrayOfEnumOptionId,
            "inner_field_name": "EnumOptionId",
            "enum_id": "testing/test-step-keys",
        },
        "steps": {
            "field_name": "steps",
            "is_array": True,
            "cls": TestStep,
            "arr_cls": ArrayOfTestStep,
            "inner_field_name": "TestStep",
        },
        "uri": "_uri",
        "_unresolved": "_unresolved",
    }
    _obj_client = "test_management_client"
    _obj_struct = "tns3:TestSteps"
