# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from .abstract_text_crate import AbstractTextCrate

class TestManagementText(AbstractTextCrate):
    ''' A crate to deal with 'tns2:Text' of the TestManagement service '''

    def _mapToSUDS(self):
        sudsObject = self.session.test_management_client.factory.create('tns2:Text')
        TestManagementText._mapSpecificAttributesToSUDS(self, sudsObject)
        return sudsObject
