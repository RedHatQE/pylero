#!/usr/bin/env python
# -*- coding: utf8 -*-

# A temporary, just-show-something-thing before proper testing code arises.

from __future__ import absolute_import, division, print_function, unicode_literals

import datetime
import random
import unittest

from pylarionlib.server import Server
from pylarionlib.test_classes import FunctionalTestCase, StructuralTestCase, NonFunctionalTestCase, TestSuite
from pylarionlib.document import Document
from pylarionlib.simple_test_plan import SimpleTestPlan
from pylarionlib.test_run import TestRun
from pylarionlib.simple_test_run import SimpleTestRun
from pylarionlib.test_record import TestRecord
from pylarionlib.tracker_text import TrackerText
from pylarionlib.embedding import _yamlToText, _textToYAML, _SimpleTestPlanTextEmbedding, _SimpleTestRunTextEmbedding
from pylarionlib.test_management_text import TestManagementText
from pylarionlib.test_classes import AbstractTest

my_login = 'vkadlcik'
my_password = '94rskco.kftg9'
my_project_name = 'BrnoTraining'
my_space = 'vkadlcik_spejs'
my_server = Server('http://polarion.dqe.lab.eng.bos.redhat.com/polarion', my_login, my_password, my_project_name)


class TestWorkItemCRUD(unittest.TestCase):

    test_session = None

    @classmethod
    def setUpClass(cls):
        super(TestWorkItemCRUD, cls).setUpClass()
        TestWorkItemCRUD.test_session = my_server._createSession()
        TestWorkItemCRUD.test_session._login()

    @classmethod
    def tearDownClass(cls):
        TestWorkItemCRUD.test_session._logout()
        super(TestWorkItemCRUD, cls).tearDownClass()

    def test_0001(self):
        permanent_title = 'vaskovo uzitkovy test 1'
        tc = FunctionalTestCase(TestWorkItemCRUD.test_session)
        tc.title = permanent_title
        tc._crudCreate()
        self.assertTrue(tc.puri.startswith('subterra:data-service:objects:'))
        self.assertEqual(permanent_title, tc.title)
        tc.title = 'tajna zmena v titulku!'
        self.assertNotEqual(permanent_title, tc.title)
        tc._crudRetrieve()
        self.assertEqual(permanent_title, tc.title)

    def test_0002(self):
        old_title = 'vaskovo stavebni test 1'
        new_title = 'zmena v titulku!'
        tc = StructuralTestCase(TestWorkItemCRUD.test_session)
        tc.title = old_title
        tc._crudCreate()
        self.assertTrue(tc.puri.startswith('subterra:data-service:objects:'))
        self.assertEqual(old_title, tc.title)
        tc.title = new_title
        self.assertEqual(new_title, tc.title)
        tc._crudUpdate()
        self.assertEqual(new_title, tc.title)
        tc._crudRetrieve()
        self.assertEqual(new_title, tc.title)

    def test_0003(self):
        title = 'vaskovo neuzitkovy test 1'
        tc1 = NonFunctionalTestCase(TestWorkItemCRUD.test_session)
        tc1.title = title
        tc1._crudCreate()
        self.assertTrue(tc1.puri.startswith('subterra:data-service:objects:'))
        pid = tc1.pid
        tc2 = TestWorkItemCRUD.test_session.getWorkItemByPID(pid)
        self.assertEqual(title, tc2.title)
        self.assertIsInstance(tc2, NonFunctionalTestCase)
        self.assertEqual(tc1.title, tc2.title)
        self.assertIsNone(tc2.scriptURL)

    def test_0004(self):
        surl1 = 'http://example.com/1'
        surl2 = 'http://example.com/2'
        automation1 = AbstractTest.AutomationConstants.VALUE_AUTOMATED
        automation2 = AbstractTest.AutomationConstants.VALUE_MANUAL_ONLY
        tags1 = set(['Maharaja', 'Dhiraya', 'Bir', 'Bikram', 'Shah', 'Deva'])
        tags2 = set(['Mobutu', 'Sese', 'Seko', 'Kuku', 'Ngbanda', 'Wa', 'Za', 'Banga'])
        tc1 = TestSuite(TestWorkItemCRUD.test_session)
        tc1.title = 'vaskovo testovy pruvod'
        tc1.scriptURL = surl1
        tc1._crudCreate()
        tc2 = TestWorkItemCRUD.test_session.getWorkItemByPURI(tc1.puri)
        self.assertEqual(tc1.puri, tc2.puri)
        self.assertEqual(tc1.pid, tc2.pid)
        self.assertEqual(tc1.__class__, tc2.__class__)
        self.assertEqual(surl1, tc1.scriptURL)
        self.assertEqual(surl1, tc2.scriptURL)
        self.assertIsNone(tc1.automation)
        self.assertIsNone(tc2.automation)
        self.assertEqual(set(), tc1.tags)
        self.assertEqual(set(), tc2.tags)
        tc2.scriptURL = surl2
        tc2.automation = automation1
        tc2.tags = tags1
        tc2._crudUpdate()
        tc3 = TestWorkItemCRUD.test_session.getWorkItemByPURI(tc2.puri)
        self.assertEqual(surl2, tc2.scriptURL)
        self.assertEqual(surl2, tc3.scriptURL)
        self.assertEqual(automation1, tc2.automation)
        self.assertEqual(automation1, tc3.automation)
        self.assertEqual(tags1, tc2.tags)
        self.assertEqual(tags1, tc3.tags)
        tc3.scriptURL = None
        tc3.automation = None
        tc3.tags = set()
        tc3._crudUpdate()
        tc4 = TestWorkItemCRUD.test_session.getWorkItemByPURI(tc3.puri)
        self.assertIsNone(tc3.scriptURL)
        self.assertIsNone(tc4.scriptURL)
        self.assertIsNone(tc3.automation)
        self.assertIsNone(tc4.automation)
        self.assertEqual(set(), tc3.tags)
        self.assertEqual(set(), tc4.tags)
        tc4.scriptURL = surl1
        tc4.automation = automation2
        tc4.tags = tags2
        tc4._crudUpdate()
        tc5 = TestWorkItemCRUD.test_session.getWorkItemByPURI(tc4.puri)
        self.assertEqual(surl1, tc4.scriptURL)
        self.assertEqual(surl1, tc5.scriptURL)
        self.assertEqual(automation2, tc4.automation)
        self.assertEqual(automation2, tc5.automation)
        self.assertEqual(tags2, tc4.tags)
        self.assertEqual(tags2, tc5.tags)


class TestDocumentCRUD(unittest.TestCase):

    test_session = None

    @classmethod
    def setUpClass(cls):
        super(TestDocumentCRUD, cls).setUpClass()
        TestDocumentCRUD.test_session = my_server._createSession()
        TestDocumentCRUD.test_session._login()

    @classmethod
    def tearDownClass(cls):
        TestDocumentCRUD.test_session._logout()
        super(TestDocumentCRUD, cls).tearDownClass()

    def test_0001(self):

        name = 'vaskovo dokument'

        old = TestDocumentCRUD.test_session.getDocumentByPID(name, namespace=my_space)
        if old:
            old._crudDelete()

        permanent_name = name

        doc = Document(TestDocumentCRUD.test_session)
        doc.namespace = my_space
        doc.structureLinkRole = 'parent'
        doc.name = permanent_name
        doc.workItemTypes = [ 'functionaltestcase', 'unittestcase' ]
        doc.text = TrackerText(TestDocumentCRUD.test_session, 'text/html', 'cokoliv', False)

        doc._crudCreate()

        self.assertTrue(doc.puri.startswith('subterra:data-service:objects:'))
        self.assertEqual(permanent_name, doc.name)
        doc.name = 'tajna zmena v titulku!'
        self.assertNotEqual(permanent_name, doc.name)

        doc._crudRetrieve()

        self.assertEqual(permanent_name, doc.name)

        newContent = 'It is a tale - Told by an idiot, full of sound and fury - Signifying nothing.'
        self.assertNotEqual(newContent, doc.text.content)
        doc.text.content = newContent

        doc._crudUpdate()

        self.assertEqual(newContent, doc.text.content)

        refreshed = TestDocumentCRUD.test_session.getDocumentByPURI(doc.puri)
        self.assertEqual(newContent, refreshed.text.content)

        refreshed._crudDelete()

        self.assertIsNone(refreshed.puri)
        self.assertIsNone(TestDocumentCRUD.test_session.getDocumentByPURI(doc.puri))


class TestSimpleTestPlanCRUD(unittest.TestCase):

    test_session = None

    @classmethod
    def setUpClass(cls):
        super(TestSimpleTestPlanCRUD, cls).setUpClass()
        TestSimpleTestPlanCRUD.test_session = my_server._createSession()
        TestSimpleTestPlanCRUD.test_session._login()

    @classmethod
    def tearDownClass(cls):
        TestSimpleTestPlanCRUD.test_session._logout()
        super(TestSimpleTestPlanCRUD, cls).tearDownClass()

    def test_0001(self):

        name = 'vaskovo dokument'

        old = TestSimpleTestPlanCRUD.test_session.getDocumentByPID(name, namespace=my_space)
        if old:
            old._crudDelete()

        permanent_name = name

        doc = SimpleTestPlan(TestSimpleTestPlanCRUD.test_session)
        doc.namespace = my_space
        doc.structureLinkRole = 'parent'
        doc.name = permanent_name

        doc._crudCreate()

        self.assertTrue(doc.puri.startswith('subterra:data-service:objects:'))
        self.assertEqual(permanent_name, doc.name)
        doc.name = 'tajna zmena v titulku!'
        self.assertNotEqual(permanent_name, doc.name)

        doc._crudRetrieve()

        self.assertEqual(permanent_name, doc.name)

        newContent = 'It is a tale - Told by an idiot,\nfull of sound and fury - Signifying nothing.\n{}'.format(doc.text.content)
        self.assertNotEqual(newContent, doc.text.content)
        doc.text.content = newContent

        doc._crudUpdate()

        self.assertEqual(newContent, doc.text.content)

        refreshed = TestSimpleTestPlanCRUD.test_session.getSimpleTestPlanByPURI(doc.puri)
        self.assertEqual(newContent, refreshed.text.content)

        refreshed._crudDelete()

        self.assertIsNone(refreshed.puri)
        self.assertIsNone(TestSimpleTestPlanCRUD.test_session.getSimpleTestPlanByPURI(doc.puri))


def _gen_run_id(cls):
    # TODO: make this function not so lame
    _gen_run_id.counter += 1
    return '{}_{}_{}_{}'.format(
                                      cls.test_session._server.login,
                                      datetime.datetime.now().strftime('%Y-%m-%d__%H_%M_%S'),
                                      _gen_run_id.counter,
                                      random.random()
                                      ).replace('.', '')
_gen_run_id.counter = 0


class TestTestRunCRUD(unittest.TestCase):

    test_session = None

    @classmethod
    def setUpClass(cls):
        super(TestTestRunCRUD, cls).setUpClass()
        TestTestRunCRUD.test_session = my_server._createSession()
        TestTestRunCRUD.test_session._login()

    @classmethod
    def tearDownClass(cls):
        TestTestRunCRUD.test_session._logout()
        super(TestTestRunCRUD, cls).tearDownClass()

    def test_0001(self):

        permanent_status = TestRun.Status.IN_PROGRESS

        testRun = TestRun(TestTestRunCRUD.test_session)
        testRun.pid = _gen_run_id(TestTestRunCRUD)
        testRun.status = permanent_status

        testRun._crudCreate()

        self.assertTrue(testRun.puri.startswith('subterra:data-service:objects:'))
        self.assertEqual(permanent_status, testRun.status)
        testRun.status = TestRun.Status.FINISHED
        self.assertNotEqual(permanent_status, testRun.status)

        testRun._crudRetrieve()

        self.assertEqual(permanent_status, testRun.status)

        new_status = _gen_run_id(TestTestRunCRUD)
        self.assertNotEqual(new_status, testRun.status)
        testRun.status = new_status

        testRun._crudUpdate()

        self.assertEqual(new_status, testRun.status)

        refreshed = TestTestRunCRUD.test_session.getTestRunByPURI(testRun.puri)
        self.assertEqual(new_status, refreshed.status)


class TestSimpleTestRunCRUD(unittest.TestCase):

    test_session = None

    @classmethod
    def setUpClass(cls):
        super(TestSimpleTestRunCRUD, cls).setUpClass()
        TestSimpleTestRunCRUD.test_session = my_server._createSession()
        TestSimpleTestRunCRUD.test_session._login()

    @classmethod
    def tearDownClass(cls):
        TestSimpleTestRunCRUD.test_session._logout()
        super(TestSimpleTestRunCRUD, cls).tearDownClass()

    def test_0001(self):

        permanent_status = SimpleTestRun.Status.NOT_RUN

        simpleTestRun = SimpleTestRun(TestSimpleTestRunCRUD.test_session)
        simpleTestRun.pid = _gen_run_id(TestSimpleTestRunCRUD)
        simpleTestRun.status = permanent_status

        simpleTestRun._crudCreate()

        self.assertTrue(simpleTestRun.puri.startswith('subterra:data-service:objects:'))
        self.assertEqual(permanent_status, simpleTestRun.status)
        simpleTestRun.status = SimpleTestRun.Status.FINISHED
        self.assertNotEqual(permanent_status, simpleTestRun.status)

        simpleTestRun._crudRetrieve()

        self.assertEqual(permanent_status, simpleTestRun.status)

        new_status = SimpleTestRun.Status.IN_PROGRESS
        self.assertNotEqual(new_status, simpleTestRun.status)
        simpleTestRun.status = new_status

        simpleTestRun._crudUpdate()

        self.assertEqual(new_status, simpleTestRun.status)

        refreshed = TestSimpleTestRunCRUD.test_session.getTestRunByPURI(simpleTestRun.puri)
        self.assertEqual(new_status, refreshed.status)


class TestSimpleTestPlansLinking(unittest.TestCase):

    test_session = None

    @classmethod
    def setUpClass(cls):
        super(TestSimpleTestPlansLinking, cls).setUpClass()
        TestSimpleTestPlansLinking.test_session = my_server._createSession()
        TestSimpleTestPlansLinking.test_session._login()

    @classmethod
    def tearDownClass(cls):
        TestSimpleTestPlansLinking.test_session._logout()
        super(TestSimpleTestPlansLinking, cls).tearDownClass()

    @classmethod
    def _referred(cls, puri):
        refreshed = SimpleTestPlan(TestSimpleTestPlansLinking.test_session)
        refreshed.puri = puri
        refreshed._crudRetrieve()
        return refreshed._getParentPlanURI()

    def test_0001(self):

        name_general = 'demo general plan 1'
        name_child_1 = 'demo child plan 1'
        name_child_2 = 'demo child plan 2'
        name_grand_child = 'demo grand child plan'
        all_names = [name_general, name_child_1, name_child_2, name_grand_child]

        plans = {}

        # create fresh new, not linked test plans
        for name in all_names:

            # delete if exists
            doc = TestSimpleTestPlansLinking.test_session.getDocumentByPID(name, namespace=my_space)
            if doc:
                doc._crudDelete()

            # create new
            doc = SimpleTestPlan(TestSimpleTestPlansLinking.test_session)
            doc.namespace = my_space
            doc.structureLinkRole = 'parent'
            doc.name = name
            doc._crudCreate()

            # remember
            plans[name] = doc

        # retrieve the test plans and verify no links there
        for name in all_names:
            self.assertIsNone(plans[name]._crudRetrieve()._getParentPlanURI())

        # set the links among the plans
        plans[name_child_1]._setParentPlanURI(plans[name_general].puri)
        plans[name_child_1]._crudUpdate()
        plans[name_child_2]._setParentPlanURI(plans[name_general].puri)
        plans[name_child_2]._crudUpdate()
        plans[name_grand_child]._setParentPlanURI(plans[name_child_1].puri)
        plans[name_grand_child]._crudUpdate()

        # verify the links
        self.assertIsNone(TestSimpleTestPlansLinking._referred(plans[name_general].puri))
        self.assertEqual(plans[name_general].puri, TestSimpleTestPlansLinking._referred(plans[name_child_1].puri))
        self.assertEqual(plans[name_general].puri, TestSimpleTestPlansLinking._referred(plans[name_child_2].puri))
        self.assertEqual(plans[name_child_1].puri, TestSimpleTestPlansLinking._referred(plans[name_grand_child].puri))

        # change the links among the plans
        plans[name_child_1]._setParentPlanURI(None)
        plans[name_child_1]._crudUpdate()
        plans[name_grand_child]._setParentPlanURI(plans[name_child_2].puri)
        plans[name_grand_child]._crudUpdate()

        # verify the links
        self.assertIsNone(TestSimpleTestPlansLinking._referred(plans[name_general].puri))
        self.assertIsNone(TestSimpleTestPlansLinking._referred(plans[name_child_1].puri))
        self.assertEqual(plans[name_general].puri, TestSimpleTestPlansLinking._referred(plans[name_child_2].puri))
        self.assertEqual(plans[name_child_2].puri, TestSimpleTestPlansLinking._referred(plans[name_grand_child].puri))


class TestSimpleTestRunsLinking(unittest.TestCase):

    test_session = None

    @classmethod
    def setUpClass(cls):
        super(TestSimpleTestRunsLinking, cls).setUpClass()
        TestSimpleTestRunsLinking.test_session = my_server._createSession()
        TestSimpleTestRunsLinking.test_session._login()

    @classmethod
    def tearDownClass(cls):
        TestSimpleTestRunsLinking.test_session._logout()
        super(TestSimpleTestRunsLinking, cls).tearDownClass()

    @classmethod
    def _referred(cls, puri):
        refreshed = SimpleTestRun(TestSimpleTestRunsLinking.test_session)
        refreshed.puri = puri
        refreshed._crudRetrieve()
        return refreshed.testPlanURI

    def test_0001(self):

        name_plan_1 = 'demo plan 1'
        name_plan_2 = 'demo plan 2'
        all_names = [name_plan_1, name_plan_2]

        plans = {}

        # create fresh new, not linked test plans
        for name in all_names:

            # delete if exists
            doc = TestSimpleTestRunsLinking.test_session.getDocumentByPID(name, namespace=my_space)
            if doc:
                doc._crudDelete()

            # create new
            doc = SimpleTestPlan(TestSimpleTestRunsLinking.test_session)
            doc.namespace = my_space
            doc.structureLinkRole = 'parent'
            doc.name = name
            doc._crudCreate()

            # remember
            plans[name] = doc

        # create new simple runs, not linked
        run1 = SimpleTestRun(TestSimpleTestRunsLinking.test_session)
        run1.pid = _gen_run_id(TestSimpleTestRunsLinking)
        run1.testPlanURI = plans[name_plan_2].puri
        run1._crudCreate()
        run2 = SimpleTestRun(TestSimpleTestRunsLinking.test_session)
        run2.pid = _gen_run_id(TestSimpleTestRunsLinking)
        run2._crudCreate()
        run3 = SimpleTestRun(TestSimpleTestRunsLinking.test_session)
        run3.pid = _gen_run_id(TestSimpleTestRunsLinking)
        run3._crudCreate()

        # verify how linked
        self.assertEquals(plans[name_plan_2].puri, TestSimpleTestRunsLinking._referred(run1.puri))
        self.assertIsNone(TestSimpleTestRunsLinking._referred(run2.puri))
        self.assertIsNone(TestSimpleTestRunsLinking._referred(run3.puri))

        # set the links
        run1.testPlanURI = plans[name_plan_1].puri; run1._crudUpdate()
        run2.testPlanURI = plans[name_plan_2].puri; run2._crudUpdate()
        run3.testPlanURI = plans[name_plan_1].puri; run3._crudUpdate()

        # verify linked
        self.assertEqual(plans[name_plan_1].puri, TestSimpleTestRunsLinking._referred(run1.puri))
        self.assertEqual(plans[name_plan_2].puri, TestSimpleTestRunsLinking._referred(run2.puri))
        self.assertEqual(plans[name_plan_1].puri, TestSimpleTestRunsLinking._referred(run3.puri))

        # switch the links
        run1.testPlanURI = plans[name_plan_2].puri; run1._crudUpdate()
        run2.testPlanURI = plans[name_plan_1].puri; run2._crudUpdate()
        run3.testPlanURI = plans[name_plan_2].puri; run3._crudUpdate()

        # verify linked
        self.assertEqual(plans[name_plan_2].puri, TestSimpleTestRunsLinking._referred(run1.puri))
        self.assertEqual(plans[name_plan_1].puri, TestSimpleTestRunsLinking._referred(run2.puri))
        self.assertEqual(plans[name_plan_2].puri, TestSimpleTestRunsLinking._referred(run3.puri))

        # unset the links
        run1.testPlanURI = None; run1._crudUpdate()
        run2.testPlanURI = None; run2._crudUpdate()
        run3.testPlanURI = None; run3._crudUpdate()

        # verify not linked
        self.assertIsNone(TestSimpleTestRunsLinking._referred(run1.puri))
        self.assertIsNone(TestSimpleTestRunsLinking._referred(run2.puri))
        self.assertIsNone(TestSimpleTestRunsLinking._referred(run3.puri))


class TestSimpleTestPlanWorkItemOps(unittest.TestCase):

    test_session = None

    @classmethod
    def setUpClass(cls):
        super(TestSimpleTestPlanWorkItemOps, cls).setUpClass()
        TestSimpleTestPlanWorkItemOps.test_session = my_server._createSession()
        TestSimpleTestPlanWorkItemOps.test_session._login()

    @classmethod
    def tearDownClass(cls):
        TestSimpleTestPlanWorkItemOps.test_session._logout()
        super(TestSimpleTestPlanWorkItemOps, cls).tearDownClass()

    def test_0001(self):

        tc1 = FunctionalTestCase(TestSimpleTestPlanWorkItemOps.test_session)
        tc1.title = 'fc 1'
        tc1._crudCreate()

        tc2 = FunctionalTestCase(TestSimpleTestPlanWorkItemOps.test_session)
        tc2.title = 'fc 2'
        tc2._crudCreate()

        tc3 = FunctionalTestCase(TestSimpleTestPlanWorkItemOps.test_session)
        tc3.title = 'fc 3'
        tc3._crudCreate()

        self.assertIsNotNone(tc1.puri)
        self.assertIsNotNone(tc2.puri)
        self.assertIsNotNone(tc3.puri)

        name = 'my completely new test spec 1'
        doc = TestSimpleTestPlanWorkItemOps.test_session.getDocumentByPID(name, namespace=my_space)
        if doc:
            doc._crudDelete()
        doc = SimpleTestPlan(TestSimpleTestPlanWorkItemOps.test_session)
        doc.namespace = my_space
        doc.structureLinkRole = 'parent'
        doc.name = name
        doc._crudCreate()

        refreshed = TestSimpleTestPlanWorkItemOps.test_session.getDocumentByPURI(doc.puri)
        self.assertEqual(0, len(refreshed._getTestCaseURIs()))

        doc._addTestCaseURI(tc1.puri)
        doc._addTestCaseURI(tc2.puri)
        doc._crudUpdate()

        refreshed = TestSimpleTestPlanWorkItemOps.test_session.getDocumentByPURI(doc.puri)
        self.assertEqual(2, len(refreshed._getTestCaseURIs()))
        self.assertTrue(tc1.puri in refreshed._getTestCaseURIs())
        self.assertTrue(tc2.puri in refreshed._getTestCaseURIs())

        doc._deleteTestCaseURI(tc1.puri)
        doc._addTestCaseURI(tc3.puri)
        doc._crudUpdate()

        refreshed = TestSimpleTestPlanWorkItemOps.test_session.getDocumentByPURI(doc.puri)
        self.assertEqual(2, len(refreshed._getTestCaseURIs()))
        self.assertTrue(tc2.puri in refreshed._getTestCaseURIs())
        self.assertTrue(tc3.puri in refreshed._getTestCaseURIs())

        doc._addTestCaseURI(tc3.puri)
        doc._crudUpdate()

        refreshed = TestSimpleTestPlanWorkItemOps.test_session.getDocumentByPURI(doc.puri)
        self.assertEqual(2, len(refreshed._getTestCaseURIs()))
        self.assertTrue(tc2.puri in refreshed._getTestCaseURIs())
        self.assertTrue(tc3.puri in refreshed._getTestCaseURIs())

        doc._deleteAllTestCaseURIs()
        doc._crudUpdate()

        refreshed = TestSimpleTestPlanWorkItemOps.test_session.getDocumentByPURI(doc.puri)
        self.assertEqual(0, len(refreshed._getTestCaseURIs()))


class TestSimpleTestRunRecordOps(unittest.TestCase):

    test_session = None

    @classmethod
    def setUpClass(cls):
        super(TestSimpleTestRunRecordOps, cls).setUpClass()
        TestSimpleTestRunRecordOps.test_session = my_server._createSession()
        TestSimpleTestRunRecordOps.test_session._login()

    @classmethod
    def tearDownClass(cls):
        TestSimpleTestRunRecordOps.test_session._logout()
        super(TestSimpleTestRunRecordOps, cls).tearDownClass()

    def test_0001(self):

        session = TestSimpleTestRunRecordOps.test_session

        tc1 = FunctionalTestCase(session)
        tc1.title = 'fc 1'
        tc1._crudCreate()
        self.assertIsNotNone(tc1.puri)
        tr1 = TestRecord(session, tc1.puri)

        tc2 = FunctionalTestCase(session)
        tc2.title = 'fc 2'
        tc2._crudCreate()
        self.assertIsNotNone(tc2.puri)
        tr2 = TestRecord(session, tc2.puri)

        tc3 = FunctionalTestCase(session)
        tc3.title = 'fc 3'
        tc3._crudCreate()
        self.assertIsNotNone(tc3.puri)
        tr3 = TestRecord(session, tc3.puri)

        run = SimpleTestRun(session)
        run.pid = _gen_run_id(TestSimpleTestRunRecordOps)
        run._crudCreate()

        self.assertEqual(0, len(run.testRecords))

        run.testRecords = [tr1, tr2]; run._crudUpdate()
        self.assertEqual(2, len(run.testRecords))

        tr3.comment = TestManagementText(session, content_type='text/html', content='screwed!', contentLossy=False)
        tr3.duration = 3.14
        tr3.executed = datetime.datetime.now()
        self.result = TestRecord.Status.FAILED

        run.testRecords = [tr3]; run._crudUpdate()
        self.assertEqual(1, len(run.testRecords))

        tr = run.testRecords[0]
        self.assertEqual(tr3.testCaseURI, tr.testCaseURI)
        self.assertEqual(tr3.result, tr.result)
        self.assertEqual(tr3.comment.content, tr.comment.content)
        self.assertEqual(tr3.comment.content_type, tr.comment.content_type)
        self.assertEqual(tr3.comment.contentLossy, tr.comment.contentLossy)
        self.assertTrue(abs((tr3.executed - tr.executed).total_seconds()) <= 120.0)  # SUDS not 100% inaccurate?
        self.assertEqual(tr3.duration, tr.duration)

        run = SimpleTestRun(session)
        run.pid = _gen_run_id(TestSimpleTestRunRecordOps)
        run.testRecords = [tr1, tr2]
        run._crudCreate()
        self.assertEqual(2, len(run.testRecords))


class TestRawEmbedding(unittest.TestCase):

    def testBackAndForth(self):
        text1 = '''Creeps in this petty pace from day to day,
To the last syllable of recorded time;
[pylarion-structured-field-start]  
header:
  subject: pylarion
  formatVersion: 0.0
  dataType: SimpleTestPlan
data:
  parentPlan:
    uri: subterra:data-service:objects:...
[pylarion-structured-field-end]
And all our yesterdays have lighted fools
The way to dusty death. Out, out, brief candle!
'''
        yamlObject1, prefix1, suffix1 = _textToYAML(text1)

        self.assertEqual('pylarion', yamlObject1['header']['subject'])
        self.assertEqual(0.0, yamlObject1['header']['formatVersion'])
        self.assertEqual('SimpleTestPlan', yamlObject1['header']['dataType'])
        self.assertEqual('subterra:data-service:objects:...', yamlObject1['data']['parentPlan']['uri'])

        text2 = _yamlToText(yamlObject1, prefix1, suffix1)

        lines = text2.splitlines()
        self.assertEqual('Creeps in this petty pace from day to day,', lines[0])
        self.assertEqual('To the last syllable of recorded time;', lines[1])
        self.assertEqual('[pylarion-structured-field-start]', lines[2])
        self.assertEqual('[pylarion-structured-field-end]', lines[-3])
        self.assertEqual('And all our yesterdays have lighted fools', lines[-2])
        self.assertEqual('The way to dusty death. Out, out, brief candle!', lines[-1])

        yamlObject2, prefix2, suffix2 = _textToYAML(text2)
        self.assertEqual(yamlObject1, yamlObject2)
        self.assertEqual(prefix1, prefix2)
        self.assertEqual(suffix1, suffix2)

    def testNotInstantiable_0001(self):
        text = '''Hello world'''
        self.assertIsNone(_SimpleTestPlanTextEmbedding.instantiateFromText(text))
        self.assertIsNone(_SimpleTestRunTextEmbedding.instantiateFromText(text))

    def testRootSimpleTestPlanTextEmbedding(self):
        text = '''[pylarion-structured-field-start]  
header:
  subject: pylarion
  formatVersion: 0.0
  dataType: SimpleTestPlan
data:
  parentPlan:
    uri: 
[pylarion-structured-field-end]
trailing text
'''
        instance = _SimpleTestPlanTextEmbedding.instantiateFromText(text)
        self.assertEqual('', instance.prefix)
        self.assertIsNone(instance.yamlObject['data']['parentPlan']['uri'])
        self.assertEqual('trailing text\n', instance.suffix)

    def testChildSimpleTestPlanTextEmbedding(self):
        text = '''some text before
continuing...
[pylarion-structured-field-start]  
header:
  subject: pylarion
  formatVersion: 0.0
  dataType: SimpleTestPlan
data:
  parentPlan:
    uri: subterra:data-service:objects:myParentURI
[pylarion-structured-field-end]
'''
        instance = _SimpleTestPlanTextEmbedding.instantiateFromText(text)
        self.assertEqual('some text before\ncontinuing...\n', instance.prefix)
        self.assertEqual('subterra:data-service:objects:myParentURI', instance.yamlObject['data']['parentPlan']['uri'])
        self.assertEqual('', instance.suffix)

    def testSimpleTestRunTextEmbedding(self):
        text = '''abc
[pylarion-structured-field-start]  
header:
  subject: pylarion
  formatVersion: 0.0
  dataType: SimpleTestRun
data:
  plan:
    uri: subterra:data-service:objects:myPlanURI
[pylarion-structured-field-end]
xyz
'''
        instance = _SimpleTestRunTextEmbedding.instantiateFromText(text)
        self.assertEqual('abc\n', instance.prefix)
        self.assertEqual('subterra:data-service:objects:myPlanURI', instance.yamlObject['data']['plan']['uri'])
        self.assertEqual('xyz\n', instance.suffix)
