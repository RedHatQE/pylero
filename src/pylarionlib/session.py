# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import logging
import time
import suds.sax

logger = logging.getLogger(__name__)


class Session:

    def _urlForName(self, serviceName):
        return '{}/ws/services/{}WebService?wsdl'.format(self._server.url, serviceName)

    def __init__(self, server):
        self._server = server
        self._lastRequestAt = None
        self._sessionIdHeader = None
        self._sessionClient = _SUDSClientWrapper(self._urlForName('Session'), None)
        self.builderClient = _SUDSClientWrapper(self._urlForName('Builder'), self)
        self.planningClient = _SUDSClientWrapper(self._urlForName('Planning'), self)
        self.projectClient = _SUDSClientWrapper(self._urlForName('Project'), self)
        self.securityClient = _SUDSClientWrapper(self._urlForName('Security'), self)
        self.testManagementClient = _SUDSClientWrapper(self._urlForName('TestManagement'), self)
        self.trackerClient = _SUDSClientWrapper(self._urlForName('Tracker'), self)

    def _getDefaultProject(self):
        return self._server.defaultProject

    def _getDefaultNamespace(self):
        return self._server.defaultNamespace

    def _login(self):
        sc = self._sessionClient
        sc.service.logIn(self._server.login, self._server.password)
        idElement = sc.last_received().childAtPath('Envelope/Header/sessionID')
        sessionID = idElement.text
        sessionNS = idElement.namespace()
        self._sessionIdHeader = suds.sax.element.Element('sessionID', ns=sessionNS).setText(sessionID)
        sc.set_options(soapheaders=self._sessionIdHeader)
        self._lastRequestAt = time.time()

    def _logout(self):
        self._sessionClient.service.endSession()

    def _reauth(self):
        sc = self._sessionClient
        duration = time.time() - self._lastRequestAt
        if duration > self._server.reLoginTimeout and not sc.service.hasSubject():
            logger.debug("Session expired, trying to log in again")
            self._login()
        else:
            self._lastRequestAt = time.time()

    def _logged(self):
        return _Logged(self)

    def txBegin(self):
        self._sessionClient.service.beginTransaction()

    def txCommit(self):
        self._sessionClient.service.endTransaction(False)

    def txRollback(self):
        self._sessionClient.service.endTransaction(True)

    def txRelease(self):
        if self._sessionClient.service.transactionExists():
            self.txRollback()

    def transaction(self):
        return _Transaction(self)

    def newFunctionalTestCase(self, project=None,
                              title=None,
                              status=None,
                              description=None,
                              initialEstimate=None,
                              automation=None,
                              scriptURL=None,
                              tags=set(),
                              posNeg=None):
        tc = FunctionalTestCase(self,
                                project=project,
                                title=title,
                                status=status,
                                description=description,
                                initialEstimate=initialEstimate,
                                automation=automation,
                                scriptURL=scriptURL,
                                tags=tags)
        return tc._crudCreate(project)

    def newStructuralTestCase(self, project=None,
                              title=None,
                              status=None,
                              description=None,
                              initialEstimate=None,
                              automation=None,
                              scriptURL=None,
                              tags=set(),
                              posNeg=None):
        tc = StructuralTestCase(self,
                                project=project,
                                title=title,
                                status=status,
                                description=description,
                                initialEstimate=initialEstimate,
                                automation=automation,
                                scriptURL=scriptURL,
                                tags=tags)
        return tc._crudCreate(project)

    def newNonFunctionalTestCase(self, project=None,
                                 title=None,
                                 status=None,
                                 description=None,
                                 initialEstimate=None,
                                 automation=None,
                                 scriptURL=None,
                                 tags=set(),
                                 posNeg=None):
        tc = NonFunctionalTestCase(self,
                                   project=project,
                                   title=title,
                                   status=status,
                                   description=description,
                                   initialEstimate=initialEstimate,
                                   automation=automation,
                                   scriptURL=scriptURL,
                                   tags=tags)
        return tc._crudCreate(project)

    def newTestSuite(self, project=None,
                     title=None,
                     status=None,
                     description=None,
                     initialEstimate=None,
                     automation=None,
                     scriptURL=None,
                     tags=set(),
                     posNeg=None):
        tc = TestSuite(self,
                       project=project,
                       title=title,
                       status=status,
                       description=description,
                       initialEstimate=initialEstimate,
                       automation=automation,
                       scriptURL=scriptURL,
                       tags=tags)
        return tc._crudCreate(project)

    def newSimpleTestPlan(self,
                          project=None,
                          space=None,
                          name=None,
                          initialText=None,
                          parentPlanPURI=None,
                          testCasesPURIs=[]):
        plan = SimpleTestPlan(self,
                              project=project,
                              namespace=space,
                              name=name,
                              initialText=initialText,
                              parentPlanPURI=parentPlanPURI,
                              testCasesPURIs=testCasesPURIs)
        return plan._crudCreate()

    def newSimpleTestRun(self,
                          project=None,
                          status=None,
                          namePrefix=None,
                          testPlanPURI=None,
                          testCasesPURIs=[]):
        run = SimpleTestRun(self,
                            project=project,
                            status=status,
                            namePrefix=namePrefix,
                            testPlanPURI=testPlanPURI,
                            testCasesPURIs=testCasesPURIs)
        return run._crudCreate()

    def getWorkItemByPID(self, pid, project=None):
        if not project:
            project = self._getDefaultProject()
        sudsWorkItem = self.trackerClient.service.getWorkItemById(project, pid)
        if sudsWorkItem._unresolvable:
            return None
        return WorkItem._mapFromSUDS(self, sudsWorkItem)

    def getWorkItemByPURI(self, puri):
        sudsWorkItem = self.trackerClient.service.getWorkItemByUri(puri)
        if sudsWorkItem._unresolvable:
            return None
        return WorkItem._mapFromSUDS(self, sudsWorkItem)

    def getDocumentByPID(self, pid, project=None, namespace=None):
        if not project:
            project = self._getDefaultProject()
        if not namespace:
            namespace = self._getDefaultNamespace()
        if namespace:
            location = '{}/{}'.format(namespace, pid)
        else:
            location = pid
        sudsDocument = self.trackerClient.service.getModuleByLocation(project, location)
        if sudsDocument._unresolvable:
            return None
        return Document._mapFromSUDS(self, sudsDocument)

    def getDocumentByPURI(self, puri):
        sudsDocument = self.trackerClient.service.getModuleByUri(puri)
        if sudsDocument._unresolvable:
            return None
        return Document._mapFromSUDS(self, sudsDocument)

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
            project = self._getDefaultProject()
        sudsTestRun = self.testManagementClient.service.getTestRunById(project, pid)
        if sudsTestRun._unresolvable:
            return None
        return TestRun._mapFromSUDS(self, sudsTestRun)

    def getTestRunByPURI(self, puri):
        sudsTestRun = self.testManagementClient.service.getTestRunByUri(puri)
        if sudsTestRun._unresolvable:
            return None
        return TestRun._mapFromSUDS(self, sudsTestRun)

    def getSimpleTestRunByPID(self, pid, project=None):
        testRun = self.getTestRunByPID(pid, project)
        if testRun and isinstance(testRun, SimpleTestRun):
            return testRun
        else:
            return None

    def getSimpleTestRunByPURI(self, puri):
        testRun = self.getTestRunByPURI(puri)
        if testRun and isinstance(testRun, SimpleTestRun):
            return testRun
        else:
            return None

    # TODO: other data methods


class _SUDSClientWrapper:

    def __init__(self, url, enclosingSession):
        self._sudsClient = suds.client.Client(url)
        self._enclosingSession = enclosingSession

    def __getattr__(self, attr):
        logger.debug("attr={} self={}".format(attr, self.__dict__))
        if attr == "service" and self._enclosingSession and self._enclosingSession._sessionIdHeader != None:
            logger.debug("Calling hook before _SUDSClientWrapper.service access")
            self._enclosingSession._reauth()
            self._sudsClient.set_options(soapheaders=self._enclosingSession._sessionIdHeader)
        return getattr(self._sudsClient, attr)


class _Logged:

    def __init__(self, enclosingSession):
        self._enclosingSession = enclosingSession

    def __enter__(self):
        self._enclosingSession._login()
        return self._enclosingSession

    def __exit__(self, exceptionType, exceptionValue, exceptionTrace):
        self._enclosingSession._logout()


class _Transaction:

    def __init__(self, enclosingSession):
        self._enclosingSession = enclosingSession

    def __enter__(self):
        self._enclosingSession.txBegin()
        return self._enclosingSession

    def __exit__(self, exceptionType, exceptionValue, exceptionTrace):
        try:
            if exceptionValue == None:
                self._enclosingSession.txCommit()
            else:
                self._enclosingSession.txRollback()
        finally:
            self._enclosingSession.txRelease()


from .work_item import WorkItem
from .document import Document
from .simple_test_plan import SimpleTestPlan
from .test_run import TestRun
from .simple_test_run import SimpleTestRun
from .test_classes import FunctionalTestCase, StructuralTestCase, NonFunctionalTestCase, TestSuite
