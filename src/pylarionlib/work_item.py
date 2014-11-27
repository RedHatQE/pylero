# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import suds

from .abstract_polarion_persistent_object import AbstractPolarionPersistentObject

class WorkItem(AbstractPolarionPersistentObject):

    def __init__(self, session):
        AbstractPolarionPersistentObject.__init__(self, session)
        self.project = None
        self.title = None
        self.type = None
        self.status = None
        self.description = None
        self.initialEstimate = None


    def _copy(self, another):
        AbstractPolarionPersistentObject._copy(self, another)
        another.project = self.project
        another.title = self.title
        another.type = self.type
        another.status = self.status
        another.description = self.description
        another.initialEstimate = self.initialEstimate
        return another


    @classmethod
    def _isConvertible(cls, suds_object):
        if not AbstractPolarionPersistentObject._isConvertible(suds_object):
            return False
        # TODO: check all the attributes; some are allowed be absent (f.ex. title)
        return True


    @classmethod
    def _mapSpecificAttributesToSUDS(cls, workItem, suds_object):

        AbstractPolarionPersistentObject._mapSpecificAttributesToSUDS(workItem, suds_object)

        session = workItem.session

        type_instance = session.tracker_client.factory.create('tns3:EnumOptionId')
        type_instance.id = workItem.type

        status_instance = session.tracker_client.factory.create('tns3:EnumOptionId')
        status_instance.id = workItem.status

        suds_object.project = session.project_client.service.getProject(workItem.project)
        suds_object.title = workItem.title
        suds_object.type = type_instance
        suds_object.status = status_instance

        # description needs cheating: Polarion server does not accept suds.null() there
        if not workItem.description:
            workItem.description = TrackerText(session) # just empty...
        suds_object.description = workItem.description._mapToSUDS()

        suds_object.initialEstimate = workItem.initialEstimate if workItem.initialEstimate else suds.null()


    @classmethod
    def _mapSpecificAttributesFromSUDS(cls, suds_object, workItem):

        AbstractPolarionPersistentObject._mapSpecificAttributesFromSUDS(suds_object, workItem)

        session = workItem.session

        workItem.project = suds_object.project.id
        workItem.title = suds_object.title if hasattr(suds_object, 'title') else None
        workItem.type = suds_object.type.id
        workItem.status = suds_object.status.id

        if hasattr(suds_object, 'description'):
            workItem.description = TrackerText(session)
            TrackerText._mapSpecificAttributesFromSUDS(suds_object.description, workItem.description)
        else:
            workItem.description = None

        workItem.initialEstimate = suds_object.initialEstimate if hasattr(suds_object, 'initialEstimate') else None


    def _mapToSUDS(self):
        suds_object = self.session.tracker_client.factory.create('tns3:WorkItem')
        WorkItem._mapSpecificAttributesToSUDS(self, suds_object)
        return suds_object


    @classmethod
    def _mapFromSUDS(cls, session, suds_object):
        # TODO: sanity checks
        # TODO: change the following to use _isConvertible
        type_string = suds_object.type.id
        if AbstractTest._is_known_type(type_string):
            return AbstractTest._mapFromSUDS(session, suds_object)
        else:
            # fallback for the types we don't care much
            workItem = WorkItem(session)
            WorkItem._mapSpecificAttributesFromSUDS(suds_object, workItem)
            return workItem


    # CRUD:

    def _crudCreate(self, project=None):
        if project:
            self.project = project
        if not self.project:
            self.project = self.session._get_default_project()
        suds_object = self._mapToSUDS()
        self.puri = self.session.tracker_client.service.createWorkItem(suds_object)
        return self._crudRetrieve()

    def _crudRetrieve(self):
        if not self.puri:
            raise PylarionLibException('Current object has no URI, cannot retrieve data')
        suds_object = self.session.tracker_client.service.getWorkItemByUri(self.puri)
        temp = WorkItem._mapFromSUDS(self.session, suds_object)
        temp._copy(self)
        return self

    def _crudUpdate(self):
        if not self.puri:
            raise PylarionLibException('Current object has no URI, cannot update data')
        if not self.project:
            self.project = self.session._get_default_project()
        suds_object = self._mapToSUDS()
        self.session.tracker_client.service.updateWorkItem(suds_object)
        return self._crudRetrieve()

    def _crudDelete(self):
        # TODO: check with Polarion support; deactivate instead?
        raise PylarionLibException('Not implemented')


from .exceptions import PylarionLibException
from .tracker_text import TrackerText
from .test_classes import AbstractTest
