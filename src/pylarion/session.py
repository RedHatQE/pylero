# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals

import logging
import time
import suds.sax

# TODO: figure out what this does
logger = logging.getLogger(__name__)


class Session(object):

    def _url_for_name(self, service_name):
        """generate the full URL for the WSDL client services"""
        return '{0}/ws/services/{1}WebService?wsdl'.format(self._server.url,
                                                           service_name)

    def __init__(self, server):
        """Session constructor, initialize the WSDL clients"""
        self._server = server
        self._last_request_at = None
        self._session_id_header = None
        self._session_client = _suds_client_wrapper(
            self._url_for_name('Session'), None)
        self.builder_client = _suds_client_wrapper(
            self._url_for_name('Builder'), self)
        self.planning_client = _suds_client_wrapper(
            self._url_for_name('Planning'), self)
        self.project_client = _suds_client_wrapper(
            self._url_for_name('Project'), self)
        self.security_client = _suds_client_wrapper(
            self._url_for_name('Security'), self)
        self.test_management_client = _suds_client_wrapper(
            self._url_for_name('TestManagement'), self)
        self.tracker_client = _suds_client_wrapper(
            self._url_for_name('Tracker'), self)

    def _login(self):
        """login to the Polarion API"""
        sc = self._session_client
        sc.service.logIn(self._server.login, self._server.password)
        id_element = sc.last_received(). \
            childAtPath('Envelope/Header/sessionID')
        sessionID = id_element.text
        sessionNS = id_element.namespace()
        self._session_id_header = suds.sax.element.Element(
            'sessionID', ns=sessionNS).setText(sessionID)
        sc.set_options(soapheaders=self._session_id_header)
        self._last_request_at = time.time()

    def _logout(self):
        """logout from Polarion server"""
        self._session_client.service.endSession()

    def _reauth(self):
        """auto relogin after timeout, set in the getattr function of each
        client obj
        """
        sc = self._session_client
        duration = time.time() - self._last_request_at
        if duration > self._server.relogin_timeout and not \
                sc.service.hasSubject():
            logger.debug("Session expired, trying to log in again")
            self._login()
        else:
            self._last_request_at = time.time()

    def tx_begin(self):
        self._session_client.service.beginTransaction()

    def tx_commit(self):
        self._session_client.service.endTransaction(False)

    def tx_rollback(self):
        self._session_client.service.endTransaction(True)

    def tx_release(self):
        if self._session_client.service.transactionExists():
            self.tx_rollback()


class _suds_client_wrapper:
    """class that manages the WSDL clients"""

    def __init__(self, url, enclosing_session):
        # has the actual WSDL client as a private _suds_client attribute so
        # that the "magic" __getattr__ function will be able to verify
        # functions called on it and after processing to call the WSDL function
        self._suds_client = suds.client.Client(url)
        self._enclosing_session = enclosing_session

    def __getattr__(self, attr):
        # every time a client function is called, this verifies that there is
        # still an active connection and if not, it reconnects.
        logger.debug("attr={0} self={1}".format(attr, self.__dict__))
        if attr == "service" and self._enclosing_session and \
                self._enclosing_session._session_id_header is not None:
            logger.debug("Calling hook before _suds_client_wrapper.service "
                         "access")
            self._enclosing_session._reauth()
            self._suds_client.set_options(
                soapheaders=self._enclosing_session._session_id_header)
        return getattr(self._suds_client, attr)
