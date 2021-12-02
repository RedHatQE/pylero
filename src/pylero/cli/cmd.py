# -*- coding: utf8 -*-
from __future__ import print_function

import datetime
import os

from pylero._compatible import object
from pylero._compatible import str
from pylero.document import Document
from pylero.plan import Plan
from pylero.test_run import TestRun
from pylero.work_item import Requirement
from pylero.work_item import TestCase


class CmdList(object):
    ''' An object to manage the command of list'''

    def list_documents_by_query(self,
                                query):
        fields = ['document_id',
                  'document_name',
                  'author',
                  'created',
                  'updated',
                  'updated_by']
        doc_list = Document.query(query, False, fields)

        return doc_list

    def print_documents(self, docs):
        print('Created%7sAuthor%7sDocument' % ('', ''))
        print('-------%7s------%7s--------' % ('', ''))

        for doc in docs:
            print('%-14s %-11s %s' % (doc.created.strftime('%Y-%m-%d'),
                                      doc.author,
                                      doc.document_id))

    def list_workitems_in_doc(self, doc_name_with_space):
        if doc_name_with_space.find('/') < 0:
            print("Document format should be: 'space/document'")
            exit(1)

        doc = Document(Document.default_project, doc_name_with_space)
        fields = ['work_item_id',
                  'author',
                  'title',
                  'type',
                  'status',
                  'assignee',
                  'categories',
                  'comments',
                  'created',
                  'approvals',
                  'updated']
        self.workitem_list = doc.get_work_items(None, True, fields)
        return self.workitem_list

    def print_workitems(self, workitems):
        number = len(workitems)
        print('\nTotal workitems: %d' % number)
        print('Created%7sType%10sID%12sTitle' % ('', '', ''))
        print('---------%5s-------%7s-----%9s--------' % ('', '', ''))

        for wi in workitems:
            created = str(wi.created).split(' ')[0]
            print('%-13s %-13s %-13s %s' % (created, wi.type,
                                            wi.work_item_id, wi.title))

    def list_workitems_by_query(self, query, wi_type):
        fields = ['work_item_id',
                  'title',
                  'author',
                  'created']

        if wi_type in ["testcase", "TestCase"]:
            workitem_list = TestCase.query(query, fields)
        elif wi_type in ["requirement", "Requirement"]:
            workitem_list = Requirement.query(query, fields)
        elif wi_type == '':
            workitem_list = TestCase.query(query, fields) + \
                Requirement.query(query, fields)
        else:
            print("'%s' is invalid. Use testcase or requirement" % wi_type)
            exit(0)

        return workitem_list

    def print_steps_for_testcase(self, case_id):
        tc = TestCase(TestCase.default_project, case_id)
        steps = tc.get_test_steps()

        for step in steps.steps:
            stp = step.values[0].content
            exp = step.values[1].content
            print('TestStep       = %s' % stp)
            print('ExpectedResult = %s\n' % exp)

        if steps.steps is None:
            print('No step for this tesecase!')

    def print_links_for_requirement(self, req_id):
        req = Requirement(Requirement.default_project, req_id)
        print('ID%-12sRole' % (''))
        print('-------%7s------' % (''))

        for linked in req.linked_work_items_derived:
            print('%-13s %-13s' % (linked.work_item_id,
                                   linked.role))

    def print_links_for_testcase(self, case_id):
        tc = TestCase(TestCase.default_project, case_id)
        print('ID%-12sRole' % (''))
        print('-------%7s------' % (''))

        for linked in tc.linked_work_items:
            print('%-13s %-13s' % (linked.work_item_id,
                                   linked.role))

    def print_runs_by_query(self, query, is_template=False):
        query_ful = 'project.id:%s AND %s' % (TestRun.default_project, query)
        fields = ['query',
                  'created',
                  'test_run_id',
                  'select_test_cases_by',
                  'status',
                  'plannedin',
                  'assignee',
                  'author']

        st = TestRun.search(query_ful,
                            fields,
                            'created',
                            -1,
                            is_template)
        Object = ''
        if is_template:
            Object = 'Template'

        prestr = 'Created Time %8sAuthor %3sAssignee' % ('', '')
        latstr = '%sStatus %3sPlanID%10s%s' % ('', '', '', Object)
        preln = '------------%9s------%4s------' % ('', '')
        latln = '%2s--------%2s-------%9s--------' % ('', '', '')

        print('%s %s' % (prestr, latstr))
        print('%s %s' % (preln, latln))

        for tp in st:
            created_time = str(tp.created).split('.')[0]
            print('%-20s %-9s %-8s %-10s%-15s %s' % (created_time,
                                                     tp.author,
                                                     tp.assignee,
                                                     tp.status,
                                                     tp.plannedin,
                                                     tp.test_run_id))

    def print_templates_by_query(self, query):
        self.print_runs_by_query(query, True)

    def print_testcases_from_run(self, run):
        tr = TestRun(run, None, TestRun.default_project)
        print('(Only CaseID can be displayed when --run=$template)')
        print('List cases for: %s\n' % run)
        ttstr = ('Created Time %8sStatus %1sExecutedBy %2sCaseID' % ('',
                                                                     '',
                                                                     ''))
        lnstr = ('------------%9s------%2s----------%3s------' % ('', '', ''))
        print(ttstr)
        print(lnstr)

        for rec in tr.records:
            time = str(rec.executed).split('.')[0]
            print('%-21s%-9s%-12s%-10s' % (time,
                                           rec.result,
                                           rec.executed_by,
                                           rec.test_case_id))

    def print_plan_ids(self, query):
        pls = Plan.search(query,
                          sort='due_date',
                          limit=-1,
                          fields=['due_date',
                                  'name',
                                  'plan_id'])

        ttstr = ('Due Date%-5sPlan ID%-24sPlan Name' % ('', ''))
        lnstr = ('-----------  ---------- %-20s---------' % '')
        print(ttstr)
        print(lnstr)

        for pl in pls:
            print('%-12s %-30s %s' % (pl.due_date, pl.plan_id, pl.name))


class CmdUpdate(object):
    ''' An object to manage the command of update'''

    def update_all_case_results_for_run(self, run, result, user, comment):

        run = run.strip()
        tr = TestRun(run, None, TestRun.default_project)
        print('\nUpdate %s:' % run)

        if not comment:
            comment = ''

        print('Total records: %d' % len(tr.records))
        print('Updated Date Time    Result  CaseID')
        print('-------------------  ------  -----------')

        if user == 'None':
            user = TestRun.logged_in_user_id

        for rec in tr.records:
            rec.executed = datetime.datetime.now()
            rec.executed_by = user
            executed_str = str(rec.executed).split('.')[0]
            rec.result = result
            rec.comment = comment

            print('%-20s %-7s %s' % (executed_str,
                                     result,
                                     rec.test_case_id))
            tr.update_test_record_by_object(rec.test_case_id,
                                            rec)
        print('Done!')

    def update_all_case_results_for_runs(self, runs, result, user, comment):
        if runs.find(','):
            for run in runs.split(','):
                self.update_all_case_results_for_run(run, result,
                                                     user, comment)
        else:
            print("Please use comma ',' to seperate your runs!")

    def update_1_case_result_for_run(self,
                                     run,
                                     testcase,
                                     result,
                                     user,
                                     comment):

        if not comment:
            comment = ''

        tr = TestRun(run.strip(), None, TestRun.default_project)
        print('Update %s:' % run)

        if user == 'None':
            user = TestRun.logged_in_user_id

        is_found = False
        for rec in tr.records:
            if rec.test_case_id == testcase:
                is_found = True
                rec.executed = datetime.datetime.now()
                rec.executed_by = user
                rec.result = result
                rec.comment = comment

                tr.update_test_record_by_object(testcase, rec)
                print("%4sSet %s to %s (verdict comment: '%s')" % ('',
                                                                   testcase,
                                                                   result,
                                                                   comment))
                return 0

        if not is_found:
            print('Test case %s is not found in run.' % testcase)

    def update_document(self,
                        space,
                        doc_name,
                        doc_title,
                        wi_types=None,
                        doc_type=None,
                        structure_link_role="parent",
                        content=''):

        cl = CmdList()
        if cl.list_documents_by_query(doc_name):
            print("Exit - Found same name '%s/%s'" % (space, doc_name))
            return

        file_path = ""
        # the content could be file or data
        if os.path.exists(content):
            file_path = content
            with open(content, mode='r') as check_file:
                content = check_file.read()

        doc = Document.create(Document.default_project,
                              space,
                              doc_name,
                              doc_title,
                              wi_types,
                              doc_type,
                              structure_link_role,
                              content)

        if cl.list_documents_by_query(doc_name):
            print("Created document '%s/%s'" % (space, doc_name))
            print(" - document author      : %s" % doc.author)
            print(" - document type        : %s" % doc.type)
            print(" - allowed workitem type: %s" % wi_types)
            print(" - created date         : %s" % doc.created)
            if file_path != "":
                print(" - document content is from: %s" % file_path)
            else:
                print(" - document content     : %s" % content)
            return True
        else:
            print("Failed to create document '%s/%s'" % (space, doc_name))
            return False

    def update_run(self,
                   run,
                   template=None,
                   plannedin=None,
                   assignee=None,
                   status=None,
                   description=None,
                   is_template=False):

        run = run.strip()
        query_ful = 'project.id:%s AND id:\"%s\"' % (TestRun.default_project,
                                                     run)

        fields = ['query',
                  'created',
                  'test_run_id',
                  'select_test_cases_by',
                  'status',
                  'plannedin',
                  'assignee',
                  'author']
        st = TestRun.search(query_ful,
                            fields,
                            'created',
                            -1,
                            is_template)

        # Update run if exists, otherwise create it.
        if st:
            print('Update the existing run: %s' % run)
            tr = TestRun(run,
                         None,
                         TestRun.default_project)

            # set fields
            if assignee != 'None':
                tr.assignee = assignee
                print('%4sSet Assignee to %s' % ('', assignee))
            if plannedin is not None:
                tr.plannedin = plannedin
                print('%4sSet Plannedin to %s' % ('', plannedin))
            if status is not None:
                tr.status = status
                print('%4sSet Status to %s' % ('', status))
            if description is not None:
                tr.description = description
                print('%4sSet Description to %s' % ('', description))
            tr.update()

        else:
            tr = TestRun.create(TestRun.default_project,
                                run,
                                template,
                                assignee=assignee,
                                plannedin=plannedin,
                                status=status,
                                description=description)
            # display fields
            if assignee != 'None':
                print('%4sSet Assignee to %s' % ('', assignee))
            if plannedin is not None:
                print('%4sSet Plannedin to %s' % ('', plannedin))
            if status is not None:
                print('%4sSet Status to %s' % ('', status))
            if description is not None:
                print('%4sSet Description to %s' % ('', description))
            print('Created %s:' % run)

    def update_runs(self,
                    runs,
                    template=None,
                    plannedin=None,
                    assignee=None,
                    status=None,
                    description=None):

        if runs.find(','):
            for run in runs.split(','):
                self.update_run(run,
                                template,
                                plannedin,
                                assignee,
                                status,
                                description)
            print('Done!')
        else:
            print("Please use comma ',' to seperate your runs!")
