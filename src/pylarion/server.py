# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals
from pylarion.session import Session


class Server(object):
    """Server object is instantiated once per Polarion session and creates the
    session that is used to connect to the server.
    """

    def __init__(self, url, login, password, default_project=None,
                 relogin_timeout=60, caching_policy=0, timeout=120):
        """An object that defines the properties of the Polarion server to
        connect to.

        Args:
            url: url of the Polarion server
            login: username
            password: password
            default_project: default project to use to for configuarations
            relogin_timeout: timeout after which the session will try to login
                             again
            cachingpolicy: cachingpolicy of the session
            timeout: http tiemout
        """
        self.url = url
        self.login = login
        self.password = password
        self.default_project = default_project
        self.relogin_timeout = relogin_timeout
        self.caching_policy = caching_policy
        self.timeout = timeout

    def session(self):
        return Session(self, self.caching_policy, self.timeout)
