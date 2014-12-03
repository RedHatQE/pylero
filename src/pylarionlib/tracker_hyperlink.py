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
        retval = session.tracker_client.factory.create('tns3:EnumOptionId')
        retval.id = role
        return retval


    @classmethod
    def _isConvertible(cls, suds_object):
        if suds_object == None:
            return False
        if hasattr(suds_object, 'role') and not hasattr(suds_object.role, 'id'):
            return False
        return True


    @classmethod
    def _mapSpecificAttributesToSUDS(cls, trackerHyperlink, suds_object):
        suds_object.role = TrackerHyperlink._createRoleSUDSObjects(trackerHyperlink.session, trackerHyperlink.role)
        suds_object.uri = trackerHyperlink.uri


    @classmethod
    def _mapSpecificAttributesFromSUDS(cls, suds_object, trackerHyperlink):

        trackerHyperlink.role = None
        if hasattr(suds_object, 'role') and hasattr(suds_object.role, 'id'):
            trackerHyperlink.role = suds_object.role.id

        trackerHyperlink.uri = suds_object.uri


    def _mapToSUDS(self):
        sudsObject = self.session.tracker_client.factory.create('tns3:Hyperlink')
        TrackerHyperlink._mapSpecificAttributesToSUDS(self, sudsObject)
        return sudsObject


    @classmethod
    def _mapFromSUDS(cls, session, suds_object):
        trackerHyperlink = TrackerHyperlink(session)
        TrackerHyperlink._mapSpecificAttributesFromSUDS(suds_object, trackerHyperlink)
        return trackerHyperlink
