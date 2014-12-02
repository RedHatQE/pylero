# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from .abstract_polarion_persistent_object import AbstractPolarionPersistentObject

class TestRun(AbstractPolarionPersistentObject):

    empty_template = 'Empty'

    class Status():
        ''' Values for a TestRun's status '''
        NOT_RUN     = "notrun"
        IN_PROGRESS = "inprogress"
        FINISHED    = "finished"


    def __init__(self, session):
        AbstractPolarionPersistentObject.__init__(self, session)
        self.project = None
        self.status = None


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
            self.project = self.session._get_default_project()
        if not self.status:
            self.status = TestRun.Status.NOT_RUN
        return self


    @classmethod
    def _isConvertible(cls, suds_object):
        if not AbstractPolarionPersistentObject._isConvertible(suds_object):
            return False
        # TODO: check all the attributes
        return True


    @classmethod
    def _mapFromSUDS(cls, session, suds_object):
        # TODO: sanity checks
        if SimpleTestRun._isConvertible(suds_object):
            return SimpleTestRun._mapFromSUDS(session, suds_object)
        else:
            # Fall back: Not a "proper" test plan, just a document
            testRun = TestRun(session)
            TestRun._mapSpecificAttributesFromSUDS(suds_object, testRun)
            return testRun


    def _mapToSUDS(self):
        suds_object = self.session.test_management_client.factory.create('tns3:TestRun')
        TestRun._mapSpecificAttributesToSUDS(self, suds_object)
        return suds_object


    @classmethod
    def _mapSpecificAttributesToSUDS(cls, testRun, suds_object):

        AbstractPolarionPersistentObject._mapSpecificAttributesToSUDS(testRun, suds_object)

        session = testRun.session

        suds_object.projectURI = session.project_client.service.getProject(testRun.project)._uri

        suds_object.status = session.test_management_client.factory.create('tns4:EnumOptionId')
        suds_object.status.id = testRun.status


    @classmethod
    def _mapSpecificAttributesFromSUDS(cls, suds_object, testRun):

        AbstractPolarionPersistentObject._mapSpecificAttributesFromSUDS(suds_object, testRun)

        session = testRun.session

        testRun.project = session.project_client.service.getProjectByURI(suds_object.projectURI).id
        testRun.status = suds_object.status.id


    def _crudCreate(self, project=None):

        self._fillMissingValues(project)

        # By Polarion's design, we store the test run in two steps:
        # create and update.

        uri = self.session.test_management_client.service.createTestRun(self.project, self.pid, self.empty_template)
        uri = '{}'.format(uri)  # work around Text jumping in sometimes
        suds_object = self.session.test_management_client.service.getTestRunByUri(uri)
        stub = self.__class__._mapFromSUDS(self.session, suds_object)

        temp = (self.status, None) # use a tuple, over time there will be more attributes here

        stub._copy(self)
        self.status = temp[0]

        return self._crudUpdate()


    def _crudRetrieve(self):
        if not self.puri:
            raise PylarionLibException('Current object has no URI, cannot retrieve data')
        suds_object = self.session.test_management_client.service.getTestRunByUri(self.puri)
        temp = self.__class__._mapFromSUDS(self.session, suds_object)
        temp._copy(self)
        return self


    def _crudUpdate(self):
        if not self.puri:
            raise PylarionLibException('Current object has no URI, cannot update data')
        self._fillMissingValues()
        suds_object = self._mapToSUDS()
        self.session.test_management_client.service.updateTestRun(suds_object)
        return self._crudRetrieve()


    def _crudDelete(self):
        raise PylarionLibException('Not implemented')


from .exceptions import PylarionLibException
from .simple_test_run import SimpleTestRun
