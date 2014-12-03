# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import suds

class AbstractPolarionMappingObject(object):

    def  __init__(self, session):
        self.session = session

    def _copy(self, another):
        another.session = self.session
        return another

    def _fillMissingValues(self, project=None, namespace=None):
        return self

    @classmethod
    def _isConvertible(cls, sudsObject):
        '''
        Say if the SUDS object can be mapped to self

        Override in subclasses
        '''
        return True

    @classmethod
    def _mapSpecificAttributesToSUDS(cls, abstractPolarionMappingObject, sudsObject):
        pass

    @classmethod
    def _mapSpecificAttributesFromSUDS(cls, sudsObject, abstractPolarionMappingObject):
        pass

    def _mapToSUDS(self):
        # override in subclasses
        return suds.null()

    @classmethod
    def _mapFromSUDS(cls, session, sudsObject):
        # TODO: delegate to subclasses if possible
        return AbstractPolarionMappingObject(session)
