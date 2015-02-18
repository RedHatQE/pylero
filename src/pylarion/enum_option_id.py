# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals
import pylarion.base_polarion as bp


class EnumOptionId(bp.BasePolarion):
    """An object to manage Polarion TestManagement tns4:EnumOptionId"""
    _cls_suds_map = {"id": "id"}
    _id_field = "id"
    _obj_client = "test_management_client"
    _obj_struct = "tns4:EnumOptionId"


class ArrayOfEnumOptionId(bp.BasePolarion):
    """An object to manage Polarion TestManagement tns4:ArrayOfEnumOptionId"""
    _obj_client = "test_management_client"
    _obj_struct = "tns4:ArrayOfEnumOptionId"


# TODO undestand if all below subclasses can be used as a form of enum so that
# only valid valuescan be passed in for their EnumOptionId field.
# Look at Polarion documentation for functions that return specific options to
# determine if these classes should be self-generated or other way to implement
class EnumTestResult(EnumOptionId):
    ''' Values for a TestRecord's result '''
    PASSED = 'passed'
    FAILED = 'failed'
    BLOCKED = 'blocked'


class EnumTestRunStatus(EnumOptionId):
    ''' Values for a TestRun's status '''
    NOT_RUN = "notrun"
    IN_PROGRESS = "inprogress"
    FINISHED = "finished"


class EnumTestRunTypes(EnumOptionId):
    """Possible values for a TestRun type"""
    MANUAL = "manual"
    AUTOMATED = "automated"


class EnumSelectTestCasesBy(EnumOptionId):
    AUTOMATED_PROCESS = "automatedProcess"
    DYNAMIC_QUERY = "dynamicQueryResult"
    DYNAMIC_LIVEDOC = "dynamicLiveDoc"
    MANUAL_SELECTION = "manualSelection"
    STATIC_QUERY = "staticQueryResult"
    STATIC_LIVEDOC = "staticLiveDoc"


class TestType(EnumOptionId):
    REGRESSION = "regression"