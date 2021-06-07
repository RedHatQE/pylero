# -*- coding: utf8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from pylero.base_polarion import BasePolarion
from pylero.enum_option_id import EnumOptionId
from pylero.test_run_attachment import ArrayOfTestRunAttachment
from pylero.test_run_attachment import TestRunAttachment
from pylero.text import Text


class TestStepResult(BasePolarion):
    """Object to handle the Polarion WSDL tns3:TestStepResult class

    Attributes:
        attachments (ArrayOfTestRunAttachment)
        comment (Text)
        result (EnumOptionId)
"""
    _cls_suds_map = {"attachments":
                     {"field_name": "attachments",
                      "is_array": True,
                      "cls": TestRunAttachment,
                      "arr_cls": ArrayOfTestRunAttachment,
                      "inner_field_name": "TestRunAttachment"},
                     "comment":
                     {"field_name": "comment",
                      "cls": Text},
                     "result":
                     {"field_name": "result",
                      "cls": EnumOptionId,
                      "enum_id": "testing/test-result"},
                     "uri": "_uri",
                     "_unresolved": "_unresolved"}
    _obj_client = "test_management_client"
    _obj_struct = "tns3:TestStepResult"


class ArrayOfTestStepResult(BasePolarion):
    _obj_client = "test_management_client"
    _obj_struct = "tns3:ArrayOfTestStepResult"
