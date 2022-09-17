# -*- coding: utf8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from pylero._compatible import builtins  # noqa
from pylero._compatible import object
from pylero.session import Session


class Server(object):
    """Server object is instantiated once per Polarion session and creates the
    session that is used to connect to the server.
    """

    def __init__(
        self,
        url,
        login,
        password,
        default_project=None,
        relogin_timeout=60,
        timeout=120,
        cert_path=None,
    ):
        """An object that defines the properties of the Polarion server to
        connect to.

        Args:
            url: url of the Polarion server
            login: username
            password: password
            default_project: default project to use to for configuarations
            relogin_timeout: timeout after which the session will try to login
                             again
            timeout: http tiemout
            cert_path: path to customize CA bundle
        """
        self.url = url
        self.login = login
        self.password = password
        self.default_project = default_project
        self.relogin_timeout = relogin_timeout
        self.timeout = timeout
        self.cert_path = cert_path

    def session(self):
        return Session(self, self.timeout)
