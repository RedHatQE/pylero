# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from .abstract_polarion_crate import AbstractPolarionCrate

class TrackerText(AbstractPolarionCrate):
    ''' A crate to deal with 'tns2:Text' of the Tracker service '''


    def __init__(self, session, content_type='text/html', content='', contentLossy=False):
        AbstractPolarionCrate.__init__(self, session)
        self.content_type = content_type
        self.content      = content
        self.contentLossy = contentLossy


    def _copy(self, another):
        AbstractPolarionCrate._copy(self, another)
        another.content_type = self.content_type
        another.content      = self.content
        another.contentLossy = self.contentLossy
        return another


    @classmethod
    def _isConvertible(cls, suds_object):
        if suds_object == None:
            return True
        # TODO: verify with WSDL if some attributes could be omitted
        if not hasattr(suds_object, 'type'):
            return False
        if not hasattr(suds_object, 'content'):
            return False
        if not hasattr(suds_object, 'contentLossy'):
            return False
        return True


    @classmethod
    def _mapSpecificAttributesToSUDS(cls, trackerText, suds_object):
        suds_object.type = trackerText.content_type
        suds_object.content = trackerText.content
        suds_object.contentLossy = trackerText.contentLossy


    @classmethod
    def _mapSpecificAttributesFromSUDS(cls, suds_object, trackerText):
        trackerText.content_type = suds_object.type 
        trackerText.content = suds_object.content
        trackerText.contentLossy = suds_object.contentLossy 


    def _mapToSUDS(self):
        sudsObject = self.session.tracker_client.factory.create('tns2:Text')
        TrackerText._mapSpecificAttributesToSUDS(self, sudsObject)
        return sudsObject
    

    @classmethod
    def _mapFromSUDS(cls, session, suds_object):
        trackerText = TrackerText(session)
        TrackerText._mapSpecificAttributesFromSUDS(suds_object, trackerText)
        return trackerText
