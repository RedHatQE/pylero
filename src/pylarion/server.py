# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals
from pylarion.session import Session


class Server(object):
    """Server object is instantiated once per Polarion session and creates the
    session that is used to connect to the server.
    """

    def __init__(self, url, login, password, default_project=None,
                 default_namespace=None, relogin_timeout=60):
        self.url = url
        self.login = login
        self.password = password
        self.default_project = default_project
        self.default_namespace = default_namespace
        self.relogin_timeout = relogin_timeout

    def session(self):
        return Session(self)
