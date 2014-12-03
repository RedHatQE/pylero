# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from .abstract_polarion_crate import AbstractPolarionCrate

class AbstractTextCrate(AbstractPolarionCrate):
    ''' Common abstraction for various '*:Text' types '''


    def __init__(self, session, contentType='text/html', content='', contentLossy=False):
        AbstractPolarionCrate.__init__(self, session)
        self.contentType = contentType
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
        another.contentType = self.contentType
        another.content      = self.content
        another.contentLossy = self.contentLossy
        return another


    def _fillMissingValues(self, project=None, namespace=None):
        super(AbstractTextCrate, self)._fillMissingValues(project, namespace)
        if not self.contentType:
            self.contentType = 'text/html'
        if not self.contentLossy:
            self.contentLossy = False
        return self


    @classmethod
    def _isConvertible(cls, sudsObject):
        if sudsObject == None:
            return True
        # TODO: verify with WSDLs if some attributes could be omitted
        if not hasattr(sudsObject, 'type'):
            return False
        if not hasattr(sudsObject, 'content'):
            return False
        if not hasattr(sudsObject, 'contentLossy'):
            return False
        return True


    @classmethod
    def _mapSpecificAttributesToSUDS(cls, text, sudsObject):
        sudsObject.type = text.contentType
        sudsObject.content = text.content
        sudsObject.contentLossy = text.contentLossy


    @classmethod
    def _mapSpecificAttributesFromSUDS(cls, sudsObject, text):
        text.contentType = sudsObject.type
        text.content = sudsObject.content
        text.contentLossy = sudsObject.contentLossy


    def _mapToSUDS(self):
        # override in concrete subclasses
        raise PylarionLibException('Not implemented')


    @classmethod
    def _mapFromSUDS(cls, session, sudsObject):
        text = AbstractTextCrate(session)
        AbstractTextCrate._mapSpecificAttributesFromSUDS(sudsObject, text)
        return text


from pylarionlib.exceptions import PylarionLibException
