import datetime
import os
import unittest

from pylero.exceptions import PyleroLibException
from pylero.plan import Plan
from pylero.work_item import Requirement

TIME_STAMP = datetime.datetime.now().strftime("%Y%m%d%H%M%s")
DEFAULT_PROJ = Plan.default_project
TEMPLATE_ID = "tmp_reg-%s" % TIME_STAMP
PLAN_ID = "plan_reg-%s" % TIME_STAMP

CUR_PATH = os.path.dirname(os.path.abspath(__file__))
ATTACH_PATH = CUR_PATH + "/refs/red_box.png"
ATTACH_TITLE = "File"


class PlanTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        req1 = Requirement.create(
            DEFAULT_PROJ,
            "regression",
            "regression",
            severity="should_have",
            reqtype="functional",
        )

        cls.NEW_REQ = req1.work_item_id
        req2 = Requirement.create(
            DEFAULT_PROJ,
            "regression",
            "regression",
            severity="should_have",
            reqtype="functional",
        )
        cls.NEW_REQ2 = req2.work_item_id

    def test_001_create_template(self):
        """This test does the following:
        * Creates a Plan template with no parent
        * Verifies that the returned object exists and is a template
        The parent attribute is not returned
        """
        template = Plan.create_plan_template(
            TEMPLATE_ID, "Regression", DEFAULT_PROJ, None
        )
        self.assertIsNotNone(template.plan_id)
        self.assertTrue(template.is_template)

    def test_002_create_plan(self):
        """This test does the following:
        * creates a test riun based on the template created in previous test
        * Verifies that the returned object exists and is not a template
        """
        plan = Plan.create(PLAN_ID, "Regression", DEFAULT_PROJ, None, TEMPLATE_ID)
        self.assertIsNotNone(plan.plan_id)
        self.assertFalse(plan.is_template)

    def test_003_search_template(self):
        lst_res = Plan.search("id:%s" % TEMPLATE_ID, search_templates=True)
        self.assertEqual(len(lst_res), 1)
        self.assertEqual(lst_res[0].plan_id, TEMPLATE_ID)

    def test_004_search_plan(self):
        lst_res = Plan.search("id:%s" % PLAN_ID)
        self.assertEqual(len(lst_res), 1)
        self.assertEqual(lst_res[0].plan_id, PLAN_ID)

    def test_005_get_plan(self):
        plan = Plan(project_id=DEFAULT_PROJ, plan_id=PLAN_ID)
        self.assertEqual(plan.plan_id, PLAN_ID)
        plan2 = Plan(uri=plan.uri)
        self.assertEqual(plan2.plan_id, PLAN_ID)

    def test_006_add_items(self):
        plan = Plan(project_id=DEFAULT_PROJ, plan_id=PLAN_ID)
        plan.add_plan_items([self.NEW_REQ, self.NEW_REQ2])
        plan.reload()
        self.assertEqual(len(plan.records), 2)

    def test_007_stats(self):
        plan = Plan(project_id=DEFAULT_PROJ, plan_id=PLAN_ID)
        stats = plan.get_statistics()
        self.assertEqual(stats.number_of_planned, 2)

    def test_008_remove_wi(self):
        plan = Plan(project_id=DEFAULT_PROJ, plan_id=PLAN_ID)
        plan.remove_plan_items([self.NEW_REQ])
        plan.reload()
        self.assertEqual(len(plan.records), 1)
        self.assertEqual(plan.records[0].item, self.NEW_REQ2)

    def test_009_update(self):
        plan = Plan(project_id=DEFAULT_PROJ, plan_id=PLAN_ID)
        plan.color = "red"
        plan.update()
        plan.color = ""
        plan.reload()
        self.assertEqual(plan.color, "red")

    def test_010_delete(self):
        Plan.delete_plans(DEFAULT_PROJ, PLAN_ID)
        with self.assertRaises(PyleroLibException):
            Plan(project_id=DEFAULT_PROJ, plan_id=PLAN_ID)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
