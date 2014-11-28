# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from .test_run import TestRun

class SimpleTestRun(TestRun):
    # TODO: see interface.txt for more.

    @classmethod
    def _isConvertible(cls, suds_object):
        if not TestRun._isConvertible(suds_object):
            return False
        # TODO: check for the expected
        return True

    @classmethod
    def _mapFromSUDS(cls, session, suds_object):
        simpleTestRun = SimpleTestRun(session)
        SimpleTestRun._mapSpecificAttributesFromSUDS(suds_object, simpleTestRun)
        return simpleTestRun

    def _mapToSUDS(self):
        suds_object = self.session.test_management_client.factory.create('tns3:TestRun')
        SimpleTestRun._mapSpecificAttributesToSUDS(self, suds_object)
        return suds_object
