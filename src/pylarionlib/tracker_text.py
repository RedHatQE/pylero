# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from .abstract_text_crate import AbstractTextCrate

class TrackerText(AbstractTextCrate):
    ''' A crate to deal with 'tns2:Text' of the Tracker service '''

    def _mapToSUDS(self):
        sudsObject = self.session.trackerClient.factory.create('tns2:Text')
        TrackerText._mapSpecificAttributesToSUDS(self, sudsObject)
        return sudsObject
