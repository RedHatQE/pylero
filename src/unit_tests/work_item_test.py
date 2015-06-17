'''
Created on Apr 15, 2015

@author: szacks
'''
import unittest2
import os
from pylarion.work_item import TestCase, Requirement
from pylarion.exceptions import PylarionLibException
from pylarion.test_step import TestStep

DEFAULT_PROJ = TestCase.default_project
HYPERLINK = "http://www.google.com"
CUR_PATH = os.path.dirname(os.path.abspath(__file__))
ATTACH_PATH = CUR_PATH + "/refs/red_box.png"


class WorkItemTest(unittest2.TestCase):

    @classmethod
    def setUpClass(cls):
        tc = TestCase.create(DEFAULT_PROJ,
                             "regression",
                             "regression",
                             caseimportance="high",
                             caselevel="component",
                             caseautomation="notautomated",
                             caseposneg="positive",
                             testtype="functional",
                             subtype1="-")
        req = Requirement.create(DEFAULT_PROJ,
                                 "regression _link",
                                 "regression link",
                                 reqtype="functional",
                                 severity="should_have")
        cls.work_item_id = tc.work_item_id
        cls.work_item_uri = tc.uri
        cls.work_item_id_2 = req.work_item_id
        cls.work_item_uri_2 = req.uri

    def test_aa_query(self):
        results = TestCase.query(
            "project.id:%s AND title:regression" % (DEFAULT_PROJ))
        tc = results[0]
        self.assertIsNone(tc.title)
        results2 = TestCase.query(
            "project.id:%s AND title:regression" % (DEFAULT_PROJ),
            fields=["work_item_id", "title"])
        tc = results2[0]
        self.assertIsNotNone(tc.title)

    def test_ab_get_item(self):
        tc = TestCase(project_id=DEFAULT_PROJ,
                      work_item_id=self.work_item_id)
        self.assertIsNotNone(tc.uri)

    def test_add_assignee(self):
        tc = TestCase(project_id=DEFAULT_PROJ,
                      work_item_id=self.work_item_id)
        with self.assertRaises(PylarionLibException):
            tc.add_assignee("invalid user")
        self.assertTrue(tc.add_assignee(tc.logged_in_user_id))
        tc2 = TestCase(project_id=DEFAULT_PROJ,
                       work_item_id=self.work_item_id)
        self.assertTrue(tc2.assignee)
        self.assertEqual(tc2.assignee[0].user_id, tc2.logged_in_user_id)

    def test_add_approvee(self):
        tc = TestCase(project_id=DEFAULT_PROJ,
                      work_item_id=self.work_item_id)
        with self.assertRaises(PylarionLibException):
            tc.add_approvee("invalid user")
        tc.add_approvee(tc.logged_in_user_id)
        tc2 = TestCase(project_id=DEFAULT_PROJ,
                       work_item_id=self.work_item_id)
        self.assertTrue(len(tc2.approvals) == 1)
        approval = tc2.approvals[0]
        self.assertEqual(approval.status, "waiting")
        self.assertEqual(approval.user_id, tc.logged_in_user_id)

    def test_add_category(self):
        tc = TestCase(project_id=DEFAULT_PROJ,
                      work_item_id=self.work_item_id)
        with self.assertRaises(PylarionLibException):
            tc.add_category("invalid category")
        self.assertTrue(tc.add_category("filesystems"))
        tc2 = TestCase(project_id=DEFAULT_PROJ,
                       work_item_id=self.work_item_id)
        self.assertTrue(len(tc2.categories) == 1)
        cat = tc2.categories[0]
        self.assertEqual(cat.category_id, "filesystems")

    def test_add_hyperlink(self):
        # TODO: check if an invalid hyperlink can be passed in.
        tc = TestCase(project_id=DEFAULT_PROJ,
                      work_item_id=self.work_item_id)
        with self.assertRaises(PylarionLibException):
            tc.add_hyperlink(HYPERLINK, "invalid")
        self.assertTrue(tc.add_hyperlink(HYPERLINK, "ref_ext"))
        tc2 = TestCase(project_id=DEFAULT_PROJ,
                       work_item_id=self.work_item_id)
        self.assertTrue(len(tc2.hyperlinks) == 1)
        link = tc2.hyperlinks[0]
        self.assertEqual(link.uri, HYPERLINK)
        self.assertEqual(link.role, "ref_ext")

    def test_add_linked_work_item(self):
        tc = TestCase(project_id=DEFAULT_PROJ,
                      work_item_id=self.work_item_id)
        self.assertTrue(tc.add_linked_item(self.work_item_id_2, "verifies"))
        tc2 = TestCase(project_id=DEFAULT_PROJ,
                       work_item_id=self.work_item_id)
        self.assertTrue(len(tc2.linked_work_items) == 1)
        link = tc2.linked_work_items[0]
        self.assertEqual(link.work_item_id, self.work_item_id_2)
        self.assertEqual(link.role, "verifies")
        req3 = Requirement(project_id=DEFAULT_PROJ,
                           work_item_id=self.work_item_id_2)
        self.assertTrue(len(req3.linked_work_items_derived) == 1)
        link = req3.linked_work_items_derived[0]
        self.assertEqual(link.work_item_id, self.work_item_id)
        self.assertEqual(link.role, "verifies")

    def test_create_attachment(self):
        tc = TestCase(project_id=DEFAULT_PROJ,
                      work_item_id=self.work_item_id)
        tc.create_attachment(ATTACH_PATH, "Attached File")
        tc2 = TestCase(project_id=DEFAULT_PROJ,
                       work_item_id=self.work_item_id)
        self.assertTrue(len(tc2.attachments) == 1)
        attach = tc2.attachments[0]
        self.assertEqual(attach.author, tc2.logged_in_user_id)
        self.assertEqual(attach.title, "Attached File")

    def test_create_comment(self):
        tc = TestCase(project_id=DEFAULT_PROJ,
                      work_item_id=self.work_item_id)
        tc.create_comment("This is a comment")
        tc2 = TestCase(project_id=DEFAULT_PROJ,
                       work_item_id=self.work_item_id)
        self.assertTrue(len(tc2.comments) == 1)
        comment = tc2.comments[0]
        self.assertEqual(comment.text, "This is a comment")

    def test_delete_attachment(self):
        tc = TestCase(project_id=DEFAULT_PROJ,
                      work_item_id=self.work_item_id)
        attach = tc.attachments[0]
        tc.delete_attachment(attach.attachment_id)
        tc2 = TestCase(project_id=DEFAULT_PROJ,
                       work_item_id=self.work_item_id)
        self.assertEqual(tc2.attachments, [])

    def test_edit_approval(self):
        tc = TestCase(project_id=DEFAULT_PROJ,
                      work_item_id=self.work_item_id)
        with self.assertRaises(PylarionLibException):
            tc.edit_approval("invalid user", "approved")
        with self.assertRaises(PylarionLibException):
            tc.edit_approval(tc.logged_in_user_id, "invalid status")
        tc.edit_approval(tc.logged_in_user_id, "approved")
        tc2 = TestCase(project_id=DEFAULT_PROJ,
                       work_item_id=self.work_item_id)
        self.assertTrue(len(tc2.approvals) == 1)
        approval = tc2.approvals[0]
        self.assertEqual(approval.status, "approved")
        self.assertEqual(approval.user_id, tc.logged_in_user_id)

    def test_get_back_linked_work_items(self):
        req = Requirement(project_id=DEFAULT_PROJ,
                          work_item_id=self.work_item_id_2)
        items = req.get_back_linked_work_items()
        self.assertTrue(len(items) == 1)
        wi = items[0]
        self.assertEqual(wi.work_item_id, self.work_item_id)

    def test_multiple_types(self):
        req = Requirement()
        tc = TestCase()
        with self.assertRaises(AttributeError):
            tc.reqtype
        with self.assertRaises(AttributeError):
            req.caseimportance
        req.title = "req1"
        tc.title = "tc1"
        self.assertNotEqual(req.title, tc.title)

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
        tc = TestCase(project_id=DEFAULT_PROJ,
                      work_item_id=self.work_item_id)
        tc.set_test_steps(set_steps)
        tc2 = TestCase(project_id=DEFAULT_PROJ,
                       work_item_id=self.work_item_id)
        get_steps = tc2.get_test_steps()
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
        tc = TestCase(project_id=DEFAULT_PROJ,
                      work_item_id=self.work_item_id)
        self.assertFalse(tc.remove_assignee("invalid user"))
        self.assertFalse(tc.remove_assignee("oramraz"))
        self.assertTrue(tc.remove_assignee(tc.logged_in_user_id))

    def test_remove_category(self):
        tc = TestCase(project_id=DEFAULT_PROJ,
                      work_item_id=self.work_item_id)
        self.assertFalse(tc.remove_category("invalid cat"))
        self.assertFalse(tc.remove_category("clustering"))
        self.assertTrue(tc.remove_category("filesystems"))

    def test_remove_hyperlink(self):
        tc = TestCase(project_id=DEFAULT_PROJ,
                      work_item_id=self.work_item_id)
        self.assertTrue(tc.remove_hyperlink(HYPERLINK))

    def test_remove_linked_item(self):
        tc = TestCase(project_id=DEFAULT_PROJ,
                      work_item_id=self.work_item_id)
        self.assertTrue(tc.remove_linked_item(self.work_item_id_2,
                                              "verifies"))

    def test_update(self):
        tc = TestCase(project_id=DEFAULT_PROJ,
                      work_item_id=self.work_item_id)
        tc.status = "approved"
        tc.update()
        tc2 = TestCase(project_id=DEFAULT_PROJ,
                       work_item_id=self.work_item_id)
        self.assertEqual(tc2.status, "approved")


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest2.main()
