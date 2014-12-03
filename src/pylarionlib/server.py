# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

class Server:

    # no singleton dance by design

    def __init__(self, url, login, password, defaultProject=None, defaultNamespace=None, reLoginTimeout=60):
        # TODO 60 is Mirek's magic constant. Ask him and document.
        self.url = url
        self.login = login
        self.password = password
        self.defaultProject = defaultProject
        self.defaultNamespace = defaultNamespace
        self.reLoginTimeout = reLoginTimeout

    def _createSession(self):
        return session.Session(self)

    def session(self):
        '''
        Provide a context manager with an open session
        '''
        return session.Session(self)._logged()


from . import session