# -*- coding: utf8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from pylero.base_polarion import BasePolarion
from pylero.enum_option_id import EnumOptionId
from pylero.test_run_attachment import ArrayOfTestRunAttachment
from pylero.test_run_attachment import TestRunAttachment
from pylero.test_step_result import ArrayOfTestStepResult
from pylero.test_step_result import TestStepResult
from pylero.text import Text
from pylero.user import User
from pylero.work_item import _WorkItem


class TestRecord(BasePolarion):
    """Object to handle the Polarion WSDL tns3:TestRecord class

    Attributes (for specific details, see Polarion):
        attachments (ArrayOfTestRunAttachment)
        comment (Text)
        defect_case_id (string)
        duration (float)
        executed (dateTime)
        executed_by (string)
        result (EnumOptionId)
        test_case_revision (string)
        test_case_id (string)
        test_step_results (ArrayOfTestStepResult)"""

    _cls_suds_map = {
        "attachments": {
            "field_name": "attachments",
            "is_array": True,
            "cls": TestRunAttachment,
            "arr_cls": ArrayOfTestRunAttachment,
            "inner_field_name": "TestRunAttachment",
        },
        "comment": {"field_name": "comment", "cls": Text},
        "defect_case_id": {
            "field_name": "defectURI",
            "cls": _WorkItem,
            "named_arg": "uri",
            "sync_field": "uri",
        },
        "duration": "duration",
        "executed": "executed",
        "executed_by": {
            "field_name": "executedByURI",
            "cls": User,
            "named_arg": "uri",
            "sync_field": "uri",
        },
        "result": {"field_name": "result", "cls": EnumOptionId, "enum_id": "result"},
        "test_case_id": {
            "field_name": "testCaseURI",
            "cls": _WorkItem,
            "named_arg": "uri",
            "sync_field": "uri",
        },
        "test_case_revision": "testCaseRevision",
        "test_step_results": {
            "field_name": "testStepResults",
            "is_array": True,
            "cls": TestStepResult,
            "arr_cls": ArrayOfTestStepResult,
            "inner_field_name": "TestStepResult",
        },
    }
    _obj_client = "test_management_client"
    _obj_struct = "tns3:TestRecord"
    _id_field = "test_case_id"

    def __init__(self, project_id=None, test_case_id=None, suds_object=None):
        self.project_id = project_id if project_id else self.default_project
        super(self.__class__, self).__init__(test_case_id, suds_object)

    def _fix_circular_refs(self):
        # need to pass in the project_id parm to the Work Item,
        # but it is not given before instatiation
        self._cls_suds_map["test_case_id"]["additional_parms"] = {
            "project_id": self.project_id
        }
        self._cls_suds_map["defect_case_id"]["additional_parms"] = {
            "project_id": self.project_id
        }


class ArrayOfTestRecord(BasePolarion):
    _obj_client = "test_management_client"
    _obj_struct = "tns3:ArrayOfTestRecord"
