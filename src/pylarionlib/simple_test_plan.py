# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from .document import Document

class SimpleTestPlan(Document):
    
    # TODO: references to test cases

    _typeId = 'testspecification'

    def __init__(self, session):

        Document.__init__(self, session)

        self.type = SimpleTestPlan._typeId

        self.workItemTypes = [ tcls._wiType for tcls in [ FunctionalTestCase, StructuralTestCase, NonFunctionalTestCase, TestSuite ] ]


    @classmethod
    def _isConvertible(cls, suds_object):
        if not Document._isConvertible(suds_object):
            return False
        if not hasattr(suds_object, 'type'):
            return False
        if not hasattr(suds_object, 'id'):
            return False
        if suds_object.type.id != SimpleTestPlan._typeId:
            return False
        # TODO: check text.content for a simple, expected text
        return True


    @classmethod
    def _mapFromSUDS(cls, session, suds_object):
        simpleTestPlan = SimpleTestPlan(session)
        SimpleTestPlan._mapSpecificAttributesFromSUDS(suds_object, simpleTestPlan)
        return simpleTestPlan


    def _mapToSUDS(self):
        suds_object = self.session.tracker_client.factory.create('tns3:Module')
        SimpleTestPlan._mapSpecificAttributesToSUDS(self, suds_object)
        return suds_object


from .test_classes import FunctionalTestCase, StructuralTestCase, NonFunctionalTestCase, TestSuite
