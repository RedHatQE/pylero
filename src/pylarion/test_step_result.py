# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals
import pylarion.base_polarion as bp
import pylarion.test_run_attachment as tra
import pylarion.text as t
import pylarion.enum_option_id as eoi


class TestStepResult(bp.BasePolarion):
    """Object to handle the Polarion WSDL tns3:TestStepResult class

    Attributes (for specific details, see Polarion):
        attachments (ArrayOfTestRunAttachment)
        comment (Text)
        result (eoi.EnumOptionId)
"""
    _cls_suds_map = {"attachments": {"field_name": "attachments",
                                     "is_array": True,
                                     "cls": tra.TestRunAttachment,
                                     "arr_cls": tra.ArrayOfTestRunAttachment,
                                     "inner_field_name": "TestRunAttachment"},
                     "comment": {"field_name": "comment", "cls": t.Text},
                     "result": {"field_name": "result",
                                "cls": eoi.EnumOptionId},
                     "uri": "_uri",
                     "_unresolved": "_unresolved"}
    _obj_client = "test_management_client"
    _obj_struct = "tns3:TestStepResult"


class ArrayOfTestStepResult(bp.BasePolarion):
    _obj_client = "test_management_client"
    _obj_struct = "tns3:ArrayOfTestStepResult"
