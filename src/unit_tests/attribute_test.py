# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import datetime
import unittest

from pylero.document import Document
from pylero.exceptions import PyleroLibException
from pylero.test_record import TestRecord
from pylero.test_run import TestRun
from pylero.test_steps import TestSteps
from pylero.user import User
from pylero.work_item import Requirement
from pylero.work_item import TestCase

USER = "user1"
ALT_USER = "user2"
PROJ2 = "proj2"
TIME_STAMP = datetime.datetime.now().strftime("%Y%m%d%H%M%s")
# TEST_RUN_ID will change if the generate id setting is set
TEST_RUN_ID = "tr_regr-%s" % TIME_STAMP
TEST_RUN_TITLE = "tr_regr-%s" % TIME_STAMP
# TEMPLATE_ID will change if the generate id setting is set
TEMPLATE_ID = "tr_regr2-%s" % TIME_STAMP
TEMPLATE_TITLE = "tr_regr2-%s" % TIME_STAMP
DOC_NAME = "Document_Test-%s" % TIME_STAMP
DEFAULT_PROJ = Document.default_project


class AttributeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global TEST_RUN_ID
        cls.doc = Document.create(
            DEFAULT_PROJ,
            "Testing",
            DOC_NAME,
            "Attribute_Test",
            ["testcase"],
            "testspecification",
        )
        cls.testrun = TestRun.create(
            DEFAULT_PROJ, TEST_RUN_ID, "example", TEST_RUN_TITLE
        )
        TEST_RUN_ID = cls.testrun.test_run_id
        # arch is a custom field defined by global admins for test runs.
        # It is set here for a test on custom fields that requires at least two
        # valid values. If in the future, this custom field is removed, or the
        # number of valid values is lowered to 1, a different custom field will
        # have to be used.
        valid_values = cls.testrun.get_valid_field_values("arch")
        cls.testrun.arch = valid_values[1]
        cls.testrun.update()

        cls.tc = TestCase.create(
            DEFAULT_PROJ,
            "regression",
            "regression",
            caseimportance="high",
            caselevel="component",
            caseautomation="notautomated",
            caseposneg="positive",
            testtype="functional",
            subtype1="-",
        )
        cls.TEST_CASE_ID = cls.tc.work_item_id

    @classmethod
    def tearDownClass(cls):
        doc = Document(project_id=DEFAULT_PROJ, doc_with_space="Testing/" + DOC_NAME)
        doc.delete()

    def test_basic(self):
        self.assertEqual(self.doc.title, "Attribute_Test")
        self.doc.title = "new title"
        self.assertEqual(self.doc.title, "new title")
        self.doc.update()
        doc2 = Document(project_id=DEFAULT_PROJ, doc_with_space="Testing/" + DOC_NAME)
        self.assertEqual(doc2.title, "new title")

    def test_obj_writeuser(self):
        user = self.doc.author
        self.assertEqual(user, self.doc.logged_in_user_id)
        newuser = USER if not self.doc.author == USER else ALT_USER
        # verify passing in both an object and a string
        u2 = User(newuser)
        self.doc.author = u2
        self.assertEqual(self.doc.author, newuser)
        newuser = USER if not self.doc.author == USER else ALT_USER
        self.doc.author = newuser
        self.assertEqual(self.doc.author, newuser)

    def test_enum(self):
        # also tests id_attr with no_obj.
        with self.assertRaises(PyleroLibException):
            self.doc.status = "bad"
        self.doc.status = "obsolete"
        self.assertEqual(self.doc.status, "obsolete")

    def test_arr_obj(self):
        testrun = TestRun(project_id=DEFAULT_PROJ, test_run_id=TEST_RUN_ID)
        recs = testrun.records
        if not isinstance(recs, list):
            recs = []
            cnt = 0
        else:
            cnt = len(recs)
        rec = TestRecord()
        rec.test_case_id = self.TEST_CASE_ID
        rec.executed = datetime.datetime.now()
        rec.executed_by = USER
        rec.duration = "5.0"
        rec.result = "passed"
        recs.append(rec)
        testrun.records = recs
        self.assertEqual(cnt + 1, len(testrun.records))
        recs = testrun.records
        rec = recs[-1]
        self.assertEqual(rec.result, "passed")

    def test_custom_testrun(self):
        testrun = TestRun(project_id=DEFAULT_PROJ, test_run_id=TEST_RUN_ID)
        self.assertIsNotNone(testrun.arch)
        with self.assertRaises(PyleroLibException):
            testrun.arch = "bad"
        valid_values = testrun.get_valid_field_values("arch")
        testrun.arch = valid_values[0]
        self.assertEqual(valid_values[0], testrun.arch)

    def test_custom_testrun2(self):
        """this test does the following:
        * Instantiate an empty test run.
        * verify that the custom field exists and is None
        * test an invalid value
        * test a valid value
        * verify that it saves it in the attribute
        """
        testrun = TestRun()
        self.assertIsNone(testrun.arch)
        with self.assertRaises(PyleroLibException):
            testrun.arch = "bad"
        valid_values = testrun.get_valid_field_values("arch")
        testrun.arch = valid_values[0]
        self.assertEqual(valid_values[0], testrun.arch)

    def test_custom_workitem(self):
        tc2 = TestCase(project_id=DEFAULT_PROJ, work_item_id=self.TEST_CASE_ID)
        self.assertIsNotNone(tc2.caseautomation)
        with self.assertRaises(PyleroLibException):
            tc2.caseautomation = "bad"
        tc2.caseautomation = "automated"
        # check for shared memory issue
        self.assertNotEqual(self.tc.caseautomation, tc2.caseautomation)
        req = Requirement()
        with self.assertRaises(PyleroLibException):
            req.reqtype = "bad"
        req.reqtype = "functional"

    def test_uri_obj(self):
        testrun2 = TestRun(project_id=DEFAULT_PROJ, test_run_id=TEST_RUN_ID)
        self.assertEqual(testrun2.template, "example")
        new_template = TestRun.create_template(
            DEFAULT_PROJ, TEMPLATE_ID, "example", title=TEMPLATE_TITLE
        )
        testrun2.template = new_template
        self.assertEqual(testrun2.template, new_template.test_run_id)
        self.assertNotEqual(testrun2.template, "example")

    def test_bad_character(self):
        """this test validates that non UTF-8 characters will cause an error"""
        test_case = TestCase()
        steps = TestSteps()
        with self.assertRaises(PyleroLibException):  # check _obj_setter
            test_case.status = "é".encode("latin")
        with self.assertRaises(PyleroLibException):  # check _custom_setter
            test_case.tcmscaseid = "é".encode("latin")
        with self.assertRaises(PyleroLibException):  # check _regular_setter
            test_case.title = "é".encode("latin")
        with self.assertRaises(PyleroLibException):  # check _arr_obj_setter
            steps.keys = ["é".encode("latin")]


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
