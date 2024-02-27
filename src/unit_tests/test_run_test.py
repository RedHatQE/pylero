"""
Created on Apr 19, 2015

@author: szacks
"""
import datetime
import os
import unittest

from pylero.exceptions import PyleroLibException
from pylero.plan import Plan
from pylero.test_record import TestRecord
from pylero.test_run import TestRun
from pylero.test_step import TestStep
from pylero.test_step_result import TestStepResult
from pylero.work_item import IncidentReport
from pylero.work_item import TestCase

DEFAULT_PROJ = TestRun.default_project
TIME_STAMP = datetime.datetime.now().strftime("%Y%m%d%H%M%s")
# TEMPLATE_ID will change if the generate id setting is set
TEMPLATE_ID = "tmp_regr-%s" % TIME_STAMP
TEMPLATE_TITLE = "tmp_regr-%s" % TIME_STAMP
# TEST_RUN_ID will change if the generate id setting is set
TEST_RUN_ID = "tr_regr-%s" % TIME_STAMP
TEST_RUN_TITLE = "tr_regr-%s" % TIME_STAMP
PLAN_ID = "plan_regr-%s" % TIME_STAMP
CUR_PATH = os.path.dirname(os.path.abspath(__file__))
ATTACH_PATH = CUR_PATH + "/refs/red_box.png"
ATTACH_TITLE = "File"
TITLE1 = "title1_regr-%s" % TIME_STAMP
TITLE2 = "title2_regr-%s" % TIME_STAMP
TEST_RUN_ID2 = "tr2_regr-%s" % TIME_STAMP


class TestRunTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        tc1 = TestCase.create(
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
        cls.NEW_TEST_CASE = tc1.work_item_id
        tc2 = TestCase.create(
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
        cls.NEW_TEST_CASE2 = tc2.work_item_id
        Plan.create(
            plan_id=PLAN_ID,
            plan_name="regression",
            project_id=DEFAULT_PROJ,
            parent_id=None,
            template_id="release",
        )
        cls.NEW_PLAN = PLAN_ID

    def test_001_create_template(self):
        """This test does the following:
        * Creates a TestRun template based on the "Empty" template
        * Verifies that the returned object exists and is a template
        * Adds a custom field as a kwarg
        * Tries to create another template with an invalid enum value in kwarg
        * Tries to create another template with an invalid kwarg
        """
        global TEMPLATE_ID
        template = TestRun.create_template(
            DEFAULT_PROJ, TEMPLATE_ID, "Empty", title=TEMPLATE_TITLE, arch="i386"
        )
        TEMPLATE_ID = template.test_run_id
        self.assertIsNotNone(template.test_run_id)
        self.assertTrue(template.is_template)
        self.assertEqual(template.arch, "i386")
        with self.assertRaises(PyleroLibException):
            template = TestRun.create_template(
                DEFAULT_PROJ,
                TEMPLATE_ID + "1",
                "Empty",
                TEMPLATE_TITLE + "1",
                arch="BAD",
            )
        with self.assertRaises(PyleroLibException):
            template = TestRun.create_template(
                DEFAULT_PROJ,
                TEMPLATE_ID + "2",
                "Empty",
                TEMPLATE_TITLE + "2",
                notaparm="BAD",
            )

    def test_002_create_run(self):
        """This test does the following:
        * creates a test run based on the template created in previous test
        * Verifies that the returned object exists and is not a template
        """
        global TEST_RUN_ID
        tr = TestRun.create(DEFAULT_PROJ, TEST_RUN_ID, TEMPLATE_ID, TEST_RUN_TITLE)
        TEST_RUN_ID = tr.test_run_id
        self.assertIsNotNone(tr.test_run_id)
        self.assertFalse(tr.is_template)

    def test_002_5_create_run_with_title(self):
        """This test does the following:
        * creates a test run based on the template created in previous test
            * with both a title and an id
            * with just a title.
        * Verifies that the returned object exists and is not a template
        """
        tr1 = TestRun.create(DEFAULT_PROJ, TEST_RUN_ID2, TEMPLATE_ID, TITLE1)
        self.assertIsNotNone(tr1.test_run_id)
        self.assertEqual(tr1.title, TITLE1)
        self.assertFalse(tr1.is_template)
        tr2 = TestRun.create(DEFAULT_PROJ, None, TEMPLATE_ID, TITLE2)
        self.assertIsNotNone(tr2.test_run_id)
        self.assertEqual(tr2.title, TITLE2)
        self.assertFalse(tr2.is_template)

    def test_003_get(self):
        """This test does the following:
        * Verifies error with invalid test_run_id
        * Gets a valid TestRun
        * verifies that the TestRun retrieves has the expected test_run_id
        """
        with self.assertRaises(PyleroLibException):
            TestRun(project_id=DEFAULT_PROJ, test_run_id="InValid")
        tr = TestRun(project_id=DEFAULT_PROJ, test_run_id=TEST_RUN_ID)
        self.assertEqual(tr.test_run_id, TEST_RUN_ID)

    def test_004_search(self):
        """This test does the following:
        * Gets a TestRun
        * Searches using the same query as the testrun (adding project id)
        * verifies that there are number of records returned as are in the
          records attribute of the TestRun
        """
        query = "id:%s" % (TEST_RUN_ID)
        lst_tr = TestRun.search(query)
        self.assertEqual(lst_tr[0].test_run_id, TEST_RUN_ID)

    def test_005_test_record_by_fields(self):
        """This test does the following:
        * gets a TestRun object
        * Adds a TestRecord to it
        ** verifies that it fails with an invalid result
        ** verifies that it fails if it adds a duplicate case.
        * Adds an attachment to the record.
        ** verifies that the attachment is there
        * deletes the attachment
        ** verifies the attachment is not there
        * updates the test record.
        """
        tr = TestRun(project_id=DEFAULT_PROJ, test_run_id=TEST_RUN_ID)
        with self.assertRaises(PyleroLibException):
            tr.add_test_record_by_fields(
                self.NEW_TEST_CASE,
                "invalid",
                "No Comment",
                tr.logged_in_user_id,
                datetime.datetime.now(),
                "50.5",
            )
        tr.add_test_record_by_fields(
            self.NEW_TEST_CASE,
            "passed",
            "No Comment",
            tr.logged_in_user_id,
            datetime.datetime.now(),
            "50.5",
        )
        tr.reload()
        self.assertEqual(tr.status, "finished")
        # test that the same case cannot be added multiple times.
        with self.assertRaises(PyleroLibException):
            tr.add_test_record_by_fields(
                self.NEW_TEST_CASE,
                "passed",
                "No Comment",
                tr.logged_in_user_id,
                datetime.datetime.now(),
                "50.5",
            )
        tr.reload()
        rec = tr.records[-1]
        tr.add_attachment_to_test_record(rec.test_case_id, ATTACH_PATH, ATTACH_TITLE)
        tr.reload()
        rec = tr.records[-1]
        self.assertTrue(len(rec.attachments) == 1)
        self.assertEqual(rec.attachments[0].title, ATTACH_TITLE)
        tr.delete_attachment_from_test_record(
            rec.test_case_id, rec.attachments[0].filename
        )
        tr.reload()
        rec = tr.records[-1]
        self.assertEqual(rec.attachments, [])
        tr.update_test_record_by_fields(
            rec.test_case_id,
            rec.result,
            "Yes Comment",
            rec.executed_by,
            rec.executed,
            rec.duration,
        )
        tr.reload()
        rec = tr.records[-1]
        self.assertEqual(rec.comment, "Yes Comment")

    def test_006_test_record_by_object(self):
        """This test does the following:
        * gets a TestRun
        * creates a TestRecord
        * populates the TestRecord
        * Tries to add a duplicate TestRecord (should fail)
        * Adds a TestRecord
        * Reloads the TestRun
        * Verifies the TestRecord was added
        * Updates the TestRecord
        * Reloads the TestRun
        * Verifies the TestRecord was modified
        """
        tr = TestRun(project_id=DEFAULT_PROJ, test_run_id=TEST_RUN_ID)
        rec = TestRecord()
        rec.test_case_id = self.NEW_TEST_CASE
        rec.comment = "No Comment"
        rec.duration = "50.5"
        # verify that it does not allow duplicate records.
        # (same record was added in previous test)
        with self.assertRaises(PyleroLibException):
            tr.add_test_record_by_object(rec)
        rec.test_case_id = self.NEW_TEST_CASE2
        tr.add_test_record_by_object(rec)
        tr.reload()
        check_rec = tr.records[-1]
        self.assertEqual(tr.status, "inprogress")
        self.assertEqual(check_rec.test_case_id, self.NEW_TEST_CASE2)
        rec.result = "blocked"
        rec.executed_by = tr.logged_in_user_id
        rec.executed = datetime.datetime.now()
        tr.update_test_record_by_object(self.NEW_TEST_CASE2, rec)
        tr.reload()
        self.assertEqual(tr.status, "finished")

        check_rec = tr.records[-1]
        self.assertEqual(check_rec.result, "blocked")

    def test_007_attachment(self):
        """This test does the following:
        * add an attachment to the TestRun.
        * verify that there is 1 attachment with the correct title
        * verify the get_attachment function
        * verify the get_attachments function
        * delete the attachment
        * verify that there are no attachments.
        """
        tr = TestRun(project_id=DEFAULT_PROJ, test_run_id=TEST_RUN_ID)
        tr.add_attachment(ATTACH_PATH, ATTACH_TITLE)
        tr.reload()
        self.assertEqual(len(tr.attachments), 1)
        self.assertEqual(tr.attachments[0].title, ATTACH_TITLE)
        attach = tr.get_attachment(tr.attachments[0].filename)
        self.assertEqual(tr.attachments[0].title, attach.title)
        lst_attach = tr.get_attachments()
        self.assertEqual(lst_attach[0].title, attach.title)
        tr.delete_attachment(tr.attachments[0].filename)
        tr.reload()
        self.assertEqual(tr.attachments, [])

    def test_008_update(self):
        """This test does the following:
        * gets a TestRun
        * modifies an attribute
        * updates the TestRun
        * reloads the TestRun
        * verifies that the TestRun attribute has changed
        """
        tr = TestRun(project_id=DEFAULT_PROJ, test_run_id=TEST_RUN_ID)
        tr.type = "featureverification"
        tr.update()
        tr.reload()
        self.assertEqual(tr.type, "featureverification")

    def test_009_dynamic_records(self):
        """This test does the following:
        * creates a TestCase
        * creates a TestRun based on the Example template (Dynamic query)
        * verifies that it is a dynamic query
        * updates an test record.
        * reloads
        * verifies that the record has been added
        """
        TestCase.create(
            DEFAULT_PROJ,
            TIME_STAMP,
            "regression",
            caseimportance="high",
            caselevel="component",
            caseautomation="notautomated",
            caseposneg="positive",
            testtype="functional",
            subtype1="-",
        )
        tr = TestRun.create(
            DEFAULT_PROJ,
            "querytest-%s" % TIME_STAMP,
            "Example",
            "querytest-%s" % TIME_STAMP,
            query=TIME_STAMP,
        )
        self.assertEqual(tr.select_test_cases_by, "dynamicQueryResult")
        num_recs = len(tr.records)
        test_case_id = tr.records[0].test_case_id
        tr.update_test_record_by_fields(
            test_case_id,
            "blocked",
            "comment",
            tr.logged_in_user_id,
            datetime.datetime.now(),
            0,
        )
        tr.reload()
        self.assertEqual(num_recs, len(tr.records))
        self.assertEqual(test_case_id, tr.records[0].test_case_id)
        self.assertEqual(tr.records[0].result, "blocked")

    def test_010_search_with_custom_fields(self):
        """This test does the following:
        * Gets a TestRun
        * Searches using the same query as the testrun (adding project id)
        * and with custom_field 'plannedin'
        * verifies that the 'plannedin' field of the returnd TestRun is None
        * The purpose here is to check that it doesnt throws exception
        """
        query = "id:%s" % (TEST_RUN_ID)
        lst_tr = TestRun.search(query, ["plannedin"])
        self.assertEqual(lst_tr[0].plannedin, None)
        lst_tr[0].plannedin = self.NEW_PLAN
        lst_tr[0].update()
        lst_tr = TestRun.search(query, ["plannedin"])
        self.assertEqual(lst_tr[0].plannedin, self.NEW_PLAN)
        lst_tr[0].plannedin = None
        lst_tr[0].update()

    def test_011_customfield_object(self):
        """This test does the following:
        * gets a TestRun
        * Adds a Plan to it
        * Verifies that the plan was added
        * Verifies that a non valid plan cant be added
        """
        tr = TestRun(project_id=DEFAULT_PROJ, test_run_id=TEST_RUN_ID)
        with self.assertRaises(PyleroLibException):
            tr.plannedin = "not_valid"
        tr.plannedin = self.NEW_PLAN
        self.assertEqual(tr.plannedin, self.NEW_PLAN)
        tr.update()

    def test_012_search_with_URI_fields(self):
        """This test does the following:
        * Gets a TestRun
        * Searches using the same query as the testrun (adding project id)
        * Verify that 'author' is instantiated
        """
        query = "id:%s" % (TEST_RUN_ID)
        lst_tr = TestRun.search(query, fields=["author"])
        self.assertIsNotNone(lst_tr[0].author)

    def test_013_incident_report_test(self):
        """This test does the following:
        * gets a TestRun
        * gets a TestCase
        * adds test_steps
        * creates a TestRecord
        * populates the TestRecord
        * Fail the testRecord
        * reloads the TestCase
        * Verifies that an Incident Report was Created
        """
        tr = TestRun(project_id=DEFAULT_PROJ, test_run_id=TEST_RUN_ID)
        tests = [["Test 1", "Result 1"], ["Test 2", "Result 2"], ["Test 3", "Result 3"]]
        set_steps = []
        for test in tests:
            ts = TestStep()
            ts.values = test
            set_steps.append(ts)
        tc = TestCase(work_item_id=self.NEW_TEST_CASE)
        tc.set_test_steps(set_steps)
        tc.update()
        tc.reload()
        steps = tc.test_steps.steps
        results = []
        for step in steps:
            res = TestStepResult()
            res.result = "failed"
            res.comment = "This is the result"
            results.append(res)
        rec = TestRecord()
        rec.test_step_results = results
        rec.test_case_id = self.NEW_TEST_CASE
        rec.comment = "Incident Report was Created"
        rec.duration = "50.5"
        rec.result = "failed"
        rec.executed_by = tr.logged_in_user_id
        rec.executed = datetime.datetime.now()
        tr.update_test_record_by_object(self.NEW_TEST_CASE, rec)
        tc.reload()
        linked_work_items = tc.linked_work_items_derived
        idx = len(linked_work_items) - 1
        item_id = linked_work_items[idx].work_item_id
        incident = IncidentReport(project_id=DEFAULT_PROJ, work_item_id=item_id)
        self.assertIsNotNone(incident)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
