# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function, \
    unicode_literals
import os
import suds
import datetime
from pylarion.exceptions import PylarionLibException
from pylarion.base_polarion import BasePolarion
from pylarion.test_run_attachment import TestRunAttachment
from pylarion.test_run_attachment import ArrayOfTestRunAttachment
from pylarion.enum_option_id import EnumOptionId
from pylarion.test_record import TestRecord
from pylarion.test_record import ArrayOfTestRecord
from pylarion.custom import Custom
from pylarion.custom import ArrayOfCustom
from pylarion.document import Document
from pylarion.work_item import _WorkItem
from pylarion.user import User
from pylarion.project import Project
from pylarion.text import Text


class TestRun(BasePolarion):
    """Object to manage the Polarion Test Management WS tns3:TestRun

    Attributes:
        attachments (list of TestRunAttachments)
        author (User) - user object of the Test Run Author
        created (datetime)
        document (Module)
        finished_on (datetime)
        group_id
        is_template (bool) - indicates if the TestRun object is a Template
        keep_in_history (bool)
        location
        project (Project)
        query (str) - The Polarion query that the TestRun objects are based on.
        records (list of TestRecord objects)
        select_test_cases_by (EnumSelectCasesBy):
            The test cases can be:
                AUTOMATED_PROCESS
                DYNAMIC_QUERY
                DYNAMIC_LIVEDOC
                MANUAL_SELECTION
                STATIC_QUERY
                STATIC_LIVEDOC

        status
        summary_defect (_WorkItem)
        template (TestRun) - template that the TestRun is based on.
        test_run_id (str) - Unique identifier of the test run within the
                            project
        type
        updated
        custom_fields
    """
    _cls_suds_map = {"attachments":
                     {"field_name": "attachments",
                      "is_array": True,
                      "cls": TestRunAttachment,
                      "arr_cls": ArrayOfTestRunAttachment,
                      "inner_field_name": "TestRunAttachment"},
                     "author":
                     {"field_name": "authorURI",
                      "cls": User,
                      "named_arg": "uri",
                      "sync_field": "uri"},
                     "created": "created",
                     "document":
                     {"field_name": "document",
                      "cls": Document},
                     "finished_on": "finishedOn",
                     "group_id": "groupId",
                     "test_run_id": "id",
                     "is_template": "isTemplate",
                     "keep_in_history": "keepInHistory",
                     "location": "location",
                     "project_id":
                     {"field_name": "projectURI",
                      "cls": Project,
                      "named_arg": "uri",
                      "sync_field": "uri"},
                     "query": "query",
                     "records":
                     {"field_name": "records",
                      "is_array": True,
                      "cls": TestRecord,
                      "arr_cls": ArrayOfTestRecord,
                      "inner_field_name": "TestRecord"},
                     "select_test_cases_by":
                     {"field_name": "selectTestCasesBy",
                      "cls": EnumOptionId},
                     "status":
                     {"field_name": "status",
                      "cls": EnumOptionId},
                     "summary_defect":
                     {"field_name": "summaryDefectURI",
                      "cls": _WorkItem,
                      "named_arg": "uri",
                      "sync_field": "uri"},
                     "template":
                     {"field_name": "templateURI",
                      "named_arg": "uri",
                      "sync_field": "uri"},
                     "type":
                     {"field_name": "type",
                      "cls": EnumOptionId},
                     "updated": "updated",
                     "custom_fields":
                     {"field_name": "customFields",
                      "is_array": True,
                      "cls": Custom,
                      "arr_cls": ArrayOfCustom,
                      "inner_field_name": "Custom"},
                     "uri": "_uri",
                     "_unresolvable": "_unresolvable"}
    _id_field = "test_run_id"
    _obj_client = "test_management_client"
    _obj_struct = "tns3:TestRun"

    @classmethod
    def create(cls, project_id, test_run_id, template):
        """class method create for creating a new test run in Polarion

        Args:
            project_id (string) - the Polarion project to create the test run
                                  in
            test_run_id (string) - the unique identifier for the test run
            template (string) - the id of the template to base the test run on.

        Returns:
            The created TestRun object
        Implements:
            test_management.createTestRun
        """
        uri = cls.session.test_management_client.service.createTestRun(
            project_id, test_run_id, template)
        if uri:
            return cls(uri=uri)
        else:
            raise PylarionLibException("Test Run was not created")

    @classmethod
    def create_template(cls, project_id, template_id,
                        parent_template_id="Empty",
                        select_test_cases_by="staticQueryResult", query=None,
                        doc_with_space=None):  # , test_case_ids=[]):
        # see comment below regarding test_case)ids.
        """class method create_template for creating a new template in Polarion

        Args:
            project_id (string) - the Polarion project to create the test run
                                  in
            template_id (string) - the unique identifier for the template
            parent_template_id - the template that this is based onthe ba
            select_test_cases_by - the method used to choose test cases
                                   NOTE: It is currently not possible to select
                                         test cases manually via the API
            query - the Lucene query, for query methods
            doc_with_space - the space/doc_name, for document methods

        Returns:
            The created TestRun Template object
        Implements:
            test_management.createTestRun
        """
        tr = cls.create(project_id, template_id, parent_template_id)
        tr.is_template = True
        tr.select_test_cases_by = select_test_cases_by
        if query:
            tr.query = query
        elif doc_with_space:
            tr.document = Document(project_id, doc_with_space)
# TODO: This should work as soon as Polarion implements Change Request REQ-6334
#        if test_case_ids:
#            for test_case_id in test_case_ids:
#                tr.add_test_record_by_object(testrec.TestRecord(
#                                             test_case_id, project_id))

        tr.update()
        return TestRun(template_id, project_id=project_id)

    @classmethod
    def search(self, query, fields=[], sort="test_run_id", limit=-1,
               search_templates=False):
        """class method search executes the given query and returns the results

        Args:
            query - the Polarion query used to find test runs
            Optional:
                fields -  test run fields that should be initialized,
                          all other fields will be null.
                          Field names are from the object's attributes and not
                          the Polarion field names
                sort - the field used to sort results, default is test_run_id
                limit (int) - the maximum number of records to be returned, -1
                              for no limit.
                search_templates (bool) - if set, searches the templates
                                          instead of the test runs
        Returns:
            list of TestRun objects
        Implements:
            test_management.searchTestRunTemplates
            test_management.searchTestRunTemplatesLimited
            test_management.searchTestRunTemplatesWithFields
            test_management.searchTestRunTemplatesWithFieldsLimited
            test_management.searchTestRuns
            test_management.searchTestRunLimited
            test_management.searchTestRunsWithFields
            test_management.searchTestRunsWithFieldsLimited
        """
# The Polarion functions with limited seem to be the same as without limited
#    when -1 is passed in as limit. Because of this, the wrapper will not
#    implement the functions without limited.
        function_name = "search"
        p_sort = self._cls_suds_map[sort] if not isinstance(
            self._cls_suds_map[sort], dict) else \
            self._cls_suds_map[sort]["field_name"]
        parms = [query, p_sort]
        if search_templates:
            function_name += "TestRunTemplates"
        else:
            function_name += "TestRuns"
        p_fields = self._convert_obj_fields_to_polarion(fields)
        if p_fields:
            function_name += "WithFieldsLimited"
            parms.append(p_fields)
        parms.append(limit)
        test_runs = []
        results = getattr(self.session.test_management_client.service,
                          function_name)(*parms)
        for suds_obj in results:
            tr = TestRun(suds_object=suds_obj)
            test_runs.append(tr)
        return test_runs

    def __init__(self, test_run_id=None, suds_object=None, project_id=None,
                 uri=None):
        """TestRun constructor.

        Args:
            Optional
                test_run_id - when given, the object is populated with the
                              TestRuns. Requires project_id parameter
                suds_object - Polarion TestRun object. When given, the object
                              is populated by object data.
                project_id - the Polarion project that the Test Run is located
                             in.
                        Required if test_run_id is passed in
                uri - the uri that references the Polarion TestRun
        Notes:
            Either test_run_id and project or suds_object or uri can be passed
            in or none of them. If none of the identifying parameters are
            passed in an empty object is created
        Implements:
            test_management.getTestRunById
            test_management.getTestRunByUri
        """
        super(self.__class__, self).__init__(test_run_id, suds_object)
        if test_run_id:
            if not project_id:
                raise PylarionLibException("When test_run_id is passed in, "
                                           "project_id is required")
            self._suds_object = self.session.test_management_client.service. \
                getTestRunById(project_id, test_run_id)
        elif uri:
            self._suds_object = self.session.test_management_client.service. \
                getTestRunByUri(uri)
        if test_run_id or uri:
            if not getattr(self._suds_object, "_unresolvable", None):
                raise PylarionLibException(
                    "The Test Run {0} was not found.".format(test_run_id))

    def _fix_circular_refs(self):
        # a class can't reference itself as a class attribute so it is
        # defined after instatiation
        self._cls_suds_map["template"]["cls"] = self.__class__

    def _get_index_of_test_record(self, test_case_id):
        # specific functions request the index of the test record within the
        # test run. However, the user doesn't know what the index is.
        # Therefore the user passes in the test case id and this function
        # figures out the index.
        index = -1
        for test_record in self.records:
            if test_record.executed:
                index += 1
                if test_case_id in test_record.test_case_uri:
                    return index
        if index == -1:
            raise PylarionLibException("The Test Case is either not part of"
                                       "this TestRun or has not been executed")

    def _verify_record_count(self, record_index):
        # verifies the number of records is not less then the index given.
        self._verify_obj()
        if record_index > len(self.records)-1:
            raise PylarionLibException("There are only {0} test records".
                                       format(len(self.records)))

    def _verify_test_step_count(self, record_index, test_step_index):
        # verifies the number of test steps is not less then the index given.
        self._verify_record_count(record_index)
        if test_step_index > len(self.records[record_index].
                                 test_step_results)-1:
            raise PylarionLibException("There are only {0} test records".
                                       format(len(self.records)))

    def add_attachment_to_test_record(self, test_case_id, path, title):
        """method add_attachment_to_test_record, adds the given attachment to
        the specified test record

        Args:
            test_case_id (str) - The id of the test case
            path - file path to upload
            title - u.User friendly name of the file
        Returns:
            None
        Notes:
            Raises an error if the test case given is not in the TestRun or has
            not been executed yet.
        Implements:
            test_management.addAttachmentToTestRecord
        """
        record_index = self._get_index_of_test_record(test_case_id)
        self._verify_record_count(record_index)
        data = self._get_file_data(path)
        filename = os.path.basename(path)
        self.session.test_management_client.service. \
            addAttachmentToTestRecord(self.uri, record_index, filename,
                                      title, data)

    def add_attachment(self, path, title):
        """method add_attachment adds the given attachment to the current
        test run

        Args:
            path - file path to upload
            title - u.User friendly name of the file
        Returns:
            None
        Notes:
            Raises an error if the test run object is not populated
        Implements:
            test_management.addAttachmentToTestRun
        """
        self._verify_obj()
        data = self._get_file_data(path)
        filename = os.path.basename(path)
        self.session.test_management_client.service. \
            addAttachmentToTestRun(self.uri, filename, title, data)

    def add_attachment_to_test_step(self, test_case_id, test_step_index,
                                    path, title):
        """method add_attachment_to_test_step, adds the given attachment to
        the specified test step of the specified test record

        Args:
            test_case_id (str) - The id of the test case to the step is in
            test_step_index (int) - The 0 based index of the test step
            path - file path to upload
            title - u.User friendly name of the file
        Returns:
            none
        Notes:
            Raises an error if the record_index given is higher then the number
            of test records. or if the test_step_index is higher then the
            number of steps.
        Implements:
            test_management.addAttachmentToTestStep
        """
        record_index = self._get_index_of_test_record(test_case_id)
        self._verify_test_step_count(record_index, test_step_index)
        data = self._get_file_data(path)
        filename = os.path.basename(path)
        self.session.test_management_client.service.addAttachmentToTestStep(
            self.uri, record_index, test_step_index, filename, title, data)

    def add_test_record_by_fields(self, test_case_id, test_result,
                                  test_comment, executed_by, executed,
                                  duration, defect_work_item_id=None):
        """method add_test_record_by_fields, adds a test record for the given
        test case based on the result fields passed in

        Args:
            test_case_id (str) - The id of the test case that was executed
            test_result (str) - Must be one of the following values:
                                   passed
                                   failed
                                   blocked
            test_comment (str or Text object) - may be None
            executed_by (str) - user id
            executed (datetime)
            duration (float)
            defect_work_item_id (str) - _WorkItem id of defect
        Returns:
            None
        Implements:
            test_management.addTestRecord
        """
        self._verify_obj()
        tc = _WorkItem(work_item_id=test_case_id,
                       project_id=self.project_id,
                       fields=["work_item_id"])
        if test_comment:
            if isinstance(test_comment, basestring):
                obj_comment = Text(obj_id=test_comment)
                suds_comment = obj_comment._suds_object
            elif isinstance(test_comment, Text):
                suds_comment = test_comment._suds_object
            else:  # is a suds object
                suds_comment = test_comment
        else:
            suds_comment = suds.null()
        user = User(user_id=executed_by)
        if defect_work_item_id:
            defect = _WorkItem(work_item_id=defect_work_item_id,
                               project_id=self.project_id,
                               fields=["work_item_id"])
            defect_uri = defect.uri
        else:
            defect_uri = None
        self.session.test_management_client.service.addTestRecord(
            self.uri, tc.uri, test_result, suds_comment,
            user.uri, executed, duration, defect_uri)

    def add_test_record_by_object(self, test_record):
        """method add_test_record_by_object, adds a test record for the given
        test case based on the TestRecord object passed in

        Args:
            test_record (TestRecord or Polarion TestRecord)
        Returns:
            None
        Implements:
            test_management.addTestRecordToTestRun
        """
        self._verify_obj()
        if isinstance(test_record, TestRecord):
            suds_object = test_record._suds_object
        elif isinstance(test_record, TestRecord().
                        _suds_object.__class__):
            suds_object = test_record
        self.session.test_management_client.service.addTestRecordToTestRun(
            self.uri, suds_object)

    def create_summary_defect(self, defect_template_id=None):
        """method create_summary_defect, adds a new summary _WorkItem for the
        test case based on the _WorkItem template id passed in. If not template
        is passed in, it creates it based on the default template.

        Args:
            defect_template_id (str) - the _WorkItem template id to base the
            new summary defect. can be null
        Returns:
            the created _WorkItem
        Implements:
            test_management.createSummaryDefect
        """

        self._verify_obj()
        suds_defect_template = _WorkItem(work_item_id=defect_template_id,
                                         project_id=self.project_id)
        defect_template_uri = suds_defect_template._uri
        wi_uri = self.session.test_management_client.service. \
            createSummaryDefect(self.uri, defect_template_uri)
        return _WorkItem(uri=wi_uri)

    def delete_attachment_from_test_record(self, test_case_id, filename):
        """Deletes Test Record Attachment of specified record and
        attachment's file name.
        Args:
            test_case_id - The test case to delete the attachment from
            filename - name of the file to delete
        Returns:
            None
        Implements:
            test_management.deleteAttachmentFromTestRecord
        """
        record_index = self._get_index_of_test_record(test_case_id)
        self._verify_record_count(record_index)
        self.session.test_management_client.service. \
            deleteAttachmentFromTestRecord(self.uri, record_index, filename)

    def delete_attachment_from_test_step(self, test_case_id, test_step_index,
                                         filename):
        """Deletes Test Step Attachment of the specified step in the specified
        test record.
        Args:
            test_case_id - The test case to delete the attachment from
            filename - name of the file to delete
        Returns:
            None
        Implements:
            test_management.deleteAttachmentFromTestRecord
        """
        record_index = self._get_index_of_test_record(test_case_id)
        self._verify_test_step_count(record_index, test_step_index)
        self.session.test_management_client.service. \
            deleteAttachmentFromTestStep(self.uri, record_index,
                                         test_step_index, filename)

    def delete_attachment(self, filename):
        """Deletes Test Run Attachment specified by attachment's
        file name. Method is applicable also on Test Run Template.
        Args:
            filename - filename to delete
        Returns:
            None
        Implements:
            test_management.deleteTestRunAttachment
        """
        self._verify_obj()
        self.session.test_management_client.service. \
            deleteTestRunAttachment(self.uri, filename)

    def get_attachment(self, filename):
        """Gets Test Run Attachment specified by attachment's
        file name. Method is applicable also on Test Run Template.
        Args:
            filename - filename to delete
        Returns:
            TestRunAttachment object
        Implements:
            test_management.getTestRunAttachment
        """
        self._verify_obj()
        suds_attach = self.session.test_management_client.service. \
            getTestRunAttachment(self.uri, filename)
        return TestRunAttachment(suds_object=suds_attach)

    def get_attachments(self):
        """method get_attachments returns all the attachments for the TestRun
        Args:
            None
        Returns:
            ArrayOfTestRunAttachments object
        Implements:
            test_management.getTestRunAttachments
        """
        self._verify_obj()
        suds_attach = self.session.test_management_client.service. \
            getTestRunAttachments(self.uri)
        obj_attach = ArrayOfTestRunAttachment(suds_object=suds_attach)
        return obj_attach

    def get_custom_field(self, field_name):
        """gets custom field values.
        Args:
            field_name - name of the custom field
        Returns:
            value of the custom field.
        Note: Polarion WSDL currently does not publish the list of custom
              fields, so this function cannot do any verification if the field
              is valid.
        """
        self._verify_obj()
        cf = self.custom_fields
        match = filter(lambda x: x.key == field_name, cf)
        if match:
            return match[0].value
        else:
            return None

    def get_wiki_content(self):
        """method get_wiki_content returns the wiki content for the Test Run
        Args:
            None
        Returns:
            Text object containing the wiki content
        Implements:
            test_management.getWikiContentForTestRun
        """
        self._verify_obj()
        suds_wiki = self.session.test_management_client.service. \
            getWikiContentForTestRun(self.uri)
        return Text(suds_object=suds_wiki)

    def set_custom_field(self, field_name, value):
        """sets custom field values.
        Args:
            field_name - name of the custom field
        Returns:
            value of the custom field.
        Note: Polarion WSDL currently does not publish the list of custom
              fields, so this function cannot do any verification if the field
              or value is valid.
        """
        self._verify_obj()
        cf = self.custom_fields
        cust = Custom()
        cust.key = field_name
        cust.value = value
        if cf:
            # check if the custom field already exists and if so, modify it.
            match = filter(lambda x: x.key == field_name, cf)
            if match:
                match[0].value = value
            else:
                cf.append(cust)
        else:
            cf = [cust]
        self.custom_fields = cf

    def update(self):
        """method update updates the testRun object with the attribute values
        currently in the object.

        Args:
            None
        Returns
            None
        Implements:
            test_management.updateTestRun
        """
        self._verify_obj()
        self.session.test_management_client.service.updateTestRun(
            self._suds_object)

    def update_attachment(self, path, original_filename, title):
        """method update_attachment updates the specified attachment to the
        current test run

        Args:
            path - file path to upload
            original_filename - The file that we want to overwrite with the new
                                file
            title - u.User friendly name of the file
        Returns:
            None
        Notes:
            Raises an error if the test run object is not populated.
        Implements:
            test_management.updateTestRunAttachment
        """
        self._verify_obj()
        data = self._get_file_data(path)
        filename = os.path.basename(original_filename)
        self.session.test_management_client.service. \
            updateTestRunAttachment(self.uri, filename, title, data)

    def update_summary_defect(self, source, total_failures, total_errors,
                              total_tests, defect_template_id):
        """method update-summary_defect creates or updates the summary defect
        Work Item of a test run.

        Args:
            source (string) - source of the summary defect, used to generate
                              the description content.
            total_failures (int) - amount of total failures in the test run,
                                   used to generate the description content.
            total_errors (int) - amount of total errors in the test run,
                                 used to generate the description content.
            total_tests (int) - amount of total tests in the test run,
                                used to generate the description content.
            defect_template_id - ID of the defect template Work Item to be
                                 used, the configured template will be used if
                                 None.
        Returns:
            the created or updated _WorkItem
        Implements:
            test_management.updateSummaryDefect
        """
        self._verify_obj()
        suds_defect_template = _WorkItem(work_item_id=defect_template_id,
                                         project_id=self.project_id)
        defect_template_uri = suds_defect_template._uri
        wi_uri = self.session.test_management_client.service. \
            updateSummaryDefect(self.uri, source, total_failures, total_errors,
                                total_tests, defect_template_uri)
        return _WorkItem(uri=wi_uri)

    def update_test_record_by_fields(self, test_case_id,
                                     test_result=suds.null(),
                                     test_comment=None,
                                     executed_by=suds.null(),
                                     executed=datetime.datetime.now(),
                                     duration=suds.null(),
                                     defect_work_item_id=None):
        """method update_test_record_by_fields updates a test record.

        Args:
            test_case_id - id of the test case to update.
            test_result - Must be one of the following values:
                                   passed
                                   failed
                                   blocked
            test_comment - (str or Text object) - may be None
            executed_by (str) - user id
            executed - date when the test case has been executed,
                       default is now.
            duration - duration of the test case execution, any negative value
                       is treated as None.
            defect_work_item_id - _WorkItem id of defect, can be None

        Returns:
            None
        Notes:
            Only a test case that has already been executed may be updated
            using this function. To execute a test record use the
            add_test_record_by_fields function
        Implements:
            test_management.updateTestRecord
        """
        self._verify_obj()
        index = self._get_index_of_test_record(test_case_id)
        if defect_work_item_id:
            defect = _WorkItem(work_item_id=defect_work_item_id,
                               project_id=self.project_id,
                               fields=["work_item_id"])
            defect_uri = defect.uri
        else:
            defect_uri = suds.null()
        if test_comment:
            if isinstance(test_comment, basestring):
                obj_comment = Text(obj_id=test_comment)
                suds_comment = obj_comment._suds_object
            elif isinstance(test_comment, Text):
                suds_comment = test_comment._suds_object
            else:  # is a suds object
                suds_comment = test_comment
        else:
            suds_comment = suds.null()
        user = User(user_id=executed_by)
        self.session.test_management_client.service. \
            updateTestRecord(self.uri, index, test_result, suds_comment,
                             user.uri, executed, duration, defect_uri)

    def update_test_record_by_object(self, test_case_id, test_record):
        """method update_test_record_by_object, adds a test record for the
        given test case based on the TestRecord object passed in

        Args:
            test_case_id (str), the test case id that the record is related to.
            test_record (TestRecord or Polarion TestRecord)
        Returns:
            None
        Implements:
            test_management.updateTestRecordAtIndex
        """
        self._verify_obj()
        index = self._get_index_of_test_record(test_case_id)
        if isinstance(test_record, TestRecord):
            suds_object = test_record._suds_object
        elif isinstance(test_record, TestRecord().
                        _suds_object.__class__):
            suds_object = test_record
        self.session.test_management_client.service.updateTestRecordAtIndex(
            self.uri, index, suds_object)

    def update_wiki_content(self, content):
        """method update_wiki_content updates the wiki for the current TestRun

        Args:
            Content (str or Text object)
        Returns:
            None
        Implements:
            test_management.updateWikiContentForTestRun
        """
        self._verify_obj()
        if content:
            if isinstance(content, basestring):
                obj_content = Text(obj_id=content)
                suds_content = obj_content._suds_object
            elif isinstance(content, Text):
                suds_content = content._suds_object
            else:  # is a suds object
                suds_content = content
        else:
            suds_content = suds.null()
        self.session.test_management_client.service. \
            updateWikiContentForTestRun(self.uri, suds_content)
