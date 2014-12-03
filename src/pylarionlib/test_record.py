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


    def _equiv(self, other):
        if not other:
            return False
        if self.testCaseURI != other.testCaseURI:
            return False
        if self.result != other.result:
            return False
        if not TestManagementText._staticEquiv(self.comment, other.comment):
            return False
        if not self.executed and other.executed:
            return False
        if self.executed and not other.executed:
            return False
        if self.executed and other.executed:
            # For unknown reasons, datetime values stored and retrieved
            # from/to Plarion differ in milliseconds. Ignore that.
            delta = self.executed - other.executed
            deltaSec = abs(delta.total_seconds())
            if deltaSec > 1.0:
                return False
        if self.duration != other.duration:
            return False
        return True


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
    def _isConvertible(cls, sudsObject):
        if sudsObject == None:
            return False
        # TODO: verify with WSDLs if some attributes could be omitted
        return True


    @classmethod
    def _mapSpecificAttributesToSUDS(cls, testRecord, sudsObject):

        session = testRecord.session

        sudsObject.testCaseURI = testRecord.testCaseURI

        if testRecord.result:
            sudsObject.result = session.testManagementClient.factory.create('tns4:EnumOptionId')
            sudsObject.result.id = testRecord.result

        if testRecord.comment:
            sudsObject.comment = testRecord.comment._mapToSUDS()

        if testRecord.executed:
            sudsObject.executed = suds.sax.date.DateTime(testRecord.executed)

        sudsObject.duration = testRecord.duration


    @classmethod
    def _mapSpecificAttributesFromSUDS(cls, sudsObject, testRecord):

        session = testRecord.session

        testRecord.testCaseURI = sudsObject.testCaseURI

        testRecord.result = None
        if hasattr(sudsObject, 'result'):
            if hasattr(sudsObject.result, 'id'):
                testRecord.result = sudsObject.result.id

        testRecord.comment = None
        if hasattr(sudsObject, 'comment'):
            if sudsObject.comment:
                testRecord.comment = TestManagementText(session)
                TestManagementText._mapSpecificAttributesFromSUDS(sudsObject.comment, testRecord.comment)

        testRecord.executed = None
        if hasattr(sudsObject, 'executed'):
            if sudsObject.executed:
                testRecord.executed = sudsObject.executed

        testRecord.duration = None
        if hasattr(sudsObject, 'duration'):
            testRecord.duration = sudsObject.duration


    def _mapToSUDS(self):
        sudsObject = self.session.testManagementClient.factory.create('tns3:TestRecord')
        TestRecord._mapSpecificAttributesToSUDS(self, sudsObject)
        return sudsObject


    @classmethod
    def _mapFromSUDS(cls, session, sudsObject):
        testRecord = TestRecord(session)
        TestRecord._mapSpecificAttributesFromSUDS(sudsObject, testRecord)
        return testRecord


from pylarionlib.test_management_text import TestManagementText
