# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from .work_item import WorkItem

class AbstractTest(WorkItem):

    # Maybe I should rename this class to AbstractSimpleTest and add -Simple-
    # to the subclasses names, too?

    # Implementation notes:
    # On the Polarion side, the data specific for this level and interesting to us
    # are hidden a bit:
    # - scriptURL ... suds_object.hyperlinks[0].uri ... if we can simplify so
    # - automation ... tracker_proxy.getCustomField(puri, 'caseautomation').value
    # - tcmsTags ... ditto but with 'tcmstag'
    # In practice, we must include additional SOAP calls in the _mapSpecificAttributes*()
    # methods as well as in the CRUD methods.

    _known_subclasses = []

    def __init__(self, session):
        WorkItem.__init__(self, session)
        self.automation = None
        self.scriptURL = None
        self.tcmsTags = []


    def _copy(self, another):
        WorkItem._copy(self, another)
        another.automation = self.automation
        another.scriptURL = self.scriptURL
        another.tcmsTags = self.tcmsTags
        return another


    @classmethod
    def _isConvertible(cls, suds_object):
        if not WorkItem._isConvertible(suds_object):
            return False
        # TODO: AbstractTest specific attributes
        return True


    @classmethod
    def _mapSpecificAttributesToSUDS(cls, abstractTest, suds_object):
        WorkItem._mapSpecificAttributesToSUDS(abstractTest, suds_object)
        # TODO: AbstractTest specific attributes


    @classmethod
    def _mapSpecificAttributesFromSUDS(cls, suds_object, abstractTest):
        WorkItem._mapSpecificAttributesFromSUDS(suds_object, abstractTest)
        # TODO: AbstractTest specific attributes


    @classmethod
    def _is_known_type(cls, type_string):
        for subclass in AbstractTest._known_subclasses:
            if type_string == subclass._wiType:
                return True
        return False


    @classmethod
    def _mapFromSUDS(cls, session, suds_object):
        # TODO: sanity checks?
        type_string = suds_object.type.id
        for subclass in AbstractTest._known_subclasses:
            if type_string == subclass._wiType:
                return subclass._mapFromSUDS(session, suds_object)
        raise PylarionLibException('Unknown work item type {}'.format(type_string))


    # TODO: CRUD


# TODO: all the below

class FunctionalTestCase(AbstractTest):

    _wiType = 'functionaltestcase'
    _known_subclasses = []

    def __init__(self, session):
        AbstractTest.__init__(self, session)
        self.type = FunctionalTestCase._wiType
        self.pos_neg = None

    def _copy(self, another):
        AbstractTest._copy(self, another)
        another.type = self.type
        another.pos_neg = self.pos_neg
        return another

    @classmethod
    def _mapSpecificAttributesToSUDS(cls, abstractTest, suds_object):
        AbstractTest._mapSpecificAttributesToSUDS(abstractTest, suds_object)
        # TODO: FunctionalTestCase specific attributes

    @classmethod
    def _mapSpecificAttributesFromSUDS(cls, suds_object, abstractTest):
        AbstractTest._mapSpecificAttributesFromSUDS(suds_object, abstractTest)
        # TODO: FunctionalTestCase specific attributes

    @classmethod
    def _mapFromSUDS(cls, session, suds_object):
        type_string = suds_object.type.id
        if type_string != FunctionalTestCase._wiType:
            raise PylarionLibException('Cannot instantiate from {}'.format(type_string))
        wi = FunctionalTestCase(session)
        FunctionalTestCase._mapSpecificAttributesFromSUDS(suds_object, wi)
        return wi

class StructuralTestCase(AbstractTest):

    _wiType = 'structuraltestcase'
    _known_subclasses = []

    def __init__(self, session):
        AbstractTest.__init__(self, session)
        self.type = StructuralTestCase._wiType
        self.pos_neg = None

    def _copy(self, another):
        AbstractTest._copy(self, another)
        another.type = self.type
        another.pos_neg = self.pos_neg
        return another

    @classmethod
    def _mapSpecificAttributesToSUDS(cls, abstractTest, suds_object):
        AbstractTest._mapSpecificAttributesToSUDS(abstractTest, suds_object)
        # TODO: StructuralTestCase specific attributes

    @classmethod
    def _mapSpecificAttributesFromSUDS(cls, suds_object, abstractTest):
        AbstractTest._mapSpecificAttributesFromSUDS(suds_object, abstractTest)
        # TODO: StructuralTestCase specific attributes

    @classmethod
    def _mapFromSUDS(cls, session, suds_object):
        type_string = suds_object.type.id
        if type_string != StructuralTestCase._wiType:
            raise PylarionLibException('Cannot instantiate from {}'.format(type_string))
        wi = StructuralTestCase(session)
        StructuralTestCase._mapSpecificAttributesFromSUDS(suds_object, wi)
        return wi

class NonFunctionalTestCase(AbstractTest):

    _wiType = 'nonfunctionaltestcase'
    _known_subclasses = []

    def __init__(self, session):
        AbstractTest.__init__(self, session)
        self.type = NonFunctionalTestCase._wiType
        self.pos_neg = None

    def _copy(self, another):
        AbstractTest._copy(self, another)
        another.type = self.type
        another.pos_neg = self.pos_neg
        return another

    @classmethod
    def _mapSpecificAttributesToSUDS(cls, abstractTest, suds_object):
        AbstractTest._mapSpecificAttributesToSUDS(abstractTest, suds_object)
        # TODO: NonFunctionalTestCase specific attributes

    @classmethod
    def _mapSpecificAttributesFromSUDS(cls, suds_object, abstractTest):
        AbstractTest._mapSpecificAttributesFromSUDS(suds_object, abstractTest)
        # TODO: NonFunctionalTestCase specific attributes

    @classmethod
    def _mapFromSUDS(cls, session, suds_object):
        type_string = suds_object.type.id
        if type_string != NonFunctionalTestCase._wiType:
            raise PylarionLibException('Cannot instantiate from {}'.format(type_string))
        wi = NonFunctionalTestCase(session)
        NonFunctionalTestCase._mapSpecificAttributesFromSUDS(suds_object, wi)
        return wi


class TestSuite(AbstractTest):

    _wiType = 'testsuite'
    _known_subclasses = []

    def __init__(self, session):
        AbstractTest.__init__(self, session)
        self.type = TestSuite._wiType
        self.testTypes = None

    def _copy(self, another):
        AbstractTest._copy(self, another)
        another.type = self.type
        another.testTypes = self.testTypes
        return another

    @classmethod
    def _mapSpecificAttributesToSUDS(cls, abstractTest, suds_object):
        AbstractTest._mapSpecificAttributesToSUDS(abstractTest, suds_object)
        # TODO: TestSuite specific attributes

    @classmethod
    def _mapSpecificAttributesFromSUDS(cls, suds_object, abstractTest):
        AbstractTest._mapSpecificAttributesFromSUDS(suds_object, abstractTest)
        # TODO: TestSuite specific attributes

    @classmethod
    def _mapFromSUDS(cls, session, suds_object):
        type_string = suds_object.type.id
        if type_string != TestSuite._wiType:
            raise PylarionLibException('Cannot instantiate from {}'.format(type_string))
        wi = TestSuite(session)
        TestSuite._mapSpecificAttributesFromSUDS(suds_object, wi)
        return wi


AbstractTest._known_subclasses = [ FunctionalTestCase, StructuralTestCase, NonFunctionalTestCase, TestSuite ]


from .exceptions import PylarionLibException
