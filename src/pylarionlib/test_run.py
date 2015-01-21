# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from .abstract_polarion_persistent_object import AbstractPolarionPersistentObject

class TestRun(AbstractPolarionPersistentObject):

    emptyTemplate = 'Empty'

    class Status():
        ''' Values for a TestRun's status '''
        NOT_RUN     = "notrun"
        IN_PROGRESS = "inprogress"
        FINISHED    = "finished"


    def __init__(self, session, project=None, status=None):
        AbstractPolarionPersistentObject.__init__(self, session)
        self.project = project
        self.status = status


    def _copy(self, another):
        AbstractPolarionPersistentObject._copy(self, another)
        another.project = self.project
        another.status = self.status
        return another


    def _fillMissingValues(self, project=None, namespace=None):
        super(TestRun, self)._fillMissingValues(project, namespace)
        if project:
            self.project = project
        if not self.project:
            self.project = self.session._getDefaultProject()
        if not self.status:
            self.status = TestRun.Status.NOT_RUN
        return self


    @classmethod
    def _isConvertible(cls, sudsObject):
        if not AbstractPolarionPersistentObject._isConvertible(sudsObject):
            return False
        # TODO: check all the attributes
        return True


    @classmethod
    def _mapFromSUDS(cls, session, sudsObject):
        # TODO: sanity checks
        if SimpleTestRun._isConvertible(sudsObject):
            return SimpleTestRun._mapFromSUDS(session, sudsObject)
        else:
            # Fall back: Not SimpleTestRun, just a standard Polarion's TestRun
            testRun = TestRun(session)
            TestRun._mapSpecificAttributesFromSUDS(sudsObject, testRun)
            return testRun


    def _mapToSUDS(self):
        sudsObject = self.session.testManagementClient.factory.create('tns3:TestRun')
        TestRun._mapSpecificAttributesToSUDS(self, sudsObject)
        return sudsObject


    @classmethod
    def _mapSpecificAttributesToSUDS(cls, testRun, sudsObject):

        AbstractPolarionPersistentObject._mapSpecificAttributesToSUDS(testRun, sudsObject)

        session = testRun.session

        sudsObject.projectURI = session.projectClient.service.getProject(testRun.project)._uri

        sudsObject.status = session.testManagementClient.factory.create('tns4:EnumOptionId')
        sudsObject.status.id = testRun.status


    @classmethod
    def _mapSpecificAttributesFromSUDS(cls, sudsObject, testRun):

        AbstractPolarionPersistentObject._mapSpecificAttributesFromSUDS(sudsObject, testRun)

        session = testRun.session

        testRun.project = session.projectClient.service.getProjectByURI(sudsObject.projectURI).id
        testRun.status = sudsObject.status.id


    def _crudCreate(self, project=None):

        self._fillMissingValues(project)

        # By Polarion's design, we store the test run in two steps:
        # create and update.

        uri = self.session.testManagementClient.service.createTestRun(self.project, self.pid, self.emptyTemplate)
        uri = '{}'.format(uri)  # work around Text jumping in sometimes
        sudsObject = self.session.testManagementClient.service.getTestRunByUri(uri)
        stub = self.__class__._mapFromSUDS(self.session, sudsObject)

        temp = (self.status, None) # use a tuple, over time there will be more attributes here

        stub._copy(self)
        self.status = temp[0]

        return self._crudUpdate()


    def _crudRetrieve(self):
        if not self.puri:
            raise PylarionLibException('Current object has no URI, cannot retrieve data')
        sudsObject = self.session.testManagementClient.service.getTestRunByUri(self.puri)
        temp = self.__class__._mapFromSUDS(self.session, sudsObject)
        temp._copy(self)
        return self


    def _crudUpdate(self):
        if not self.puri:
            raise PylarionLibException('Current object has no URI, cannot update data')
        self._fillMissingValues()
        sudsObject = self._mapToSUDS()
        self.session.testManagementClient.service.updateTestRun(sudsObject)
        return self._crudRetrieve()


    def _crudDelete(self):
        raise PylarionLibException('Not implemented')


from .exceptions import PylarionLibException
from .simple_test_run import SimpleTestRun
