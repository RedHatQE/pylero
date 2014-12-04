# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import suds

from .test_run import TestRun

class SimpleTestRun(TestRun):

    # This class is really strange. The primary design problem is that
    # we use a test run's wiki to embed a reference to the test plan
    # (other currently available options seem to be even worse) but
    # the wiki isn't a standard attribute of Polarion's TestRun object.
    # TODO: Fix the design. But. Obviously. Fix Polarion setup first.
    #       I think we should have one or two custom fields for "simple"
    #       test runs: to indicate that the test run is "simple" and to
    #       store the reference to a test plan.

    # TODO: manage status: testRun.status.id = 'inprogress' # other values: notrun, finished (defined by project, template, Polarion?)

    def __init__(self, session):
        super(SimpleTestRun, self).__init__(session)
        self.testPlanURI = None
        self.testRecords = []


    def _copy(self, another):
        super(SimpleTestRun, self)._copy(another)
        another.testPlanURI = self.testPlanURI
        another.testRecords = self.testRecords
        return another


    # SUDS mapping

    @classmethod
    def _isConvertible(cls, sudsObject):
        if not TestRun._isConvertible(sudsObject):
            return False
        return SimpleTestRun._hasPlanEmbedding(sudsObject)


    @classmethod
    def _mapSpecificAttributesFromSUDS(cls, sudsObject, testRun):
        TestRun._mapSpecificAttributesFromSUDS(sudsObject, testRun)
        testRun._retrieveTestPlanURI()
        testRun._retrieveTestRecords(sudsObject)


    @classmethod
    def _mapFromSUDS(cls, session, sudsObject):
        simpleTestRun = SimpleTestRun(session)
        SimpleTestRun._mapSpecificAttributesFromSUDS(sudsObject, simpleTestRun)
        return simpleTestRun


    def _mapToSUDS(self):
        sudsObject = self.session.testManagementClient.factory.create('tns3:TestRun')
        SimpleTestRun._mapSpecificAttributesToSUDS(self, sudsObject)
        return sudsObject


    @classmethod
    def _hasPlanEmbedding(cls, sudsObject):
        # TODO: Look into getWikiContentForTestRun(...) and decide
        return True


    # Helper methods for CRUD

    def _hasEquivTestRecords(self, testRecordList):
        if not self.testRecords and not testRecordList:
            return True
        if not self.testRecords and testRecordList:
            return False
        if self.testRecords and not testRecordList:
            return False
        if len(self.testRecords) != len(testRecordList):
            return False
        for i, j in zip(self.testRecords, testRecordList):
            if not i and j:
                return False
            if i and not j:
                return False
            if not i._equiv(j):
                return False
        return True


    def _retrieveTestPlanURI(self):
        wiki = self.session.testManagementClient.service.getWikiContentForTestRun(self.puri)
        self.testPlanURI = _SimpleTestRunTextEmbedding.getPlanURI(wiki.content)


    def _fixTestPlanURI(self, wishedTestPlanURI):
        actualTestPlanURI = self.testPlanURI
        if wishedTestPlanURI == actualTestPlanURI:
            return
        wiki = self.session.testManagementClient.service.getWikiContentForTestRun(self.puri)
        newContent = _SimpleTestRunTextEmbedding.setPlanURI(wiki.content, wishedTestPlanURI)
        wiki.content = newContent
        self.session.testManagementClient.service.updateWikiContentForTestRun(self.puri, wiki)
        self._retrieveTestPlanURI()
        if wishedTestPlanURI != self.testPlanURI:
            raise PylarionLibException('Cannot set Test Plan URI={} to Test Run {}'.format(wishedTestPlanURI, self.puri))


    def _retrieveTestRecords(self, sudsObject):
        self.testRecords = []
        if hasattr(sudsObject, 'records'):
            if sudsObject.records:
                if sudsObject.records[0]:
                    if len(sudsObject.records[0]) > 0:
                        for r in sudsObject.records[0]:
                            if hasattr(r, 'testCaseURI'):
                                if r.testCaseURI != None:
                                    self.testRecords.append(TestRecord._mapFromSUDS(self.session, r))


    def _fixTestRecords(self, wishedTestRecords):

        sudsObject = self.session.testManagementClient.service.getTestRunByUri(self.puri)
        self._retrieveTestRecords(sudsObject)

        if self._hasEquivTestRecords(wishedTestRecords):
            return

        # The "natural" way - updating individual test tecords - does not
        # work:
        # - updateTestRecord() does not work at all (reports no test record
        #   for the index)
        # - updateTestRecordAtIndex() updates but then *deletes* the tes
        #    record!
        # TODO: Report to Polarion

        records = sudsObject.records[0]

        # "Empty" the run: I'm afraid there's this clumsy way only
        if records and len(records) > 0:
            for i in xrange(len(records) - 1, -1, -1):
                self.session.testManagementClient.service.updateTestRecordAtIndex(self.puri, i, suds.null())

        if wishedTestRecords:
            for tr in wishedTestRecords:
                if tr:
                    self.session.testManagementClient.service.addTestRecordToTestRun(self.puri, tr._mapToSUDS())

        sudsObject = self.session.testManagementClient.service.getTestRunByUri(self.puri)
        self._retrieveTestRecords(sudsObject)

        if not self._hasEquivTestRecords(wishedTestRecords):
            raise PylarionLibException('For Test Run {}, cannot set Test Records: {}'.format(self.puri, wishedTestRecords))


    def _crudCreateOrUpdate(self, create=True, project=None):

        wishedTestPlanURI = self.testPlanURI
        wishedTestRecords = self.testRecords

        if create:
            # Custom code to CREATE a persistent instance.
            # Lasciate ogne speranza, voi ch'intrate

            tempTestRun = TestRun(self.session)
            self._copy(tempTestRun)
            tempTestRun._crudCreate(project=project)

            wiki = self.session.testManagementClient.service.getWikiContentForTestRun(tempTestRun.puri)
            embedding = _SimpleTestRunTextEmbedding.instantiateFromPlanURI(wishedTestPlanURI)
            embedding.prefix = wiki.content
            if not embedding.prefix.endswith('\n'):
                embedding.prefix = '{}\n'.format(embedding.prefix)
            embedding.suffix = ''
            wiki.content = embedding.toText()
            self.session.testManagementClient.service.updateWikiContentForTestRun(tempTestRun.puri, wiki)

            tempTestRun._copy(self)

        else:
            super(SimpleTestRun, self)._crudUpdate()

        self._fixTestPlanURI(wishedTestPlanURI)
        self._fixTestRecords(wishedTestRecords)
        return self._crudRetrieve()


    # CRUD

    def _crudCreate(self, project=None):
        return self._crudCreateOrUpdate(True, project)

    def _crudUpdate(self):
        return self._crudCreateOrUpdate(False)


from .exceptions import PylarionLibException
from .embedding import _SimpleTestRunTextEmbedding
from .test_record import TestRecord
