# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import suds

class AbstractPolarionMappingObject:

    def  __init__(self, session):
        self.session = session

    def _copy(self, another):
        another.session = self.session
        return another

    @classmethod
    def _isConvertible(cls, suds_object):
        '''
        Say if the SUDS object can be mapped to self

        Override in subclasses
        '''
        return True

    @classmethod
    def _mapSpecificAttributesToSUDS(cls, abstractPolarionMappingObject, suds_object):
        pass

    @classmethod
    def _mapSpecificAttributesFromSUDS(cls, suds_object, abstractPolarionMappingObject):
        pass

    def _mapToSUDS(self):
        # override in subclasses
        return suds.null()

    @classmethod
    def _mapFromSUDS(cls, session, suds_object):
        # TODO: delegate to subclasses if possible
        return AbstractPolarionMappingObject(session)
