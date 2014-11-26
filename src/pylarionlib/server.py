# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

class Server:

    # no singleton dance by design

    def __init__(self, url, login, password, default_project=None, default_namespace=None, relogin_timeout=60):
        # TODO 60 is Mirek's magic constant. Ask him and document.
        self.url = url
        self.login = login
        self.password = password
        self.default_project = default_project
        self.default_namespace = default_namespace
        self.relogin_timeout = relogin_timeout

    def _createSession(self):
        return session.Session(self)

    def session(self):
        '''
        Provide a context manager with an open session
        '''
        return session.Session(self)._logged()


from . import session