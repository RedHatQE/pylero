# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

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


from .embedding import _SimpleTestRunTextEmbedding
