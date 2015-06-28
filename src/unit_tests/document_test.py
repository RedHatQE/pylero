'''
Created on Apr 13, 2015

@author: szacks
'''
import unittest2
from pylarion.document import Document
from pylarion.work_item import TestCase
from pylarion.test_run import TestRun

WI_ID = ""


class DocumentTest(unittest2.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.doc_create = Document.create(
            Document.default_project, "Testing", "Document_Test",
            "Document_Test", ["testcase"])

    @classmethod
    def tearDownClass(cls):
        doc = Document(uri=cls.doc_create.uri)
        doc.delete()

    def test_002_get_documents(self):
        lst_doc = Document.get_documents(Document.default_project, "Testing")
        doc = lst_doc[0]
        self.assertIsInstance(doc, Document)

    def test_003_query(self):
        lst_doc = Document.query("project.id:" + Document.default_project,
                                 limit=10)
        doc = lst_doc[0]
        self.assertIsInstance(doc, Document)

    def test_004_get_name(self):
        self.doc_get1 = Document(project_id=Document.default_project,
                                 doc_with_space="Testing/Document_Test")
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
        doc_with_space = self.doc_create.space
        self.doc_create.session.tx_begin()
        tmp_tr = TestRun.create_template(project_id=Document.default_project,
                                         template_id="doc_tmp_test",
                                         doc_with_space=doc_with_space)
        tr = TestRun.create(project_id=Document.default_project,
                            test_run_id="doc_test",
                            template="doc_tmp_test")
        self.assertEquals(len(tr.records), 1)
        self.assertEquals(tr.records[0].test_case_id, WI_ID)
        self.doc_create.session.tx_commit()

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest2.main()
