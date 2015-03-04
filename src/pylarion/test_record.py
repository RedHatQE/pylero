# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals
import pylarion.base_polarion as bp
import pylarion.text as t
from pylarion.test_run_attachment import TestRunAttachment
from pylarion.test_run_attachment import ArrayOfTestRunAttachment
from pylarion.test_step_result import TestStepResult
from pylarion.test_step_result import ArrayOfTestStepResult
import pylarion.enum_option_id as eoi
import pylarion.work_item as wi
import pylarion.user as u
from pylarion.exceptions import PylarionLibException


class TestRecord(bp.BasePolarion):
    '''An object to contain the'tns3:TestRecord' ''' \
        '''of the TestManagement service '''

    _cls_suds_map = {"attachments": {"field_name": "attachments",
                                     "is_array": True,
                                     "cls": TestRunAttachment,
                                     "arr_cls": ArrayOfTestRunAttachment,
                                     "inner_field_name": "TestRunAttachment"},
                     "comment": {"field_name": "comment", 'cls': t.Text},
                     "defect_case_id": {"field_name": "defectURI",
                                        "cls": wi._WorkItem,
                                        "named_arg": "uri",
                                        "sync_field": "uri"},
                     "duration": "duration",
                     "executed": "executed",
                     "executed_by": {"field_name": "executedByURI",
                                     "cls": u.User, "named_arg": "uri",
                                     "sync_field": "uri"},
                     "result": {"field_name": "result",
                                "cls": eoi.EnumTestResult},
                     "test_case_id": {"field_name": "testCaseURI",
                                      "cls": wi._WorkItem, "named_arg": "uri",
                                      "sync_field": "uri"},
                     "test_case_revision": "testCaseRevision",
                     "test_step_results": {"field_name": "testStepResults",
                                           "is_array": True,
                                           "cls": TestStepResult,
                                           "arr_cls": ArrayOfTestStepResult,
                                           "inner_field_name": "TestStepResult"
                                           }}
    _obj_client = "test_management_client"
    _obj_struct = "tns3:TestRecord"

    def __init__(self, project_id=None, test_case_id=None, suds_object=None):
        if not suds_object and not project_id:
            raise PylarionLibException("If the suds_object is not passed in,"
                                       " then project id must be")
        self.project_id = project_id
        super(self.__class__, self).__init__(None, suds_object)
        if test_case_id:
            self.test_case_uri = wi._WorkItem(test_case_id,
                                              project_id=project_id).uri

    def _fix_circular_refs(self):
        # need to pass in the project_id parm to the Work Item,
        # but it is not given before instatiation
        self._cls_suds_map["test_case_id"]["additional_parms"] = \
            {"project_id": self.project_id}
        self._cls_suds_map["defect_case_id"]["additional_parms"] = \
            {"project_id": self.project_id}


class ArrayOfTestRecord(bp.BasePolarion):
    _obj_client = "test_management_client"
    _obj_struct = "tns3:ArrayOfTestRecord"
