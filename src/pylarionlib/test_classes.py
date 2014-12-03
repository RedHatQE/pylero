# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import suds

from .work_item import WorkItem

class AbstractTest(WorkItem):

    _SCRIPT_URL_ROLE = 'testscript'

    class AutomationConstants(object):
        CF_NAME = 'caseautomation'
        VALUE_AUTOMATED = 'automated'
        VALUE_NOT_AUTOMATED = 'notautomated'
        VALUE_MANUAL_ONLY = 'manualonly'

    class TagsConstants(object):
        CF_NAME = 'tcmstag'

    _knownSubclasses = []


    def __init__(self, session):
        WorkItem.__init__(self, session)
        self.automation = None
        self.scriptURL = None
        self.tags = set()


    def _copy(self, another):
        WorkItem._copy(self, another)
        another.automation = self.automation
        another.scriptURL = self.scriptURL
        another.tags = self.tags
        return another


    def _fillMissingValues(self, project=None, namespace=None):
        super(AbstractTest, self)._fillMissingValues(project, namespace)
        return self


    @classmethod
    def _parseScriptURL(cls, sudsObject):
        # return (is-properly-structured, url-if-any)
        if not sudsObject:
            return (False, None)
        if not hasattr(sudsObject, 'hyperlinks'):
            return (True, None)
        if len(sudsObject.hyperlinks) == 0:
            return (True, None)
        if len(sudsObject.hyperlinks) > 1:
            return (False, None)
        if len(sudsObject.hyperlinks[0]) == 0:
            return (True, None)
        if len(sudsObject.hyperlinks[0]) > 1:
            return (False, None)
        if not hasattr(sudsObject.hyperlinks[0][0], 'uri'):
            return (True, None)
        return (True, sudsObject.hyperlinks[0][0].uri)


    # SUDS mapping

    @classmethod
    def _isConvertible(cls, sudsObject):
        if not WorkItem._isConvertible(sudsObject):
            return False
        return AbstractTest._parseScriptURL(sudsObject)[0]


    @classmethod
    def _mapSpecificAttributesToSUDS(cls, abstractTest, sudsObject):
        WorkItem._mapSpecificAttributesToSUDS(abstractTest, sudsObject)
        if abstractTest.scriptURL:
            # Except Polarion ignores this item for create/update :-(
            # Instead, we must use addHyperlink() and removeHyperlink() of Polarion's SOAP API.
            hyperlink = TrackerHyperlink(abstractTest.session, role=AbstractTest._SCRIPT_URL_ROLE, uri=abstractTest.scriptURL)
            sudsObject.hyperlinks = [ [ hyperlink._mapToSUDS() ] ]
        else:
            hyperlink = suds.null()


    @classmethod
    def _mapSpecificAttributesFromSUDS(cls, sudsObject, abstractTest):
        WorkItem._mapSpecificAttributesFromSUDS(sudsObject, abstractTest)
        abstractTest.scriptURL = AbstractTest._parseScriptURL(sudsObject)[1]
        abstractTest._retrieveAutomation()
        abstractTest._retrieveTags()


    @classmethod
    def _isKnownType(cls, typeString):
        for subclass in AbstractTest._knownSubclasses:
            if typeString == subclass._wiType:
                return True
        return False


    @classmethod
    def _mapFromSUDS(cls, session, sudsObject):
        # TODO: sanity checks?
        typeString = sudsObject.type.id
        for subclass in AbstractTest._knownSubclasses:
            if typeString == subclass._wiType:
                return subclass._mapFromSUDS(session, sudsObject)
        raise PylarionLibException('Unknown work item type {}'.format(typeString))


    # Helper methods for CRUD

    def _fixScriptURL(self, wishedScriptURL):
        actualSriptURL = self.scriptURL
        if wishedScriptURL == actualSriptURL:
            return
        if actualSriptURL:
            self.session.trackerClient.service.removeHyperlink(self.puri, actualSriptURL)
        if wishedScriptURL:
            self.session.trackerClient.service.addHyperlink(self.puri, wishedScriptURL, TrackerHyperlink._createRoleSUDSObjects(self.session, AbstractTest._SCRIPT_URL_ROLE))
        self._crudRetrieve()
        if wishedScriptURL != self.scriptURL:
            raise PylarionLibException('Cannot add Hyperlink={} to Work Item {}'.format(wishedScriptURL, self.puri))

    def _retrieveAutomation(self):
        self.automation = None
        envelope = self.session.trackerClient.service.getCustomField(self.puri, AbstractTest.AutomationConstants.CF_NAME)
        if envelope:
            if hasattr(envelope, 'value'):
                if envelope.value:
                    if hasattr(envelope.value, 'id'):
                        self.automation = envelope.value.id

    def _fixAutomation(self, wishedAutomation):
        actualAutomation = self.automation
        if wishedAutomation == actualAutomation:
            return
        cf = self.session.trackerClient.factory.create('tns3:CustomField')
        cf.parentItemURI = self.puri
        cf.key = AbstractTest.AutomationConstants.CF_NAME
        cf.value = self.session.trackerClient.factory.create('tns3:EnumOptionId')
        cf.value.id = wishedAutomation
        self.session.trackerClient.service.setCustomField(cf)
        self._retrieveAutomation()
        if wishedAutomation != self.automation:
            raise PylarionLibException('Cannot set Automation={} to Work Item {}'.format(wishedAutomation, self.puri))

    def _retrieveTags(self):
        self.tags = set()
        envelope = self.session.trackerClient.service.getCustomField(self.puri, AbstractTest.TagsConstants.CF_NAME)
        if envelope:
            if hasattr(envelope, 'value'):
                if envelope.value:
                    self.tags = set(x.strip() for x in envelope.value.split(',') if x.strip())

    def _fixTags(self, wishedTags):
        actualTags = self.tags
        if wishedTags == actualTags:
            return
        cf = self.session.trackerClient.factory.create('tns3:CustomField')
        cf.parentItemURI = self.puri
        cf.key = AbstractTest.TagsConstants.CF_NAME
        cf.value = ','.join(wishedTags)
        self.session.trackerClient.service.setCustomField(cf)
        self._retrieveTags()
        if wishedTags != self.tags:
            raise PylarionLibException('Cannot set Tags={} to Work Item {}'.format(wishedTags, self.puri))

    def _crudCreateOrUpdate(self, create=True, project=None):
        if not self.tags:
            self.tags = set()
        if self.tags:
            if type(self.tags) in [unicode, str]:
                self.tags = [self.tags]
            if type(self.tags) == list:
                self.tags = set(self.tags)
        wishedScriptURL = self.scriptURL
        wishedAutomation = self.automation
        wishedTags = self.tags
        if create:
            super(AbstractTest, self)._crudCreate(project)
        else:
            super(AbstractTest, self)._crudUpdate()
        self._fixScriptURL(wishedScriptURL)
        self._fixAutomation(wishedAutomation)
        self._fixTags(wishedTags)
        return self._crudRetrieve()


    # CRUD

    def _crudCreate(self, project=None):
        self._crudCreateOrUpdate(True, project=project)

    def _crudUpdate(self):
        self._crudCreateOrUpdate(False)


class FunctionalTestCase(AbstractTest):

    _wiType = 'functionaltestcase'
    _knownSubclasses = []

    def __init__(self, session):
        AbstractTest.__init__(self, session)
        self.type = FunctionalTestCase._wiType
        self.posNeg = None

    def _copy(self, another):
        AbstractTest._copy(self, another)
        another.type = self.type
        another.posNeg = self.posNeg
        return another

    def _fillMissingValues(self, project=None, namespace=None):
        super(FunctionalTestCase, self)._fillMissingValues(project, namespace)
        if not self.type:
            self.type = FunctionalTestCase._wiType
        return self

    @classmethod
    def _mapFromSUDS(cls, session, sudsObject):
        typeString = sudsObject.type.id
        if typeString != FunctionalTestCase._wiType:
            raise PylarionLibException('Cannot instantiate from {}'.format(typeString))
        wi = FunctionalTestCase(session)
        FunctionalTestCase._mapSpecificAttributesFromSUDS(sudsObject, wi)
        return wi


class StructuralTestCase(AbstractTest):

    _wiType = 'structuraltestcase'
    _knownSubclasses = []

    def __init__(self, session):
        AbstractTest.__init__(self, session)
        self.type = StructuralTestCase._wiType
        self.posNeg = None

    def _copy(self, another):
        AbstractTest._copy(self, another)
        another.type = self.type
        another.posNeg = self.posNeg
        return another

    def _fillMissingValues(self, project=None, namespace=None):
        super(StructuralTestCase, self)._fillMissingValues(project, namespace)
        if not self.type:
            self.type = FunctionalTestCase._wiType
        return self

    @classmethod
    def _mapFromSUDS(cls, session, sudsObject):
        typeString = sudsObject.type.id
        if typeString != StructuralTestCase._wiType:
            raise PylarionLibException('Cannot instantiate from {}'.format(typeString))
        wi = StructuralTestCase(session)
        StructuralTestCase._mapSpecificAttributesFromSUDS(sudsObject, wi)
        return wi


class NonFunctionalTestCase(AbstractTest):

    _wiType = 'nonfunctionaltestcase'
    _knownSubclasses = []

    def __init__(self, session):
        AbstractTest.__init__(self, session)
        self.type = NonFunctionalTestCase._wiType
        self.posNeg = None

    def _copy(self, another):
        AbstractTest._copy(self, another)
        another.type = self.type
        another.posNeg = self.posNeg
        return another

    def _fillMissingValues(self, project=None, namespace=None):
        super(NonFunctionalTestCase, self)._fillMissingValues(project, namespace)
        if not self.type:
            self.type = FunctionalTestCase._wiType
        return self

    @classmethod
    def _mapFromSUDS(cls, session, sudsObject):
        typeString = sudsObject.type.id
        if typeString != NonFunctionalTestCase._wiType:
            raise PylarionLibException('Cannot instantiate from {}'.format(typeString))
        wi = NonFunctionalTestCase(session)
        NonFunctionalTestCase._mapSpecificAttributesFromSUDS(sudsObject, wi)
        return wi


class TestSuite(AbstractTest):

    _wiType = 'testsuite'
    _knownSubclasses = []

    def __init__(self, session):
        AbstractTest.__init__(self, session)
        self.type = TestSuite._wiType
        self.testTypes = None

    def _copy(self, another):
        AbstractTest._copy(self, another)
        another.type = self.type
        another.testTypes = self.testTypes
        return another

    def _fillMissingValues(self, project=None, namespace=None):
        super(TestSuite, self)._fillMissingValues(project, namespace)
        if not self.type:
            self.type = FunctionalTestCase._wiType
        return self

    @classmethod
    def _mapFromSUDS(cls, session, sudsObject):
        typeString = sudsObject.type.id
        if typeString != TestSuite._wiType:
            raise PylarionLibException('Cannot instantiate from {}'.format(typeString))
        wi = TestSuite(session)
        TestSuite._mapSpecificAttributesFromSUDS(sudsObject, wi)
        return wi


AbstractTest._knownSubclasses = [ FunctionalTestCase, StructuralTestCase, NonFunctionalTestCase, TestSuite ]


from .exceptions import PylarionLibException
from .tracker_hyperlink import TrackerHyperlink
