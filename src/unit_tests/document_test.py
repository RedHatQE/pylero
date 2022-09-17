"""
Created on Apr 13, 2015

@author: szacks
"""
import datetime
import unittest

from pylero.document import Document
from pylero.test_run import TestRun
from pylero.work_item import TestCase

WI_ID = ""
TIME_STAMP = datetime.datetime.now().strftime("%Y%m%d%H%M%s")
DOC_NAME = "Document_Test-%s" % TIME_STAMP
# TEMPLATE_ID and TEST_RUN_ID will be changed if the project Generate ID is set
TEMPLATE_ID = "doc_tmp_test-%s" % TIME_STAMP
TEST_RUN_ID = "doc_test-%s" % TIME_STAMP
TEMPLATE_TITLE = "doc_tmp_test-%s" % TIME_STAMP
TEST_RUN_TITLE = "doc_test-%s" % TIME_STAMP


class DocumentTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc_create = Document.create(
            Document.default_project,
            "Testing",
            DOC_NAME,
            "Document_Test",
            ["testcase"],
            "testspecification",
        )

    def test_002_get_documents(self):
        lst_doc = Document.get_documents(Document.default_project, "Testing")
        doc = lst_doc[0]
        self.assertIsInstance(doc, Document)

    def test_003_query(self):
        lst_doc = Document.query("project.id:" + Document.default_project, limit=10)
        doc = lst_doc[0]
        self.assertIsInstance(doc, Document)

    def test_004_get_name(self):
        self.doc_get1 = Document(
            project_id=Document.default_project, doc_with_space="Testing/" + DOC_NAME
        )
        self.assertIsInstance(self.doc_get1, Document)

    def test_005_get_uri(self):
        self.doc_get2 = Document(uri=self.doc_create.uri)
        self.assertIsInstance(self.doc_get2, Document)

    def test_006_create_work_item(self):
        tc = TestCase()
        tc.title = "regression"
        tc.description = "regression document test"
        tc.status = "draft"
        tc.caseimportance = "high"
        tc.caselevel = "component"
        tc.caseautomation = "notautomated"
        tc.caseposneg = "positive"
        tc.testtype = "functional"
        tc.subtype1 = "-"
        doc = Document(uri=self.doc_create.uri)
        wi = doc.create_work_item(None, tc)
        doc_wis = doc.get_work_items(None, True)
        doc_wi_ids = [doc_wi.work_item_id for doc_wi in doc_wis]
        self.assertIn(wi.work_item_id, doc_wi_ids)
        global WI_ID
        WI_ID = wi.work_item_id

    def test_007_update(self):
        doc = Document(uri=self.doc_create.uri)
        doc.status = "published"
        doc.update()

    def test_008_doc_test_run_template(self):
        global TEMPLATE_ID
        global TEST_RUN_ID
        doc_with_space = self.doc_create.space
        self.doc_create.session.tx_begin()
        tmp = TestRun.create_template(
            project_id=Document.default_project,
            template_id=TEMPLATE_ID,
            doc_with_space=doc_with_space,
            title=TEMPLATE_TITLE,
        )
        TEMPLATE_ID = tmp.test_run_id
        tr = TestRun.create(
            project_id=Document.default_project,
            test_run_id=TEST_RUN_ID,
            template=TEMPLATE_ID,
            title=TEST_RUN_TITLE,
        )
        TEST_RUN_ID = tr.test_run_id
        self.assertEqual(len(tr.records), 1)
        self.assertEqual(tr.records[0].test_case_id, WI_ID)
        self.doc_create.session.tx_commit()


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
