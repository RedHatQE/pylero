# -*- coding: utf8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import re
import ssl
import time

import suds.sax.element
from pylero._compatible import builtins  # noqa
from pylero._compatible import object
from pylero._compatible import urlparse
from suds.plugin import MessagePlugin
from suds.sax.attribute import Attribute


logger = logging.getLogger(__name__)
# We create a logger in order to intercept log records from suds.client
suds_logger = logging.getLogger('suds.client')

CERT_PATH = None

# Regular expression to catch SOAP message containing password field
REGEX_SOAP_MESSAGE_PASSWORD_FIELD = \
        re.compile(r'(<ns\d:password>)(.*)(</ns\d:password>).*')


class ListenFilter(logging.Filter):
    def filter(self, record):
        """Determine which log records to output.
        Returns 0 for no, nonzero for yes.
        """
        # We assume that this message contains the password in plaintext
        # which as part of SOAP message
        if '<ns' and ':password' in record.getMessage():
            masked_record = re.sub(REGEX_SOAP_MESSAGE_PASSWORD_FIELD,
                                   r'\1*********\3',
                                   record.getMessage())
            logger.critical(masked_record)
            return False
        return True


suds_logger.addFilter(ListenFilter())


# the reason why this function definition is at the top is because it is
# assigned to "ssl._create_default_https_context", few lines below
def create_ssl_context():
    """this function creates a custom ssl context which is required for ssl
    connection in python-version >=2.7.10. this ssl context is customize to use
    certificate which is located in 'CERT_PATH'.
    """
    context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    context.verify_mode = ssl.CERT_REQUIRED
    context.check_hostname = True
    context.load_verify_locations(CERT_PATH)
    return context


class SoapNull(MessagePlugin):
    """suds plugin that is called before any suds message is sent to the remote
    server. It adds the xsi:nil=true attribute to any element that is blank.
    Without this plugin, a number of functions that were supposed to accept
    null parameters did not work.
    """

    def marshalled(self, context):
        # Go through every node in the document and check if it is empty and
        # if so set the xsi:nil tag to true
        context.envelope.walk(self.add_nil)

    def add_nil(self, element):
        """Used as a filter function with walk to add xsi:nil to blank attrs.
        """
        if element.isempty() and not element.isnil():
            element.attributes.append(Attribute('xsi:nil', 'true'))


class Session(object):

    def _url_for_name(self, service_name):
        """generate the full URL for the WSDL client services"""
        return '{0}/ws/services/{1}WebService?wsdl'.format(self._server.url,
                                                           service_name)

    def __init__(self, server, timeout):
        """Session constructor, initialize the WSDL clients

           Args:
                server: server object that the session connects to
                caching_policy: determines the caching policy of the SUDS conn
                timeout: HTTP timeout for the connection
        """
        self._server = server
        self._last_request_at = None
        self._session_id_header = None
        self._cookies = None
        self._session_client = _SudsClientWrapper(
            self._url_for_name('Session'), None, timeout)
        self.builder_client = _SudsClientWrapper(
            self._url_for_name('Builder'), self, timeout)
        self.planning_client = _SudsClientWrapper(
            self._url_for_name('Planning'), self, timeout)
        self.project_client = _SudsClientWrapper(
            self._url_for_name('Project'), self, timeout)
        self.security_client = _SudsClientWrapper(
            self._url_for_name('Security'), self, timeout)
        self.test_management_client = _SudsClientWrapper(
            self._url_for_name('TestManagement'), self, timeout)
        self.tracker_client = _SudsClientWrapper(
            self._url_for_name('Tracker'), self, timeout)

        # This block forces ssl certificate verification
        if self._server.cert_path:
            global CERT_PATH
            CERT_PATH = self._server.cert_path
            ssl._create_default_https_context = create_ssl_context

    def _login(self):
        """login to the Polarion API"""
        sc = self._session_client
        sc.service.logIn(self._server.login, self._server.password)
        id_element = sc.last_received(). \
            childAtPath('Envelope/Header/sessionID')
        session_id = id_element.text
        session_ns = id_element.namespace()
        self._session_id_header = suds.sax.element.Element(
            'sessionID', ns=session_ns).setText(session_id)
        self._cookies = sc.options.transport.cookiejar
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

    def tx_in(self):
        """Function checks if a transaction is in progress. You can not have a
        transaction within another transaction. This function helps the system
        determine if it should start a new transaction or if it is already in
        the middle of one.

        Returns:
            bool
        """
        return self._session_client.service.transactionExists()


class _SudsClientWrapper(object):
    """class that manages the WSDL clients"""

    def __init__(self, url, enclosing_session, timeout):
        """has the actual WSDL client as a private _suds_client attribute so
        that the "magic" __getattr__ function will be able to verify
        functions called on it and after processing to call the WSDL function

        Args:
            url (str): the URL of the Polarion server.
            enclosing_session: the HTTP session that the requests are sent
                               through
            timeout (int): The HTTP timeout of the connection
        """
        plugin = SoapNull()
        self._suds_client = suds.client.Client(
            url,
            plugins=[plugin],
            timeout=timeout)
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
            # for some reason adding the cookiejar didn't work, so the
            # cookie is being added to the header manually.
            # self._suds_client.options.transport.cookiejar = \
            #    self._enclosing_session._cookies
            # adding the RouteID cookie, if it exists to the headers.
            hostname = urlparse(self._enclosing_session._server.url).hostname
            route = self._enclosing_session._cookies._cookies \
                .get(hostname, {}).get("/", {}).get("ROUTEID")
            if route:
                self._suds_client.options.headers["Cookie"] = \
                    "ROUTEID=%s" % route.value
        return getattr(self._suds_client, attr)
