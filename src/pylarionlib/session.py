# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import logging
import time
import suds.sax

logger = logging.getLogger(__name__)


class Session:

    def _url_for_name(self, service_name):
        return '{}/ws/services/{}WebService?wsdl'.format(self._server.url, service_name)

    def __init__(self, server):
        self._server = server
        self._last_request_at = None
        self._session_id_header = None
        self._session_client = _SUDS_Client_Wrapper(self._url_for_name('Session'), None)
        self.builder_client = _SUDS_Client_Wrapper(self._url_for_name('Builder'), self)
        self.planning_client = _SUDS_Client_Wrapper(self._url_for_name('Planning'), self)
        self.project_client = _SUDS_Client_Wrapper(self._url_for_name('Project'), self)
        self.security_client = _SUDS_Client_Wrapper(self._url_for_name('Security'), self)
        self.test_management_client = _SUDS_Client_Wrapper(self._url_for_name('TestManagement'), self)
        self.tracker_client = _SUDS_Client_Wrapper(self._url_for_name('Tracker'), self)

    def _get_default_project(self):
        return self._server.default_project

    def _get_default_namespace(self):
        return self._server.default_namespace

    def _login(self):
        sc = self._session_client
        sc.service.logIn(self._server.login, self._server.password)
        id_element = sc.last_received().childAtPath('Envelope/Header/sessionID')
        session_id = id_element.text
        session_ns = id_element.namespace()
        self._session_id_header = suds.sax.element.Element('sessionID', ns=session_ns).setText(session_id)
        sc.set_options(soapheaders=self._session_id_header)
        self._last_request_at = time.time()

    def _logout(self):
        self._session_client.service.endSession()

    def _reauth(self):
        sc = self._session_client
        duration = time.time() - self._last_request_at
        if duration > self._server.relogin_timeout and not sc.service.hasSubject():
            logger.debug("Session expired, trying to log in again")
            self._login()
        else:
            self._last_request_at = time.time()

    def _logged(self):
        return _Logged(self)

    def txBegin(self):
        self._session_client.service.beginTransaction()

    def txCommit(self):
        self._session_client.service.endTransaction(False)

    def txRollback(self):
        self._session_client.service.endTransaction(True)

    def txRelease(self):
        if self._session_client.service.transactionExists():
            self.txRollback()

    def transaction(self):
        return _Transaction(self)

    def getWorkItemByPID(self, pid, project=None):
        if not project:
            project = self._get_default_project()
        suds_work_item = self.tracker_client.service.getWorkItemById(project, pid)
        if suds_work_item._unresolvable:
            return None
        return WorkItem._mapFromSUDS(self, suds_work_item)

    def getWorkItemByPURI(self, puri):
        suds_work_item = self.tracker_client.service.getWorkItemByUri(puri)
        if suds_work_item._unresolvable:
            return None
        return WorkItem._mapFromSUDS(self, suds_work_item)

    def getDocumentByPID(self, pid, project=None, namespace=None):
        if not project:
            project = self._get_default_project()
        if not namespace:
            namespace = self._get_default_namespace()
        if namespace:
            location = '{}/{}'.format(namespace, pid)
        else:
            location = pid
        suds_document = self.tracker_client.service.getModuleByLocation(project, location)
        if suds_document._unresolvable:
            return None
        return Document._mapFromSUDS(self, suds_document)

    def getDocumentByPURI(self, puri):
        suds_document = self.tracker_client.service.getModuleByUri(puri)
        if suds_document._unresolvable:
            return None
        return Document._mapFromSUDS(self, suds_document)

    def getSimpleTestPlanByPID(self, pid, project=None, namespace=None):
        document = self.getDocumentByPID(pid, project, namespace)
        if document and isinstance(document, SimpleTestPlan):
            return document
        else:
            return None

    def getSimpleTestPlanByPURI(self, puri):
        document = self.getDocumentByPURI(puri)
        if document and isinstance(document, SimpleTestPlan):
            return document
        else:
            return None

    def getTestRunByPID(self, pid, project=None):
        if not project:
            project = self._get_default_project()
        suds_test_run = self.test_management_client.getTestRunById(project, pid)
        if suds_test_run._unresolvable:
            return None
        return TestRun._mapFromSUDS(self, suds_test_run)

    def getTestRunByPURI(self, puri):
        suds_test_run = self.test_management_client.service.getTestRunByUri(puri)
        if suds_test_run._unresolvable:
            return None
        return TestRun._mapFromSUDS(self, suds_test_run)

    def getSimpleTestRunByPID(self, pid, project=None):
        test_run = self.getTestRunByPID(pid, project)
        if test_run and isinstance(test_run, SimpleTestRun):
            return test_run
        else:
            return None

    def getSimpleTestRunByPURI(self, puri):
        test_run = self.getTestRunByPURI(puri)
        if test_run and isinstance(test_run, SimpleTestRun):
            return test_run
        else:
            return None

    # TODO: other data methods


class _SUDS_Client_Wrapper:

    def __init__(self, url, enclosing_session):
        self._suds_client = suds.client.Client(url)
        self._enclosing_session = enclosing_session

    def __getattr__(self, attr):
        logger.debug("attr={} self={}".format(attr, self.__dict__))
        if attr == "service" and self._enclosing_session and self._enclosing_session._session_id_header != None:
            logger.debug("Calling hook before _SUDS_Client_Wrapper.service access")
            self._enclosing_session._reauth()
            self._suds_client.set_options(soapheaders=self._enclosing_session._session_id_header)
        return getattr(self._suds_client, attr)


class _Logged:

    def __init__(self, enclosing_session):
        self._enclosing_session = enclosing_session

    def __enter__(self):
        self._enclosing_session._login()
        return self._enclosing_session

    def __exit__(self, exception_type, exception_value, exception_trace):
        self._enclosing_session._logout()


class _Transaction:

    def __init__(self, enclosing_session):
        self._enclosing_session = enclosing_session

    def __enter__(self):
        self._enclosing_session.txBegin()
        return self._enclosing_session

    def __exit__(self, exception_type, exception_value, exception_trace):
        try:
            if exception_value == None:
                self._enclosing_session.txCommit()
            else:
                self._enclosing_session.txRollback()
        finally:
            self._enclosing_session.txRelease()


from .work_item import WorkItem
from .document import Document
from .simple_test_plan import SimpleTestPlan
from .test_run import TestRun
from .simple_test_run import SimpleTestRun
