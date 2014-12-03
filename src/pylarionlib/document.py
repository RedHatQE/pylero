# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import suds

from .abstract_polarion_persistent_object import AbstractPolarionPersistentObject

class Document(AbstractPolarionPersistentObject):


    def __init__(self, session):
        AbstractPolarionPersistentObject.__init__(self, session)
        self.project = None
        self.namespace = None
        self.name = None
        self.type = None
        self.workItemTypes = []
        self.structureLinkRole = None
        self.text = None


    def _copy(self, another):
        AbstractPolarionPersistentObject._copy(self, another)
        another.project = self.project
        another.namespace = self.namespace
        another.name = self.name
        another.type = self.type
        another.workItemTypes = self.workItemTypes
        another.structureLinkRole = self.structureLinkRole
        another.text = self.text
        return another


    def _fillMissingValues(self, project=None, namespace=None):
        super(Document, self)._fillMissingValues(project, namespace)
        if project:
            self.project = project
        if not self.project:
            self.project = self.session._get_default_project()
        if namespace:
            self.namespace = namespace
        if not self.namespace:
            self.namespace = self.session._get_default_namespace()
        if not self.text:
            self.text = TrackerText(self.session)
        return self


    def _workItemTypesToSUDS(self):
        sudsAllowedWITypes = []
        if self.workItemTypes:
            for i in self.workItemTypes:
                wiTypeInstance = self.session.tracker_client.factory.create('tns3:EnumOptionId')
                wiTypeInstance.id = i
                sudsAllowedWITypes.append(wiTypeInstance)
        return sudsAllowedWITypes


    def _structureLinkRoleToSUDS(self):
        sudsStructureLinkRole = self.session.tracker_client.factory.create('tns3:EnumOptionId')
        sudsStructureLinkRole.id = self.structureLinkRole
        return sudsStructureLinkRole


    @classmethod
    def _isConvertible(cls, sudsObject):
        if not AbstractPolarionPersistentObject._isConvertible(sudsObject):
            return False
        # TODO: check all the attributes
        return True


    @classmethod
    def _mapFromSUDS(cls, session, sudsObject):
        # TODO: sanity checks
        if SimpleTestPlan._isConvertible(sudsObject):
            return SimpleTestPlan._mapFromSUDS(session, sudsObject)
        else:
            # Fall back: Not a "proper" test plan, just a document
            document = Document(session)
            Document._mapSpecificAttributesFromSUDS(sudsObject, document)
            return document


    def _mapToSUDS(self):
        sudsObject = self.session.tracker_client.factory.create('tns3:Module')
        Document._mapSpecificAttributesToSUDS(self, sudsObject)
        return sudsObject


    @classmethod
    def _mapSpecificAttributesToSUDS(cls, document, sudsObject):

        AbstractPolarionPersistentObject._mapSpecificAttributesToSUDS(document, sudsObject)

        session = document.session

        sudsObject.project = session.project_client.service.getProject(document.project)
        sudsObject.moduleFolder = document.namespace
        sudsObject.moduleName = document.name

        sudsObject.type = session.tracker_client.factory.create('tns3:EnumOptionId')
        sudsObject.type.id = document.type

        sudsObject.allowedWITypes = document._workItemTypesToSUDS()

        sudsObject.structureLinkRole = session.tracker_client.factory.create('tns3:EnumOptionId')
        sudsObject.structureLinkRole.id = document.structureLinkRole

        if not document.text:
            document.text = TrackerText(session)
        sudsObject.homePageContent = document.text._mapToSUDS()


    @classmethod
    def _mapSpecificAttributesFromSUDS(cls, sudsObject, document):

        AbstractPolarionPersistentObject._mapSpecificAttributesFromSUDS(sudsObject, document)

        session = document.session

        document.project = sudsObject.project.id
        document.namespace = sudsObject.moduleFolder
        document.name = sudsObject.moduleName

        if hasattr(sudsObject, 'type'):
            document.type = sudsObject.type.id

        document.workItemTypes = []
        if hasattr(sudsObject, 'allowedWITypes') and hasattr(sudsObject.allowedWITypes, 'EnumOptionId') and sudsObject.allowedWITypes.EnumOptionId:
            for i in sudsObject.allowedWITypes.EnumOptionId:
                document.workItemTypes.append(i.id)

        document.structureLinkRole = sudsObject.structureLinkRole.id

        if hasattr(sudsObject, 'homePageContent'):
            document.text = TrackerText(session)
            TrackerText._mapSpecificAttributesFromSUDS(sudsObject.homePageContent, document.text)


    def _crudCreate(self, project=None, namespace=None):

        self._fillMissingValues(project, namespace)

        # This will be really crazy now. By Polarion's design and bugs, we
        # must store the document in two steps: create and update.

        uri = self.session.tracker_client.service.createModule(
                                           self.project,
                                           self.namespace,
                                           self.name,
                                           self._workItemTypesToSUDS(),
                                           self._structureLinkRoleToSUDS(),
                                           False,
                                           suds.null())
        uri = '{}'.format(uri) # work around Text jumping in sometimes
        sudsObject = self.session.tracker_client.service.getModuleByUri(uri)
        stub = self.__class__._mapFromSUDS(self.session, sudsObject)

        temp = (self.type, self.workItemTypes, self.text)

        stub._copy(self)
        self.type = temp[0]
        self.workItemTypes = temp[1]
        self.text = temp[2]

        return self._crudUpdate()


    def _crudRetrieve(self):
        if not self.puri:
            raise PylarionLibException('Current object has no URI, cannot retrieve data')
        sudsObject = self.session.tracker_client.service.getModuleByUri(self.puri)
        temp = self.__class__._mapFromSUDS(self.session, sudsObject)
        temp._copy(self)
        return self


    def _crudUpdate(self):
        if not self.puri:
            raise PylarionLibException('Current object has no URI, cannot update data')
        self._fillMissingValues()
        sudsObject = self._mapToSUDS()
        self.session.tracker_client.service.updateModule(sudsObject)
        return self._crudRetrieve()


    def _crudDelete(self):
        if not self.puri:
            raise PylarionLibException('Current object has no URI, cannot update data')
        self.session.tracker_client.service.deleteModule(self.puri)
        empty = self.__class__(self.session)
        empty._copy(self)


from .tracker_text import TrackerText
from .exceptions import PylarionLibException
from .simple_test_plan import SimpleTestPlan
