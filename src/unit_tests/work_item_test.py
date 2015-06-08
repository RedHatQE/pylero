'''
Created on Apr 15, 2015

@author: szacks
'''
import unittest2
import os
from pylarion.work_item import FunctionalTestCase, Requirement
from pylarion.exceptions import PylarionLibException
from pylarion.test_step import TestStep

DEFAULT_PROJ = FunctionalTestCase.default_project
HYPERLINK = "http://www.google.com"
CUR_PATH = os.path.dirname(os.path.abspath(__file__))
ATTACH_PATH = CUR_PATH + "/refs/red_box.png"


class WorkItemTest(unittest2.TestCase):

    @classmethod
    def setUpClass(cls):
        ftc = FunctionalTestCase.create(DEFAULT_PROJ,
                                        "regression",
                                        "regression",
                                        caseimportance="high",
                                        caselevel="component",
                                        caseautomation="notautomated",
                                        caseposneg="positive")
        req = Requirement.create(DEFAULT_PROJ,
                                 "regression _link",
                                 "regression link",
                                 reqtype="functional",
                                 severity="should_have")
        cls.work_item_id = ftc.work_item_id
        cls.work_item_uri = ftc.uri
        cls.work_item_id_2 = req.work_item_id
        cls.work_item_uri_2 = req.uri

    def test_aa_query(self):
        results = FunctionalTestCase.query(
            "project.id:%s AND title:regression" % (DEFAULT_PROJ))
        ftc = results[0]
        self.assertIsNone(ftc.title)
        results2 = FunctionalTestCase.query(
            "project.id:%s AND title:regression" % (DEFAULT_PROJ),
            fields=["work_item_id", "title"])
        ftc = results2[0]
        self.assertIsNotNone(ftc.title)

    def test_ab_get_item(self):
        ftc = FunctionalTestCase(project_id=DEFAULT_PROJ,
                                 work_item_id=self.work_item_id)
        self.assertIsNotNone(ftc.uri)

    def test_add_assignee(self):
        ftc = FunctionalTestCase(project_id=DEFAULT_PROJ,
                                 work_item_id=self.work_item_id)
        with self.assertRaises(PylarionLibException):
            ftc.add_assignee("invalid user")
        self.assertTrue(ftc.add_assignee(ftc.logged_in_user_id))
        ftc2 = FunctionalTestCase(project_id=DEFAULT_PROJ,
                                  work_item_id=self.work_item_id)
        self.assertTrue(ftc2.assignee)
        self.assertEqual(ftc2.assignee[0].user_id, ftc2.logged_in_user_id)

    def test_add_approvee(self):
        ftc = FunctionalTestCase(project_id=DEFAULT_PROJ,
                                 work_item_id=self.work_item_id)
        with self.assertRaises(PylarionLibException):
            ftc.add_approvee("invalid user")
        ftc.add_approvee(ftc.logged_in_user_id)
        ftc2 = FunctionalTestCase(project_id=DEFAULT_PROJ,
                                  work_item_id=self.work_item_id)
        self.assertTrue(len(ftc2.approvals) == 1)
        approval = ftc2.approvals[0]
        self.assertEqual(approval.status, "waiting")
        self.assertEqual(approval.user_id, ftc.logged_in_user_id)

    def test_add_category(self):
        ftc = FunctionalTestCase(project_id=DEFAULT_PROJ,
                                 work_item_id=self.work_item_id)
        with self.assertRaises(PylarionLibException):
            ftc.add_category("invalid category")
        self.assertTrue(ftc.add_category("filesystems"))
        ftc2 = FunctionalTestCase(project_id=DEFAULT_PROJ,
                                  work_item_id=self.work_item_id)
        self.assertTrue(len(ftc2.categories) == 1)
        cat = ftc2.categories[0]
        self.assertEqual(cat.category_id, "filesystems")

    def test_add_hyperlink(self):
        # TODO: check if an invalid hyperlink can be passed in.
        ftc = FunctionalTestCase(project_id=DEFAULT_PROJ,
                                 work_item_id=self.work_item_id)
        with self.assertRaises(PylarionLibException):
            ftc.add_hyperlink(HYPERLINK, "invalid")
        self.assertTrue(ftc.add_hyperlink(HYPERLINK, "ref_ext"))
        ftc2 = FunctionalTestCase(project_id=DEFAULT_PROJ,
                                  work_item_id=self.work_item_id)
        self.assertTrue(len(ftc2.hyperlinks) == 1)
        link = ftc2.hyperlinks[0]
        self.assertEqual(link.uri, HYPERLINK)
        self.assertEqual(link.role, "ref_ext")

    def test_add_linked_work_item(self):
        ftc = FunctionalTestCase(project_id=DEFAULT_PROJ,
                                 work_item_id=self.work_item_id)
        self.assertTrue(ftc.add_linked_item(self.work_item_id_2, "verifies"))
        ftc2 = FunctionalTestCase(project_id=DEFAULT_PROJ,
                                  work_item_id=self.work_item_id)
        self.assertTrue(len(ftc2.linked_work_items) == 1)
        link = ftc2.linked_work_items[0]
        self.assertEqual(link.work_item_id, self.work_item_id_2)
        self.assertEqual(link.role, "verifies")
        ftc3 = Requirement(project_id=DEFAULT_PROJ,
                           work_item_id=self.work_item_id_2)
        self.assertTrue(len(ftc3.linked_work_items_derived) == 1)
        link = ftc3.linked_work_items_derived[0]
        self.assertEqual(link.work_item_id, self.work_item_id)
        self.assertEqual(link.role, "verifies")

    def test_create_attachment(self):
        ftc = FunctionalTestCase(project_id=DEFAULT_PROJ,
                                 work_item_id=self.work_item_id)
        ftc.create_attachment(ATTACH_PATH, "Attached File")
        ftc2 = FunctionalTestCase(project_id=DEFAULT_PROJ,
                                  work_item_id=self.work_item_id)
        self.assertTrue(len(ftc2.attachments) == 1)
        attach = ftc2.attachments[0]
        self.assertEqual(attach.author, ftc2.logged_in_user_id)
        self.assertEqual(attach.title, "Attached File")

    def test_create_comment(self):
        ftc = FunctionalTestCase(project_id=DEFAULT_PROJ,
                                 work_item_id=self.work_item_id)
        ftc.create_comment("This is a comment")
        ftc2 = FunctionalTestCase(project_id=DEFAULT_PROJ,
                                  work_item_id=self.work_item_id)
        self.assertTrue(len(ftc2.comments) == 1)
        comment = ftc2.comments[0]
        self.assertEqual(comment.text, "This is a comment")

    def test_delete_attachment(self):
        ftc = FunctionalTestCase(project_id=DEFAULT_PROJ,
                                 work_item_id=self.work_item_id)
        attach = ftc.attachments[0]
        ftc.delete_attachment(attach.attachment_id)
        ftc2 = FunctionalTestCase(project_id=DEFAULT_PROJ,
                                  work_item_id=self.work_item_id)
        self.assertEqual(ftc2.attachments, [])

    def test_edit_approval(self):
        ftc = FunctionalTestCase(project_id=DEFAULT_PROJ,
                                 work_item_id=self.work_item_id)
        with self.assertRaises(PylarionLibException):
            ftc.edit_approval("invalid user", "approved")
        with self.assertRaises(PylarionLibException):
            ftc.edit_approval(ftc.logged_in_user_id, "invalid status")
        ftc.edit_approval(ftc.logged_in_user_id, "approved")
        ftc2 = FunctionalTestCase(project_id=DEFAULT_PROJ,
                                  work_item_id=self.work_item_id)
        self.assertTrue(len(ftc2.approvals) == 1)
        approval = ftc2.approvals[0]
        self.assertEqual(approval.status, "approved")
        self.assertEqual(approval.user_id, ftc.logged_in_user_id)

    def test_get_back_linked_work_items(self):
        ftc = Requirement(project_id=DEFAULT_PROJ,
                          work_item_id=self.work_item_id_2)
        items = ftc.get_back_linked_work_items()
        self.assertTrue(len(items) == 1)
        wi = items[0]
        self.assertEqual(wi.work_item_id, self.work_item_id)

    def test_multiple_types(self):
        req = Requirement()
        ftc = FunctionalTestCase()
        with self.assertRaises(AttributeError):
            ftc.reqtype
        with self.assertRaises(AttributeError):
            req.caseimportance
        req.title = "req1"
        ftc.title = "ftc1"
        self.assertNotEqual(req.title, ftc.title)

    def test_steps(self):
        test1 = ["Test 1", "Result 1"]
        test2 = ["Test 2", "Result 2"]
        test3 = ["Test 3", "Result 3"]
        ts1 = TestStep()
        ts1.values = test1
        ts2 = TestStep()
        ts2.values = test2
        ts3 = TestStep()
        ts3.values = test3
        set_steps = [ts1, ts2, ts3]
        ftc = FunctionalTestCase(project_id=DEFAULT_PROJ,
                                 work_item_id=self.work_item_id)
        ftc.set_test_steps(set_steps)
        ftc2 = FunctionalTestCase(project_id=DEFAULT_PROJ,
                                  work_item_id=self.work_item_id)
        get_steps = ftc2.get_test_steps()
        self.assertEqual(get_steps.steps[0].values[0].content,
                         ts1.values[0].content)
        self.assertEqual(get_steps.steps[0].values[1].content,
                         ts1.values[1].content)
        self.assertEqual(get_steps.steps[1].values[0].content,
                         ts2.values[0].content)
        self.assertEqual(get_steps.steps[1].values[1].content,
                         ts2.values[1].content)
        self.assertEqual(get_steps.steps[2].values[0].content,
                         ts3.values[0].content)
        self.assertEqual(get_steps.steps[2].values[1].content,
                         ts3.values[1].content)

    def test_remove_assignee(self):
        ftc = FunctionalTestCase(project_id=DEFAULT_PROJ,
                                 work_item_id=self.work_item_id)
        self.assertFalse(ftc.remove_assignee("invalid user"))
        self.assertFalse(ftc.remove_assignee("oramraz"))
        self.assertTrue(ftc.remove_assignee(ftc.logged_in_user_id))

    def test_remove_category(self):
        ftc = FunctionalTestCase(project_id=DEFAULT_PROJ,
                                 work_item_id=self.work_item_id)
        self.assertFalse(ftc.remove_category("invalid cat"))
        self.assertFalse(ftc.remove_category("clustering"))
        self.assertTrue(ftc.remove_category("filesystems"))

    def test_remove_hyperlink(self):
        ftc = FunctionalTestCase(project_id=DEFAULT_PROJ,
                                 work_item_id=self.work_item_id)
        self.assertTrue(ftc.remove_hyperlink(HYPERLINK))

    def test_remove_linked_item(self):
        ftc = FunctionalTestCase(project_id=DEFAULT_PROJ,
                                 work_item_id=self.work_item_id)
        self.assertTrue(ftc.remove_linked_item(self.work_item_id_2,
                                               "verifies"))

    def test_update(self):
        ftc = FunctionalTestCase(project_id=DEFAULT_PROJ,
                                 work_item_id=self.work_item_id)
        ftc.status = "approved"
        ftc.update()
        ftc2 = FunctionalTestCase(project_id=DEFAULT_PROJ,
                                  work_item_id=self.work_item_id)
        self.assertEqual(ftc2.status, "approved")


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest2.main()
