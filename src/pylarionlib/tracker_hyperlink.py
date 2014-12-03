#!/usr/bin/env python
# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from .abstract_polarion_crate import AbstractPolarionCrate

class TrackerHyperlink(AbstractPolarionCrate):
    ''' A crate to deal with 'tns3:Hyperlink' of the Tracker service '''


    def __init__(self, session, role=None, uri=None):
        AbstractPolarionCrate.__init__(self, session)
        self.role = None
        self.uri = None
        self._fillMissingValues()


    def _copy(self, another):
        AbstractPolarionCrate._copy(self, another)
        another.role = self.role
        another.uri = self.uri
        return another


    @classmethod
    def _createRoleSUDSObjects(cls, session, role):
        retval = session.trackerClient.factory.create('tns3:EnumOptionId')
        retval.id = role
        return retval


    @classmethod
    def _isConvertible(cls, sudsObject):
        if sudsObject == None:
            return False
        if hasattr(sudsObject, 'role') and not hasattr(sudsObject.role, 'id'):
            return False
        return True


    @classmethod
    def _mapSpecificAttributesToSUDS(cls, trackerHyperlink, sudsObject):
        sudsObject.role = TrackerHyperlink._createRoleSUDSObjects(trackerHyperlink.session, trackerHyperlink.role)
        sudsObject.uri = trackerHyperlink.uri


    @classmethod
    def _mapSpecificAttributesFromSUDS(cls, sudsObject, trackerHyperlink):

        trackerHyperlink.role = None
        if hasattr(sudsObject, 'role') and hasattr(sudsObject.role, 'id'):
            trackerHyperlink.role = sudsObject.role.id

        trackerHyperlink.uri = sudsObject.uri


    def _mapToSUDS(self):
        sudsObject = self.session.trackerClient.factory.create('tns3:Hyperlink')
        TrackerHyperlink._mapSpecificAttributesToSUDS(self, sudsObject)
        return sudsObject


    @classmethod
    def _mapFromSUDS(cls, session, sudsObject):
        trackerHyperlink = TrackerHyperlink(session)
        TrackerHyperlink._mapSpecificAttributesFromSUDS(sudsObject, trackerHyperlink)
        return trackerHyperlink
