# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from .abstract_polarion_crate import AbstractPolarionCrate

class AbstractTextCrate(AbstractPolarionCrate):
    ''' Common abstraction for various '*:Text' types '''


    def __init__(self, session, content_type='text/html', content='', contentLossy=False):
        AbstractPolarionCrate.__init__(self, session)
        self.content_type = content_type
        self.content      = content
        self.contentLossy = contentLossy
        self._fillMissingValues()


    @classmethod
    def _isLikeNone(cls, t):
        if t == None:
            return True
        if not hasattr(t, 'content'):
            return True
        if not t.content:
            return True
        if t.content.isspace():
            return True
        return False


    @classmethod
    def _staticEquiv(cls, t1, t2):
        e1 = AbstractTextCrate._isLikeNone(t1)
        e2 = AbstractTextCrate._isLikeNone(t2)
        if e1 and e2:
            return True
        if e1 != e2:
            return False
        x1 = '{}'.format(t1.content)
        x2 = '{}'.format(t2.content)
        return x1 == x2


    def _copy(self, another):
        AbstractPolarionCrate._copy(self, another)
        another.content_type = self.content_type
        another.content      = self.content
        another.contentLossy = self.contentLossy
        return another


    def _fillMissingValues(self, project=None, namespace=None):
        super(AbstractTextCrate, self)._fillMissingValues(project, namespace)
        if not self.content_type:
            self.content_type = 'text/html'
        if not self.contentLossy:
            self.contentLossy = False
        return self


    @classmethod
    def _isConvertible(cls, suds_object):
        if suds_object == None:
            return True
        # TODO: verify with WSDLs if some attributes could be omitted
        if not hasattr(suds_object, 'type'):
            return False
        if not hasattr(suds_object, 'content'):
            return False
        if not hasattr(suds_object, 'contentLossy'):
            return False
        return True


    @classmethod
    def _mapSpecificAttributesToSUDS(cls, text, suds_object):
        suds_object.type = text.content_type
        suds_object.content = text.content
        suds_object.contentLossy = text.contentLossy


    @classmethod
    def _mapSpecificAttributesFromSUDS(cls, suds_object, text):
        text.content_type = suds_object.type
        text.content = suds_object.content
        text.contentLossy = suds_object.contentLossy


    def _mapToSUDS(self):
        # override in concrete subclasses
        raise PylarionLibException('Not implemented')


    @classmethod
    def _mapFromSUDS(cls, session, suds_object):
        text = AbstractTextCrate(session)
        AbstractTextCrate._mapSpecificAttributesFromSUDS(suds_object, text)
        return text


from pylarionlib.exceptions import PylarionLibException
