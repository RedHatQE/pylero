# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import suds

from .abstract_polarion_persistent_object import AbstractPolarionPersistentObject

class WorkItem(AbstractPolarionPersistentObject):

    def __init__(self, session,
                 project=None,
                 title=None,
                 wiType=None,
                 status=None,
                 description=None,
                 initialEstimate=None):

        AbstractPolarionPersistentObject.__init__(self, session)

        self.project = project
        self.title = title
        self.wiType = wiType
        self.status = status
        self.description = description
        self.initialEstimate = initialEstimate

        if self.description:
            if type(self.description) in [str, unicode]:
                content = self.description
                self.description = TrackerText(self.session, content=content)


    def _copy(self, another):
        AbstractPolarionPersistentObject._copy(self, another)
        another.project = self.project
        another.title = self.title
        another.wiType = self.wiType
        another.status = self.status
        another.description = self.description
        another.initialEstimate = self.initialEstimate
        return another


    def _fillMissingValues(self, project=None, namespace=None):
        super(WorkItem, self)._fillMissingValues(project, namespace)
        if project:
            self.project = project
        if not self.project:
            self.project = self.session._getDefaultProject()
        return self


    @classmethod
    def _isConvertible(cls, sudsObject):
        if not AbstractPolarionPersistentObject._isConvertible(sudsObject):
            return False
        # TODO: check all the attributes; some are allowed be absent (f.ex. title)
        return True


    @classmethod
    def _mapSpecificAttributesToSUDS(cls, workItem, sudsObject):

        AbstractPolarionPersistentObject._mapSpecificAttributesToSUDS(workItem, sudsObject)

        session = workItem.session

        typeInstance = session.trackerClient.factory.create('tns3:EnumOptionId')
        typeInstance.id = workItem.wiType

        statusInstance = session.trackerClient.factory.create('tns3:EnumOptionId')
        statusInstance.id = workItem.status

        sudsObject.project = session.projectClient.service.getProject(workItem.project)
        sudsObject.title = workItem.title
        sudsObject.type = typeInstance
        sudsObject.status = statusInstance

        # description needs cheating: Polarion server does not accept suds.null() there
        if not workItem.description:
            workItem.description = TrackerText(session) # just empty...
        sudsObject.description = workItem.description._mapToSUDS()

        sudsObject.initialEstimate = workItem.initialEstimate if workItem.initialEstimate else suds.null()


    @classmethod
    def _mapSpecificAttributesFromSUDS(cls, sudsObject, workItem):

        AbstractPolarionPersistentObject._mapSpecificAttributesFromSUDS(sudsObject, workItem)

        session = workItem.session

        workItem.project = sudsObject.project.id
        workItem.title = sudsObject.title if hasattr(sudsObject, 'title') else None
        workItem.wiType = sudsObject.type.id
        workItem.status = sudsObject.status.id

        if hasattr(sudsObject, 'description'):
            workItem.description = TrackerText(session)
            TrackerText._mapSpecificAttributesFromSUDS(sudsObject.description, workItem.description)
        else:
            workItem.description = None

        workItem.initialEstimate = sudsObject.initialEstimate if hasattr(sudsObject, 'initialEstimate') else None


    def _mapToSUDS(self):
        sudsObject = self.session.trackerClient.factory.create('tns3:WorkItem')
        WorkItem._mapSpecificAttributesToSUDS(self, sudsObject)
        return sudsObject


    @classmethod
    def _mapFromSUDS(cls, session, sudsObject):
        # TODO: sanity checks
        # TODO: change the following to use _isConvertible
        typeString = sudsObject.type.id
        if AbstractTest._isKnownType(typeString):
            return AbstractTest._mapFromSUDS(session, sudsObject)
        else:
            # fallback for the types we don't care much
            workItem = WorkItem(session)
            WorkItem._mapSpecificAttributesFromSUDS(sudsObject, workItem)
            return workItem


    # CRUD:

    def _crudCreate(self, project=None):
        self._fillMissingValues(project)
        sudsObject = self._mapToSUDS()
        uri = self.session.trackerClient.service.createWorkItem(sudsObject)
        uri = '{}'.format(uri) # work around Text jumping in sometimes
        self.puri = uri
        return self._crudRetrieve()

    def _crudRetrieve(self):
        if not self.puri:
            raise PylarionLibException('Current object has no URI, cannot retrieve data')
        sudsObject = self.session.trackerClient.service.getWorkItemByUri(self.puri)
        temp = WorkItem._mapFromSUDS(self.session, sudsObject)
        temp._copy(self)
        return self

    def _crudUpdate(self):
        if not self.puri:
            raise PylarionLibException('Current object has no URI, cannot update data')
        self._fillMissingValues()
        sudsObject = self._mapToSUDS()
        self.session.trackerClient.service.updateWorkItem(sudsObject)
        return self._crudRetrieve()

    def _crudDelete(self):
        # TODO: check with Polarion support; deactivate instead?
        raise PylarionLibException('Not implemented')


from .exceptions import PylarionLibException
from .tracker_text import TrackerText
from .test_classes import AbstractTest
