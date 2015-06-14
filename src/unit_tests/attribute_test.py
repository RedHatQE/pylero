import unittest2
import datetime
from pylarion.document import Document
from pylarion.exceptions import PylarionLibException
from pylarion.user import User
from pylarion.test_run import TestRun
from pylarion.project import Project
from pylarion.test_record import TestRecord
from pylarion.work_item import TestCase, Requirement

USER = "szacks"
ALT_USER = "oramraz"
PROJ2 = "szacks"
TEST_RUN_ID = "tr_regr-%s" % datetime.datetime.now().strftime("%Y%m%d%H%M%s")
DEFAULT_PROJ = Document.default_project


class AttributeTest(unittest2.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.doc = Document.create(
            DEFAULT_PROJ, "Testing", "Attribute_Test",
            "Attribute_Test", ["testcase"])
        cls.testrun = TestRun.create(DEFAULT_PROJ, TEST_RUN_ID, "example")
        cls.tc = TestCase.create(DEFAULT_PROJ,
                                 "regression",
                                 "regression",
                                 caseimportance="high",
                                 caselevel="component",
                                 caseautomation="notautomated",
                                 caseposneg="positive")
        cls.TEST_CASE_ID = cls.tc.work_item_id

    @classmethod
    def tearDownClass(cls):
        doc = Document(project_id=DEFAULT_PROJ,
                       doc_with_space="Testing/Attribute_Test")
        doc.delete()

    def test_basic(self):
        self.assertEqual(self.doc.title, "Attribute_Test")
        self.doc.title = "new title"
        self.assertEqual(self.doc.title, "new title")
        self.doc.update()
        doc2 = Document(project_id=DEFAULT_PROJ,
                        doc_with_space="Testing/Attribute_Test")
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
        with self.assertRaises(PylarionLibException):
            self.doc.status = "bad"
        self.doc.status = "obsolete"
        self.assertEqual(self.doc.status, "obsolete")

    def test_arr_obj(self):
        testrun = TestRun(project_id=DEFAULT_PROJ,
                          test_run_id=TEST_RUN_ID)
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
        self.assertEqual(cnt+1, len(testrun.records))
        recs = testrun.records
        rec = recs[-1]
        self.assertEqual(rec.result, "passed")

    def test_custom_testrun(self):
        testrun = TestRun(project_id=DEFAULT_PROJ,
                          test_run_id=TEST_RUN_ID)
        self.assertIsNotNone(testrun.arch)
        with self.assertRaises(PylarionLibException):
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
        with self.assertRaises(PylarionLibException):
            testrun.arch = "bad"
        valid_values = testrun.get_valid_field_values("arch")
        testrun.arch = valid_values[0]
        self.assertEqual(valid_values[0], testrun.arch)

    def test_custom_workitem(self):
        tc2 = TestCase(project_id=DEFAULT_PROJ,
                       work_item_id=self.TEST_CASE_ID)
        self.assertIsNotNone(tc2.caseautomation)
        with self.assertRaises(PylarionLibException):
            tc2.caseautomation = "bad"
        tc2.caseautomation = "automated"
        # check for shared memory issue
        self.assertNotEqual(self.tc.caseautomation, tc2.caseautomation)
        req = Requirement()
        with self.assertRaises(PylarionLibException):
            req.reqtype = "bad"
        req.reqtype = 'functional'

    def test_uri_obj(self):
        testrun2 = TestRun(project_id=DEFAULT_PROJ,
                           test_run_id=TEST_RUN_ID)
        self.assertEqual(testrun2.project_id, DEFAULT_PROJ)
        proj = Project(PROJ2)
        testrun2.project_id = proj
        self.assertEqual(testrun2.project_id,
                         proj.project_id)
        testrun2.project_id = DEFAULT_PROJ
        self.assertNotEqual(testrun2.project_id,
                            proj.project_id)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest2.main()
