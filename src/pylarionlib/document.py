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
    def _isConvertible(cls, suds_object):
        if not AbstractPolarionPersistentObject._isConvertible(suds_object):
            return False
        # TODO: check all the attributes
        return True


    @classmethod
    def _mapFromSUDS(cls, session, suds_object):
        # TODO: sanity checks
        # TODO: Can it be SimpleTestPlan (among others, check suds_object.type.id)? If yes, convert there, otherwise as follows
        document = Document(session)
        Document._mapSpecificAttributesFromSUDS(suds_object, document)
        return document


    def _mapToSUDS(self):
        suds_object = self.session.tracker_client.factory.create('tns3:Module')
        Document._mapSpecificAttributesToSUDS(self, suds_object)
        return suds_object


    @classmethod
    def _mapSpecificAttributesToSUDS(cls, document, suds_object):

        AbstractPolarionPersistentObject._mapSpecificAttributesToSUDS(document, suds_object)

        session = document.session

        suds_object.project = session.project_client.service.getProject(document.project)
        suds_object.moduleFolder = document.namespace
        suds_object.moduleName = document.name

        suds_object.type = session.tracker_client.factory.create('tns3:EnumOptionId')
        suds_object.type.id = document.type

        suds_object.allowedWITypes = document._workItemTypesToSUDS()

        suds_object.structureLinkRole = session.tracker_client.factory.create('tns3:EnumOptionId')
        suds_object.structureLinkRole.id = document.structureLinkRole

        if not document.text:
            document.text = TrackerText(session)
        suds_object.homePageContent = document.text._mapToSUDS()


    @classmethod
    def _mapSpecificAttributesFromSUDS(cls, suds_object, document):

        AbstractPolarionPersistentObject._mapSpecificAttributesFromSUDS(suds_object, document)

        session = document.session

        document.project = suds_object.project.id
        document.namespace = suds_object.moduleFolder
        document.name = suds_object.moduleName

        if hasattr(suds_object, 'type'):
            document.type = suds_object.type.id

        document.workItemTypes = []
        if hasattr(suds_object, 'allowedWITypes') and hasattr(suds_object.allowedWITypes, 'EnumOptionId') and suds_object.allowedWITypes.EnumOptionId:
            for i in suds_object.allowedWITypes.EnumOptionId:
                document.workItemTypes.append(i.id)

        document.structureLinkRole = suds_object.structureLinkRole.id

        if hasattr(suds_object, 'homePageContent'):
            document.text = TrackerText(session)
            TrackerText._mapSpecificAttributesFromSUDS(suds_object.homePageContent, document.text)


    def _crudCreate(self, project=None):

        if project:
            self.project = project
        if not self.project:
            self.project = self.session._get_default_project()
        if not self.namespace:
            self.namespace = self.session._get_default_namespace()
        if not self.text:
            self.text = TrackerText(self.session)

        # This will be really crazy now. By Polarion's design and bugs, we
        # must store the document in two steps: create and update.

        self.puri = self.session.tracker_client.service.createModule(
                                           self.project,
                                           self.namespace,
                                           self.name,
                                           self._workItemTypesToSUDS(),
                                           self._structureLinkRoleToSUDS(),
                                           False,
                                           suds.null())
        suds_object = self.session.tracker_client.service.getModuleByUri(self.puri)
        stub = Document._mapFromSUDS(self.session, suds_object)

        temp = (self.type, self.workItemTypes, self.text)

        stub._copy(self)
        self.type = temp[0]
        self.workItemTypes = temp[1]
        self.text = temp[2]

        return self._crudUpdate()


    def _crudRetrieve(self):
        if not self.puri:
            raise PylarionLibException('Current object has no URI, cannot retrieve data')
        suds_object = self.session.tracker_client.service.getModuleByUri(self.puri)
        temp = Document._mapFromSUDS(self.session, suds_object)
        temp._copy(self)
        return self


    def _crudUpdate(self):
        if not self.puri:
            raise PylarionLibException('Current object has no URI, cannot update data')
        if not self.project:
            self.project = self.session._get_default_project()
        if not self.namespace:
            self.namespace = self.session._get_default_namespace()
        if not self.text:
            self.text = TrackerText(self.session)
        suds_object = self._mapToSUDS()
        self.session.tracker_client.service.updateModule(suds_object)
        return self._crudRetrieve()


    def _crudDelete(self):
        if not self.puri:
            raise PylarionLibException('Current object has no URI, cannot update data')
        self.session.tracker_client.service.deleteModule(self.puri)
        empty = Document(self.session)
        empty._copy(self)


from .tracker_text import TrackerText
from .exceptions import PylarionLibException
