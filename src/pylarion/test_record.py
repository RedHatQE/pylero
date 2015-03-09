# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals
from pylarion.base_polarion import BasePolarion
from pylarion.text import Text
from pylarion.test_run_attachment import TestRunAttachment
from pylarion.test_run_attachment import ArrayOfTestRunAttachment
from pylarion.test_step_result import TestStepResult
from pylarion.test_step_result import ArrayOfTestStepResult
from pylarion.enum_option_id import EnumOptionId
from pylarion.work_item import _WorkItem
from pylarion.user import User


class TestRecord(BasePolarion):
    '''An object to contain the'tns3:TestRecord' ''' \
        '''of the TestManagement service '''

    _cls_suds_map = {"attachments":
                     {"field_name": "attachments",
                      "is_array": True,
                      "cls": TestRunAttachment,
                      "arr_cls": ArrayOfTestRunAttachment,
                      "inner_field_name": "TestRunAttachment"},
                     "comment":
                     {"field_name": "comment",
                      'cls': Text},
                     "defect_case_id":
                     {"field_name": "defectURI",
                      "cls": _WorkItem,
                      "named_arg": "uri",
                      "sync_field": "uri"},
                     "duration": "duration",
                     "executed": "executed",
                     "executed_by":
                     {"field_name": "executedByURI",
                      "cls": User,
                      "named_arg": "uri",
                      "sync_field": "uri"},
                     "result":
                     {"field_name": "result",
                      "cls": EnumOptionId},
                     "test_case_id":
                     {"field_name": "testCaseURI",
                      "cls": _WorkItem,
                      "named_arg": "uri",
                      "sync_field": "uri"},
                     "test_case_revision": "testCaseRevision",
                     "test_step_results":
                     {"field_name": "testStepResults",
                      "is_array": True,
                      "cls": TestStepResult,
                      "arr_cls": ArrayOfTestStepResult,
                      "inner_field_name": "TestStepResult"}}
    _obj_client = "test_management_client"
    _obj_struct = "tns3:TestRecord"

    def __init__(self, project_id=None, test_case_id=None, suds_object=None):
        self.project_id = project_id if project_id else self.default_project
        super(self.__class__, self).__init__(None, suds_object)
        if test_case_id:
            self.test_case_uri = _WorkItem(test_case_id,
                                           project_id=self.project_id).uri

    def _fix_circular_refs(self):
        # need to pass in the project_id parm to the Work Item,
        # but it is not given before instatiation
        self._cls_suds_map["test_case_id"]["additional_parms"] = \
            {"project_id": self.project_id}
        self._cls_suds_map["defect_case_id"]["additional_parms"] = \
            {"project_id": self.project_id}


class ArrayOfTestRecord(BasePolarion):
    _obj_client = "test_management_client"
    _obj_struct = "tns3:ArrayOfTestRecord"
