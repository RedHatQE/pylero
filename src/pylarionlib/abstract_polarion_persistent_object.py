# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from .abstract_polarion_mapping_object import AbstractPolarionMappingObject

class AbstractPolarionPersistentObject(AbstractPolarionMappingObject):

    def __init__(self, session):
        AbstractPolarionMappingObject.__init__(self, session)
        self.puri = None  # Polarion URI
        self.pid = None  # Polarion ID


    def _copy(self, another):
        AbstractPolarionMappingObject._copy(self, another)
        another.puri = self.puri
        another.pid = self.pid
        return another


    def _fillMissingValues(self, project=None, namespace=None):
        super(AbstractPolarionPersistentObject, self)._fillMissingValues(project, namespace)
        return self


    # mappings from/to SUDS

    @classmethod
    def _isConvertible(cls, suds_object):
        if suds_object == None:
            return False
        # TODO: verify with WSDL if some attributes could be omitted
        if not hasattr(suds_object, '_uri'):
            return False
        if not hasattr(suds_object, 'id'):
            return False
        return True

    @classmethod
    def _mapSpecificAttributesToSUDS(cls, abstractPolarionPersistentObject, suds_object):
        AbstractPolarionMappingObject._mapSpecificAttributesToSUDS(abstractPolarionPersistentObject, suds_object)
        suds_object._uri = abstractPolarionPersistentObject.puri
        suds_object.id = abstractPolarionPersistentObject.pid

    @classmethod
    def _mapSpecificAttributesFromSUDS(cls, suds_object, abstractPolarionPersistentObject):
        AbstractPolarionMappingObject._mapSpecificAttributesFromSUDS(suds_object, abstractPolarionPersistentObject)
        abstractPolarionPersistentObject.puri = suds_object._uri
        abstractPolarionPersistentObject.pid = suds_object.id


    # CRUD:

    def _crudCreate(self, project=None):
        '''
        Create a new object in Polarion from the data in self

        If project == None, use the default project of the current session.
        Return self.

        Override in subclasses.
        '''
        raise exceptions.PylarionLibException('Not implemented')

    def _crudRetrieve(self):
        '''
        Retrieve data from Polarion by self's URI and copy the data to self

        Return self.

        Override in subclasses.
        '''
        raise exceptions.PylarionLibException('Not implemented')

    def _crudUpdate(self):
        '''
        Update the corresponfing data in Polarion with the content of self.

        Find the corresponding object in Polarion (by self's URI) and rewrite
        it with the content of self. Return self.

        Override in subclasses.
        '''
        raise exceptions.PylarionLibException('Not implemented')

    def _crudDelete(self):
        '''
        Delete the corresponding data in Polarion.

        Find the corresponding object in Polarion (by self's URI) and delete
        it. Destroy data in self. Return self.

        Override in subclasses.
        '''
        raise exceptions.PylarionLibException('Not implemented')

from . import exceptions
