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


    @classmethod
    def _isConvertible(cls, suds_object):
        if not TestRun._isConvertible(suds_object):
            return False
        return SimpleTestRun._hasPlanEmbedding(suds_object)


    @classmethod
    def _mapFromSUDS(cls, session, suds_object):
        simpleTestRun = SimpleTestRun(session)
        SimpleTestRun._mapSpecificAttributesFromSUDS(suds_object, simpleTestRun)
        return simpleTestRun


    def _mapToSUDS(self):
        suds_object = self.session.test_management_client.factory.create('tns3:TestRun')
        SimpleTestRun._mapSpecificAttributesToSUDS(self, suds_object)
        return suds_object


    def _crudCreate(self, project=None):

        # Custom code to CREATE a persistent instance.
        # First, we must work around Polarion's inability to create a (normal)
        # test run in one step.
        # Second, the wiki content (where we store a reference to a test plan)
        # isn't directly accessible (we must call yet another methods of the
        # Polarion API).
        # Lasciate ogne speranza, voi ch'intrate

        tempTestRun = TestRun(self.session)
        self._copy(tempTestRun)
        tempTestRun._crudCreate(project=project)

        wiki = self.session.test_management_client.service.getWikiContentForTestRun(tempTestRun.puri)
        embedding = _SimpleTestRunTextEmbedding.instantiateFromPlanURI(None)
        embedding.prefix = wiki.content
        if not embedding.prefix.endswith('\n'):
            embedding.prefix = '{}\n'.format(embedding.prefix)
        embedding.suffix = ''
        wiki.content = embedding.toText()
        self.session.test_management_client.service.updateWikiContentForTestRun(tempTestRun.puri, wiki)

        self.puri = tempTestRun.puri

        # For some peculiar reason, out testing project creates test run
        # with one predefined test record though there's no corresponding
        # work item. For now, just brute force.
        # TODO: Investigate, maybe template problem?
        self._setTestRecords([])

        return self._crudRetrieve()


    @classmethod
    def _hasPlanEmbedding(cls, suds_object):
        # TODO: Look into getWikiContentForTestRun(...) and decide
        return True


    def _getPlanURI(self):
        wiki = self.session.test_management_client.service.getWikiContentForTestRun(self.puri)
        return _SimpleTestRunTextEmbedding.getPlanURI(wiki.content)


    def _setPlanURI(self, uri):
        # NOTE: Persisted immediately!
        wiki = self.session.test_management_client.service.getWikiContentForTestRun(self.puri)
        newContent = _SimpleTestRunTextEmbedding.setPlanURI(wiki.content, uri)
        wiki.content = newContent
        self.session.test_management_client.service.updateWikiContentForTestRun(self.puri, wiki)


    def _getTestRecords(self):

        suds_object = self.session.test_management_client.service.getTestRunByUri(self.puri)
        if not suds_object or suds_object._unresolvable:
            raise PylarionLibException('Test Run UID not found: {}'.format(self.puri))

        retval = []
        if hasattr(suds_object, 'records'):
            if suds_object.records:
                if suds_object.records[0]:
                    if len(suds_object.records[0]) > 0:
                        for r in suds_object.records[0]:
                            if hasattr(r, 'testCaseURI'):
                                if r.testCaseURI != None:
                                    retval.append(TestRecord._mapFromSUDS(self.session, r))

        return retval


    def _setTestRecords(self, testRecords):
        # NOTE: Persisted immediately (and per partes)!

        # The "natural" way - updating individual test tecords - does not
        # work:
        # - updateTestRecord() does not work at all (reports no test record
        #   for the index)
        # - updateTestRecordAtIndex() updates but then *deletes* the tes
        #    record!
        # TODO: Report to Polarion

        suds_object = self.session.test_management_client.service.getTestRunByUri(self.puri)
        if not suds_object or suds_object._unresolvable:
            raise PylarionLibException('Test Run UID not found: {}'.format(self.puri))

        # There has to be the following item, otherwise we are screwed.
        # ATM I don't know how to create it "manually".
        records = suds_object.records[0]

        # "Empty" the run: I'm afraid there's this clumsy way only
        if records and len(records) > 0:
            for i in xrange(len(records) - 1, -1, -1):
                self.session.test_management_client.service.updateTestRecordAtIndex(self.puri, i, suds.null())

        if testRecords:
            for tr in testRecords:
                if tr:
                    self.session.test_management_client.service.addTestRecordToTestRun(self.puri, tr._mapToSUDS())


from .exceptions import PylarionLibException
from .embedding import _SimpleTestRunTextEmbedding
from .test_record import TestRecord
