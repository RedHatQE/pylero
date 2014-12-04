# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from .document import Document

class SimpleTestPlan(Document):

    # A temporary implementation for "simple" (Pylarion-friendly) test plans.
    # TODO: Reimplement when we configure Polarion, eventually. I guess
    #       we should dedicate one or more custom fields to declare "simple"
    #       plans and their hierarchy.

    # TODO: references to test cases etc. See interface.txt for more.

    _DOCUMENT_TYPE = 'testspecification'
    _DOCUMENT_STRUCTURE_LINK_ROLE = 'parent'

    def __init__(self, session, project=None, namespace=None, name=None, initialText=None, parentPlanPURI=None, testCasesPURIs=[]):

        Document.__init__(self, session, project=project, namespace=namespace, name=name)

        self.type = SimpleTestPlan._DOCUMENT_TYPE

        self.structureLinkRole = SimpleTestPlan._DOCUMENT_STRUCTURE_LINK_ROLE

        self.workItemTypes = [ tcls._WI_TYPE for tcls in [ FunctionalTestCase, StructuralTestCase, NonFunctionalTestCase, TestSuite ] ]

        embedding = _SimpleTestPlanTextEmbedding.instantiateFromParentURI(parentPlanPURI)
        embedding.prefix = initialText
        self.text = TrackerText(session, content=embedding.toText())

        if testCasesPURIs:
            for i in testCasesPURIs:
                self._addTestCaseURI(i)


    @classmethod
    def _isConvertible(cls, sudsObject):
        if not Document._isConvertible(sudsObject):
            return False
        if not hasattr(sudsObject, 'type'):
            return False
        if not hasattr(sudsObject, 'id'):
            return False
        if sudsObject.type.id != SimpleTestPlan._DOCUMENT_TYPE:
            return False
        if not SimpleTestPlan._hasParentPlanEmbedding(sudsObject):
            return False
        # TODO: check all the test inside are linked only
        return True


    @classmethod
    def _mapFromSUDS(cls, session, sudsObject):
        simpleTestPlan = SimpleTestPlan(session)
        SimpleTestPlan._mapSpecificAttributesFromSUDS(sudsObject, simpleTestPlan)
        if not SimpleTestPlan._hasParentPlanEmbedding(sudsObject):
            raise PylarionLibException('No valid SimpleTestPlan embedding'.format(sudsObject))
        return simpleTestPlan


    def _mapToSUDS(self):
        sudsObject = self.session.trackerClient.factory.create('tns3:Module')
        SimpleTestPlan._mapSpecificAttributesToSUDS(self, sudsObject)
        return sudsObject


    def _crudCreate(self, project=None, namespace=None):
        # Work around a chicken-and-egg problem introduced by the two-steps
        # process needed to create a Document (Hint: by Polarion's design)
        if project:
            self.project = project
        if namespace:
            self.namespace = namespace
        tempDocument = Document(self.session)
        self._copy(tempDocument)
        tempDocument._crudCreate(project=self.project, namespace=self.namespace)
        self.puri = tempDocument.puri
        return self._crudRetrieve()


    @classmethod
    def _hasParentPlanEmbedding(cls, sudsObject):
        if not hasattr(sudsObject, 'homePageContent'):
            return False
        if not hasattr(sudsObject.homePageContent, 'content'):
            return False
        return None != _SimpleTestPlanTextEmbedding.instantiateFromText(sudsObject.homePageContent.content)


    def _getParentPlanURI(self):
        return _SimpleTestPlanTextEmbedding.getParentPlanURI(self.text.content)


    def _setParentPlanURI(self, uri):
        # NOTE: Not persisted until _crudUpdate()
        self.text.content = _SimpleTestPlanTextEmbedding.setParentPlanURI(self.text.content, uri)


    def _getTestCaseURIs(self):
        # NOTE: Not persisted until _crudUpdate()
        retval = []
        wipids = _SimpleTestPlanTextEmbedding.getLinkedWorkItemPIDs(self.text.content)
        for wipid in wipids:
            wi = self.session.getWorkItemByPID(wipid, self.project)
            if wi:
                retval.append(wi.puri)
        return retval


    def _addTestCaseURI(self, uri):
        # NOTE: Not persisted until _crudUpdate()
        wi = self.session.getWorkItemByPURI(uri)
        if wi.project != self.project:
            # TODO: is that really so?
            raise PylarionLibException('Work Item {} and Document {} are in different projects'.format(uri, self.puri))
        wipids = _SimpleTestPlanTextEmbedding.getLinkedWorkItemPIDs(self.text.content)
        if wi.pid not in wipids:
            wipids.append(wi.pid)
            self.text.content = _SimpleTestPlanTextEmbedding.setLinkedWorkItemPIDs(self.text.content, wipids)


    def _deleteTestCaseURI(self, uri):
        # NOTE: Not persisted until _crudUpdate()
        wi = self.session.getWorkItemByPURI(uri)
        if wi.project != self.project:
            # not in the same project, kinda "unreachable"
            raise PylarionLibException('Work Item {} and Document {} are in different projects'.format(uri, self.puri))
        wipids = _SimpleTestPlanTextEmbedding.getLinkedWorkItemPIDs(self.text.content)
        if wi.pid in wipids:
            wipids.remove(wi.pid)
            self.text.content = _SimpleTestPlanTextEmbedding.setLinkedWorkItemPIDs(self.text.content, wipids)


    def _deleteAllTestCaseURIs(self):
        # NOTE: Not persisted until _crudUpdate()
        wipids = _SimpleTestPlanTextEmbedding.getLinkedWorkItemPIDs(self.text.content)
        if wipids:
            self.text.content = _SimpleTestPlanTextEmbedding.setLinkedWorkItemPIDs(self.text.content, [])


    # public methods

    def getPlanText(self):
        embedding = _SimpleTestPlanTextEmbedding.instantiateFromText(self.text.content)
        return embedding.prefix

    def setPlanText(self, newText):
        embedding = _SimpleTestPlanTextEmbedding.instantiateFromText(self.text.content)
        embedding.prefix = newText
        self.text.content = embedding.toText()

    def getParentPlanPURI(self):
        return self._getParentPlanURI()

    def setParentPlanPURI(self, puri):
        self._setParentPlanURI(puri)

    def getTestCasesPURIs(self):
        return self._getTestCaseURIs()

    def addTestCasePURI(self, puri):
        self._addTestCaseURI(self, puri)

    def deleteTestCasePURI(self, puri):
        self._deleteTestCaseURI(puri)

    def deleteAllTestCases(self):
        self._deleteAllTestCaseURIs()


from .exceptions import PylarionLibException
from .test_classes import FunctionalTestCase, StructuralTestCase, NonFunctionalTestCase, TestSuite
from .tracker_text import TrackerText
from .embedding import _SimpleTestPlanTextEmbedding
