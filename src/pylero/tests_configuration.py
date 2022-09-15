# -*- coding: utf8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from pylero.base_polarion import BasePolarion
from pylero.properties import Properties


class TestsConfiguration(BasePolarion):
    """Object to handle the Polarion WSDL tns3:TestsConfiguration class

    Attributes:
        defect_auto_assignement_enabled (boolean)
        defect_reuse_type (string)
        defect_template (string)
        defect_to_test_case_link_role_id (string)
        defect_work_item_type (string)
        defects_project (string)
        fields_to_copy_from_test_case_to_defect (Properties)
        fields_to_copy_from_test_run_to_linked_defect (Properties)
        fields_to_copy_from_test_run_to_new_defect (Properties)
        max_created_defects (int)
        max_created_defects_percent (int)
        result_error_enum_id (string)
        result_failed_enum_id (string)
        result_passed_enum_id (string)
        retest_allowed (boolean)
        status_error_enum_id (string)
        status_failed_enum_id (string)
        status_ok_enum_id (string)
        summary_defect_severity (string)
        test_case_id_custom_field (string)
        test_case_template (string)
        test_case_test_comment_field_id (string)
        test_case_test_result_field_id (string)
        test_case_work_item_type (string)
        test_run_template (string)"""

    _cls_suds_map = {
        "defect_auto_assignement_enabled": "defectAutoAssignementEnabled",
        "defect_reuse_type": "defectReuseType",
        "defect_template": "defectTemplate",
        "defect_to_test_case_link_role_id": "defectToTestCaseLinkRoleId",
        "defect_work_item_type": "defectWorkItemType",
        "defects_project": "defectsProject",
        "fields_to_copy_from_test_case_to_defect": {
            "field_name": "fieldsToCopyFromTestCaseToDefect",
            "cls": Properties,
        },
        "fields_to_copy_from_test_run_to_linked_defect": {
            "field_name": "fieldsToCopyFromTestRunToLinkedDefect",
            "cls": Properties,
        },
        "fields_to_copy_from_test_run_to_new_defect": {
            "field_name": "fieldsToCopyFromTestRunToNewDefect",
            "cls": Properties,
        },
        "max_created_defects": "maxCreatedDefects",
        "max_created_defects_percent": "maxCreatedDefectsPercent",
        "result_error_enum_id": "resultErrorEnumId",
        "result_failed_enum_id": "resultFailedEnumId",
        "result_passed_enum_id": "resultPassedEnumId",
        "retest_allowed": "retestAllowed",
        "status_error_enum_id": "statusErrorEnumId",
        "status_failed_enum_id": "statusFailedEnumId",
        "status_ok_enum_id": "statusOkEnumId",
        "summary_defect_severity": "summaryDefectSeverity",
        "test_case_id_custom_field": "testCaseIdCustomField",
        "test_case_template": "testCaseTemplate",
        "test_case_test_comment_field_id": "testCaseTestCommentFieldId",
        "test_case_test_result_field_id": "testCaseTestResultFieldId",
        "test_case_work_item_type": "testCaseWorkItemType",
        "test_run_template": "testRunTemplate",
        "uri": "_uri",
        "_unresolved": "_unresolved",
    }
    _obj_client = "test_management_client"
    _obj_struct = "tns3:TestsConfiguration"
