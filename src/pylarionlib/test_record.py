# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import suds.sax

from .abstract_polarion_crate import AbstractPolarionCrate

class TestRecord(AbstractPolarionCrate):
    ''' A crate to deal with 'tns3:TestRecord' of the TestManagement service '''


    class Status():
        ''' Values for a TestRecord's result '''
        PASSED  = 'passed'
        FAILED  = 'failed'
        BLOCKED = 'blocked'


    def __init__(self, session, testCaseURI=None):
        AbstractPolarionCrate.__init__(self, session)
        self.testCaseURI = testCaseURI
        self.result = None
        self.comment = None
        self.executed = None  # datetime
        self.duration = None  # float point number (seconds)
        self._fillMissingValues()


    def _copy(self, another):
        AbstractPolarionCrate._copy(self, another)
        another.testCaseURI = self.testCaseURI
        another.result = self.result
        another.comment = self.comment
        another.executed = self.executed
        another.duration = self.duration
        return another


    def _fillMissingValues(self, project=None, namespace=None):
        super(TestRecord, self)._fillMissingValues(project, namespace)
        # none?
        return self


    @classmethod
    def _isConvertible(cls, suds_object):
        if suds_object == None:
            return False
        # TODO: verify with WSDLs if some attributes could be omitted
        return True


    @classmethod
    def _mapSpecificAttributesToSUDS(cls, testRecord, suds_object):

        session = testRecord.session

        suds_object.testCaseURI = testRecord.testCaseURI

        if testRecord.result:
            suds_object.result = session.test_management_client.factory.create('tns4:EnumOptionId')
            suds_object.result.id = testRecord.result

        if testRecord.comment:
            suds_object.comment = testRecord.comment._mapToSUDS()

        if testRecord.executed:
            suds_object.executed = suds.sax.date.DateTime(testRecord.executed)

        suds_object.duration = testRecord.duration


    @classmethod
    def _mapSpecificAttributesFromSUDS(cls, suds_object, testRecord):

        session = testRecord.session

        testRecord.testCaseURI = suds_object.testCaseURI

        testRecord.result = None
        if hasattr(suds_object, 'result'):
            if hasattr(suds_object.result, 'id'):
                testRecord.result = suds_object.result.id

        testRecord.comment = None
        if hasattr(suds_object, 'comment'):
            if suds_object.comment:
                testRecord.comment = TestManagementText(session)
                TestManagementText._mapSpecificAttributesFromSUDS(suds_object.comment, testRecord.comment)

        testRecord.executed = None
        if hasattr(suds_object, 'executed'):
            if suds_object.executed:
                testRecord.executed = suds_object.executed

        testRecord.duration = None
        if hasattr(suds_object, 'duration'):
            testRecord.duration = suds_object.duration


    def _mapToSUDS(self):
        sudsObject = self.session.test_management_client.factory.create('tns3:TestRecord')
        TestRecord._mapSpecificAttributesToSUDS(self, sudsObject)
        return sudsObject


    @classmethod
    def _mapFromSUDS(cls, session, suds_object):
        testRecord = TestRecord(session)
        TestRecord._mapSpecificAttributesFromSUDS(suds_object, testRecord)
        return testRecord


from pylarionlib.test_management_text import TestManagementText
