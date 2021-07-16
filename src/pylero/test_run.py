# -*- coding: utf8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os

import suds
from pylero._compatible import basestring
from pylero._compatible import classmethod
from pylero._compatible import object  # noqa
from pylero._compatible import range
from pylero.base_polarion import BasePolarion
from pylero.base_polarion import tx_wrapper
from pylero.build import Build  # noqa: F401
from pylero.custom import ArrayOfCustom
from pylero.custom import Custom
from pylero.custom_field_type import CustomFieldType
from pylero.document import Document
from pylero.enum_custom_field_type import EnumCustomFieldType
from pylero.enum_option_id import ArrayOfEnumOptionId
from pylero.enum_option_id import EnumOptionId
from pylero.exceptions import PyleroLibException
from pylero.plan import Plan  # NOQA
from pylero.project import Project
from pylero.test_record import ArrayOfTestRecord
from pylero.test_record import TestRecord
from pylero.test_run_attachment import ArrayOfTestRunAttachment
from pylero.test_run_attachment import TestRunAttachment
from pylero.text import Text
from pylero.user import User
from pylero.work_item import _WorkItem
from pylero.work_item import TestCase
# Build is used in custom fields.
# Plan is used in custom fields.


def generate_description(test_run, test_case, test_record):
    tr_html = "<b>Test Run:</b> <span id=\"link\" class=    " \
              "\"polarion-rte-link\" data-type=\"testRun\" " \
              "data-item-id=\"{0}\" data-option-id=\"long\">" \
              "</span><br/>".format(test_run.test_run_id)
    tc_html = "<b>Test Case:</b> <span id=\"link\" class=" \
              "\"polarion-rte-link\" data-type=\"workItem\" " \
              "data-item-id=\"{0}\" data-option-id=\"long\"></span>" \
              "<br/>".format(test_case.work_item_id)
    table_cell_style = "style=\"text-align: left; padding: 10px; " \
                       "vertical-align: top; background-color: #ffffff;\""
    table_row_style = "style=\"border-bottom: 1px solid #f0f0f0;\""
    columns = ["", "#", "<span title=\"Step\">Step</span>",
               "<span title=\"Expected Result\">Expected Result</span>",
               "Actual Result"]
    test_step_results = {"passed": "<span title=\"Results met expected results"
                                   "\"><span style=\"white-space:nowrap;\"><im"
                                   "g src=\"/polarion/icons/default/enums/test"
                                   "run_status_passed.png\" style=\"vertical-a"
                                   "lign:text-bottom;border:0px;margin-right:2"
                                   "px;\" class=\"polarion-no-style-cleanup\"/"
                                   "></span></span>",
                         "failed": "<span title=\"Results did not meet expecte"
                                   "d results\"><span style=\"white-space:nowr"
                                   "ap;\"><img src=\"/polarion/icons/default/e"
                                   "nums/testrun_status_failed.png\" style=\"v"
                                   "ertical-align:text-bottom;border:0px;margi"
                                   "n-right:2px;\" class=\"polarion-no-style-c"
                                   "leanup\"/></span></span>",
                         "blocked": "<span title=\"Errors in the product preve"
                                    "nted test from being executed\"><span sty"
                                    "le=\"white-space:nowrap;\"><img src=\"/po"
                                    "larion/icons/default/enums/testrun_status"
                                    "_blocked.png\" style=\"vertical-align:tex"
                                    "t-bottom;border:0px;margin-right:2px;\" c"
                                    "lass=\"polarion-no-style-cleanup\"/>"
                                    "</span></span>"}
    table_header = "<table class=\"polarion-no-style-cleanup\" style=\"border"\
                   "-collapse: collapse;\"><tr style=\"text-align: left; " \
                   "white-space: nowrap; color: #757575; border-bottom: 1px " \
                   "solid #d2d7da; background-color: #ffffff;\">{0}</tr>" \
        .format("".join(["<th {0}>{1}</th>".format(table_cell_style, column)
                         for column in columns]))
    verdict = "</table><table style=\"margin-bottom: 15px; ;border-collapse: "\
              "collapse; width:100%; ;margin-top: 13px;\" class=\"polarion-no"\
              "-style-cleanup\"><tr><th style=\"width: 80%; text-align: left;"\
              " background-color: #ffffff;\">Test Case Verdict:</th></tr><tr>"\
              "<td style=\"vertical-align: top;\"><span style=\"font-weight: "\
              "bold;\"><span style=\"color: #C30000;\"><span title=\"Results "\
              "did not meet expected results\"><span style=\"white-space:" \
              "nowrap;\"><img src=\"/polarion/icons/default/enums/testrun_" \
              "status_failed.png\" style=\"vertical-align:text-bottom;border:"\
              "0px;margin-right:2px;\" class=\"polarion-no-style-cleanup\"/>" \
              "</span>Failed</span></span></span><span> {0}</span></td></tr>" \
              "</table>" \
        .format(test_record.comment)
    table_rows = ""
    for step in range(len(test_record.test_step_results)):
        table_rows += "<tr {0}>" \
                      "<td {1}>{2}</td>" \
                      "<td {1}>{3}</td>" \
                      "<td {1}>{4}</td>" \
                      "<td {1}>{5}</td>" \
                      "<td {1}>{6}</td>" \
                      "</tr>".format(table_row_style,
                                     table_cell_style,
                                     test_step_results.
                                     get(test_record.test_step_results[step]
                                         .result),
                                     step + 1,
                                     test_case.test_steps.steps[step].values[0]
                                     .content,
                                     test_case.test_steps.steps[step].values[1]
                                     .content,
                                     test_record.test_step_results[step]
                                     .comment)
    content = tr_html + tc_html + table_header + table_rows + verdict

    return content


def create_incident_report(test_run, test_record, test_case):
    project_id = test_run.project_id
    status = 'open'
    project = Project(project_id)
    tconf = project.get_tests_configuration()
    defectWorkItemType = tconf.defect_work_item_type
    title = 'Failed: ' + test_case.title
    description = generate_description(test_run, test_case, test_record)
    kwarg_dict = {}

    for prop in tconf.fields_to_copy_from_test_case_to_defect.property:
        kwarg_dict[prop.value] = getattr(test_case, prop.key)
    for prop in tconf.fields_to_copy_from_test_run_to_linked_defect.property:
        kwarg_dict[prop.value] = getattr(test_run, prop.key)

    incident_report = _WorkItem.create(project_id, defectWorkItemType, title,
                                       description, status, **kwarg_dict)
    incident_report.add_linked_item(test_case.work_item_id, "triggered_by")
    return incident_report.work_item_id


class TestRun(BasePolarion):
    """Object to manage the Polarion Test Management WS tns3:TestRun

    Attributes:
        attachments (list of TestRunAttachments)
        author (User): user object of the Test Run Author
        created (datetime)
        document (Module)
        finished_on (datetime)
        group_id
        is_template (bool): indicates if the TestRun object is a Template
        keep_in_history (bool)
        location
        project (Project)
        query (str): The Polarion query that the TestRun objects are based on.
        records (list of TestRecord objects)
        select_test_cases_by (EnumOptionId):
            The test cases can be:
                AUTOMATED_PROCESS
                DYNAMIC_QUERY
                DYNAMIC_LIVEDOC
                MANUAL_SELECTION
                STATIC_QUERY
                STATIC_LIVEDOC

        status
        summary_defect (_WorkItem)
        template (TestRun): template that the TestRun is based on.
        test_run_id (str): Unique identifier of the test run within the
                           project
        type
        updated
        custom_fields
    """
    _cls_suds_map = {
        "attachments":
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
        "_records":
            {"field_name": "records",
             "is_array": True,
             "cls": TestRecord,
             "arr_cls": ArrayOfTestRecord,
             "inner_field_name": "TestRecord"},
        "select_test_cases_by":
            {"field_name": "selectTestCasesBy",
             "cls": EnumOptionId,
             "enum_id": "testrun-selectTestCasesBy"},
        "status":
            {"field_name": "status",
             "cls": EnumOptionId,
             "enum_id": "testing/testrun-status"},
        "summary_defect":
            {"field_name": "summaryDefectURI",
             "cls": _WorkItem,
             "named_arg": "uri",
             "sync_field": "uri"},
        "title": "title",
        "template":
            {"field_name": "templateURI",
             "named_arg": "uri",
             "sync_field": "uri"},
        "type":
            {"field_name": "type",
             "cls": EnumOptionId,
             "enum_id": "testing/testrun-type"},
        "updated": "updated",
        # the custom field attribute has been changed to be a protected attr.
        # All interaction with custom fields should be done directly with the
        # derived attribute.
        "_custom_fields":
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
    _custom_field_cache = {}

    @property
    def records(self):
        """ function to return all the test records of a TestRun.
        The records array for dynamic queries/documents only includes executed
        records. This returns the unexecuted ones as well.

        Args:
            None

        Returns:
            list of TestRecords
        """
        self._verify_obj()
        # if the type is not dynamic then all the cases are in the _records
        # attribute. If they are dynamic, they have to be gotten
        if "dynamic" not in self.select_test_cases_by:
            return self._records
        if "Doc" in self.select_test_cases_by:
            cases = self.document.get_work_items(None, True)
        elif "Query" in self.select_test_cases_by:
            cases = _WorkItem.query(
                self.query + " AND project.id:" + self.project_id)
        else:
            raise PyleroLibException("Only Test Runs based on Docs or"
                                     " Queries can be dynamic")
        executed_ids = [rec.test_case_id for rec in self._records]
        test_recs = self._records
        for case in cases:
            if case.work_item_id not in executed_ids \
                    and case.type != "heading":
                test_recs.append(
                    TestRecord(self.project_id, case.work_item_id))
        return test_recs

    @records.setter
    def records(self, val):
        self._records = val

    @classmethod
    @tx_wrapper
    def create(cls, project_id, test_run_id=None, template=None, title=None,
               **kwargs):
        """class method create for creating a new test run in Polarion

        Args:
            project_id (string): the Polarion project to create the test run
                                 in
            test_run_id (string): the unique identifier for the test run,
                                  If the Enable Generated Test Run IDs option
                                  is marked in the configuration, it will
                                  ignore this field. If it is None, the title
                                  will be used.
            template (string): the id of the template to base the test run on.
                               cannot be None. Because of the existing order of
                               params before adding title, it is given a
                               default value of None, which will cause an error
                               if it is not populated
            title (string): To create a test run with a title. In this case,
                            if the id is not populated it will be autogen.
                            If it is populated, it will use that.
            **kwargs: keyword arguments. Test run attributes can be passed in
                      to be set upon creation. Required fields must be passed
                      in

        Returns:
            The created TestRun object

        References:
            test_management.createTestRun
        """
        if not template:
            raise PyleroLibException("Template is required")
        if title:
            uri = cls.session.test_management_client.service.\
                createTestRunWithTitle(
                    project_id, test_run_id or title, title, template)
        else:
            uri = cls.session.test_management_client.service.createTestRun(
                project_id, test_run_id, template)
        if uri:
            run = cls(uri=uri)
            run.verify_params(**kwargs)
            for field in kwargs:
                setattr(run, field, kwargs[field])
            run.update()
            return run
        else:
            raise PyleroLibException("Test Run was not created")

    @classmethod
    @tx_wrapper
    def create_template(cls, project_id, template_id,
                        parent_template_id="Empty",
                        select_test_cases_by=None, query=None,
                        doc_with_space=None, **kwargs):  # , test_case_ids=[]):
        # see comment below regarding test_case)ids.
        """class method create_template for creating a new template in Polarion

        Args:
            project_id (string): the Polarion project to create the test run
                                 in
            template_id (string): the unique identifier for the template
            parent_template_id: the template that this is based on
                                Default: "Empty"
            select_test_cases_by: the method used to choose test cases
                                  NOTE: It is currently not possible to select
                                  test cases manually via the API.
                                  Default: None
            query: the Lucene query, for query methods, default None
            doc_with_space: the space/doc_name, for document methods
                            default: None
            **kwargs: keyword arguments. Test run attributes can be passed in
                      to be set upon creation. Required fields must be passed
                      in

        Returns:
            The created TestRun Template object

        References:
            test_management.createTestRun
        """
        tr = cls.create(project_id, template_id, parent_template_id, **kwargs)
        tr.is_template = True
        if select_test_cases_by:
            tr.select_test_cases_by = select_test_cases_by
        elif doc_with_space:
            tr.select_test_cases_by = "dynamicLiveDoc"
        elif query:
            tr.select_test_cases_by = "dynamicQueryResult"

        # you can have both a query and a document, through which the query
        # qualifies the doc.
        if query:
            tr.query = query
        if doc_with_space:
            tr.document = Document(project_id, doc_with_space)
# TODO: This should work as soon as Polarion implements Change Request REQ-6334
        #        if test_case_ids:
        #            for test_case_id in test_case_ids:
        #                tr.add_test_record_by_object(testrec.TestRecord(
        #                                            test_case_id,
        #                                            project_id))

        tr.update()
        return TestRun(tr.test_run_id, project_id=project_id)

    @classmethod
    def search(cls, query, fields=["test_run_id"], sort="test_run_id",
               limit=-1, search_templates=False, project_id=None):
        """class method search executes the given query and returns the results

        Args:
            query: the Polarion query used to find test runs
            fields:  test run fields that should be initialized,
                     all other fields will be null.
                     Field names are from the object's attributes and not
                     the Polarion field names, default ["test_run_id"]. If you
                     want all of the fields to be returned, pass [] for this
                     parameter.
            sort: the field used to sort results, default is test_run_id
            limit (int): the maximum number of records to be returned, -1
                         for no limit, default -1.
            search_templates (bool): if set, searches the templates
                                     instead of the test runs, default False
            project_id: if set, searches the project id, else default project
        Returns:
            list of TestRun objects

        References:
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
        project_id = project_id or cls.default_project
        query += " AND project.id:%s" % (project_id)

        # The following line one purpose is to instantiate a TestRun and by
        # doing so setting all the class attribute (including 'customFields').
        TestRun(project_id=project_id)
        function_name = "search"
        p_sort = cls._cls_suds_map[sort] if not isinstance(
            cls._cls_suds_map[sort], dict) else \
            cls._cls_suds_map[sort]["field_name"]
        parms = [query, p_sort]
        if search_templates:
            function_name += "TestRunTemplates"
        else:
            function_name += "TestRuns"
        p_fields = cls._convert_obj_fields_to_polarion(fields)
        if p_fields:
            function_name += "WithFieldsLimited"
            parms.append(p_fields)
        parms.append(limit)
        test_runs = []
        results = getattr(cls.session.test_management_client.service,
                          function_name)(*parms)
        for suds_obj in results:
            tr = TestRun(suds_object=suds_obj)
            test_runs.append(tr)
        return test_runs

    def __init__(self, test_run_id=None, suds_object=None, project_id=None,
                 uri=None):
        """TestRun constructor.

        Args:
            test_run_id: when given, the object is populated with the
                         TestRuns. Requires project_id parameter
            suds_object: Polarion TestRun object. When given, the object
                         is populated by object data.
            project_id: the Polarion project that the Test Run is located
                        in. Required if test_run_id is passed in
            uri: the uri that references the Polarion TestRun

        Notes:
            Either test_run_id and project or suds_object or uri can be passed
            in or none of them. If none of the identifying parameters are
            passed in an empty object is created

        References:
            test_management.getTestRunById
            test_management.getTestRunByUri
        """
        self._add_custom_fields(project_id)
        super(self.__class__, self).__init__(test_run_id, suds_object)
        if test_run_id:
            if not project_id:
                raise PyleroLibException("When test_run_id is passed in, "
                                         "project_id is required")
            self._suds_object = self.session.test_management_client.service. \
                getTestRunById(project_id, test_run_id)
        elif uri:
            self._suds_object = self.session.test_management_client.service. \
                getTestRunByUri(uri)
        if test_run_id or uri:
            if getattr(self._suds_object, "_unresolvable", True):
                raise PyleroLibException(
                    "The Test Run {0} was not found.".format(test_run_id))

    def _fix_circular_refs(self):
        # a class can't reference itself as a class attribute so it is
        # defined after instatiation
        self._cls_suds_map["template"]["cls"] = self.__class__

    def _custom_field_types(self, field_type):
        """There are 4 types of custom fields in test runs:
        * built-in types (string, boolean, ...)
        * Pylero Text object (text)
        * Enum of existing type (@ prefix, i.e. enum:@user = Pylero User)
        * Enum, based on lookup table(i.e. enum:arch)
        The basic enums can get their valid values using the BasePolarion
        get_valid_field_values function.
        The existing type Enums, must validate by instantiating the object.

        Args;
            field_type - the field type passed in custom field enum_id
        Returns:
            None for base types, Text class for text types, the object to
            validate the enum for Enum objects or the key to validate the enum
            for basic enums
        """
        if field_type == "text":
            return Text
        # some custom types have a [] segment. Still unsure of how to handle
        # those specific attributes, but for now, this will ignore them
        field_type = field_type.split("[")[0]
        if field_type.startswith("@"):
            # an enum based on an object
            return [globals()[x] for x in globals()
                    if x.lower() == field_type[1:].lower()][0]
        else:
            # a regular enum
            return field_type

    @classmethod
    def get_defined_custom_field_types(cls, project_id):
        """Gets all the custom fields defined for the specified project.
        the custom fields are all either of type CustomFieldType or
        EnumCustomFieldType in the case where the field is an enumeration.
        These 2 classes are mostly interchangeable.

        Args:
            project_id: the project to get the custom fields from

        Returns:
            list of all the custom fields

        References:
            testmanagement.getDefinedTestRunCustomFieldTypes
        """
        if not cls._custom_field_cache[project_id]:
            cfts = cls.session.test_management_client.service. \
                getDefinedTestRunCustomFieldTypes(project_id)
        else:
            cfts = cls._custom_field_cache[project_id]
        results = [CustomFieldType(suds_object=item)
                   if isinstance(item,
                                 CustomFieldType()._suds_object.__class__)
                   else EnumCustomFieldType(suds_object=item)
                   for item in cfts]
        return results

    def _cache_custom_fields(self, project_id):
        """Polarion API provides the custom fields of a TestRun.
        Get all custom fields and save in the dict self._custom_field_cache

        Args:
            project_id
        Returns
            None
        """
        self._custom_field_cache[project_id] = {}
        results = self.get_defined_custom_field_types(project_id)
        for result in results:
            f = getattr(result, "enum_id", None)
            key = result.cft_id
            f_type = None
            if f:
                f_type = self._custom_field_types(f)
            self._custom_field_cache[project_id][key] = {}
            self._custom_field_cache[project_id][key]["type"] = f_type
            self._custom_field_cache[project_id][key]["required"] = getattr(
                    result, "required", False)
            self._custom_field_cache[project_id][key]["multi"] = getattr(
                    result, "multi", False)

    def _add_custom_fields(self, project_id):
        """ This generates object attributes, with validation, so that custom
        fields can be related to as regular attributes. It takes the custom
        fields from the cache and calls the cache function if the values are
        not already there.
        Args:
            project_id - Each project can have its own custom fields. This
                function takes the custom fields for the specific project and
                adds them to the _cls_suds_map so they will be built into
                object attributes.
        Returns:
            None
        """
        self._changed_fields = {}
        # force the session to initialize. This is needed here because the
        # system has not yet been initialized.
        self.session
        if not project_id:
            project_id = self.default_project
        if project_id not in self._custom_field_cache:
            self._cache_custom_fields(project_id)
        cache = self._custom_field_cache[project_id]
        self._required_fields = []
        for field in cache:
            if cache[field]["required"]:
                self._required_fields.append(field)
            self._cls_suds_map[field] = {}
            self._cls_suds_map[field]["field_name"] = field
            self._cls_suds_map[field]["is_custom"] = True
            if cache[field]["type"] == Text:
                self._cls_suds_map[field]["cls"] = Text
            elif cache[field]["type"]:
                if cache[field]["multi"]:
                    self._cls_suds_map[field]["cls"] = ArrayOfEnumOptionId
                    self._cls_suds_map[field]["is_array"] = True
                else:
                    self._cls_suds_map[field]["cls"] = EnumOptionId
                self._cls_suds_map[field]["enum_id"] = cache[field]["type"]
                if isinstance(cache[field]["type"], type) and "project_id" in \
                        cache[field]["type"].__init__.__code__.co_varnames[
                        :cache[field]["type"].__init__.__code__.co_argcount]:
                    self._cls_suds_map[field]["additional_parms"] = \
                        {"project_id": project_id}

    def _get_index_of_test_record(self, test_case_id):
        # specific functions request the index of the test record within the
        # test run. However, the user doesn't know what the index is.
        # Therefore the user passes in the test case id and this function
        # figures out the index.
        # However, this function does not work for update_test_record_by_object
        # as that function requires the actual index of the record and not the
        # index of only executed records.
        index = -1
        for test_record in self._records:
            if test_record.executed:
                index += 1
            if test_case_id in test_record._suds_object.testCaseURI:
                return index
        raise PyleroLibException("The Test Case is either not part of "
                                 "this TestRun or has not been executed")

    def _status_change(self):
        # load a new object to test if the status should be changed.
        # can't use existing object because it doesn't include the new test rec
        # if the status needs changing, change it in the new object, so it
        # doesn't update any user made changes in the existing object.
        check_tr = TestRun(uri=self.uri)
        results = [rec.result for rec in check_tr.records if rec.result]
        if not results:
            status = "notrun"
            check_tr.finished_on = None
        elif len(results) == len(check_tr.records):
            status = "finished"
            # Do not touch finished_on because it can not be reverted
            # DPP-171495 Web services: You cannot reset finishedOn in TestRun
            # check_tr.finished_on = datetime.datetime.now()
        else:
            status = "inprogress"
            check_tr.finished_on = None
        if status != check_tr.status:
            check_tr.status = status
            check_tr.update()

    def _verify_record_count(self, record_index):
        # verifies the number of records is not less then the index given.
        self._verify_obj()
        if record_index > (len(self.records) - 1):
            raise PyleroLibException("There are only {0} test records".
                                     format(len(self.records)))

    def _verify_test_step_count(self, record_index, test_step_index):
        # verifies the number of test steps is not less then the index given.
        self._verify_record_count(record_index)
        if test_step_index > \
                (len(self.records[record_index].test_step_results) - 1):
            raise PyleroLibException("There are only {0} test records".
                                     format(len(self.records)))

    def add_attachment_to_test_record(self, test_case_id, path, title):
        """method add_attachment_to_test_record, adds the given attachment to
        the specified test record

        Args:
            test_case_id (str): The id of the test case
            path: file path to upload
            title: u.User friendly name of the file

        Returns:
            None

        Notes:
            Raises an error if the test case given is not in the TestRun or has
            not been executed yet.

        References:
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
            path: file path to upload
            title: u.User friendly name of the file

        Returns:
            None

        Notes:
            Raises an error if the test run object is not populated

        References:
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
            test_case_id (str): The id of the test case to the step is in
            test_step_index (int): The 0 based index of the test step
            path: file path to upload
            title: u.User friendly name of the file

        Returns:
            none

        Notes:
            Raises an error if the record_index given is higher then the number
            of test records. or if the test_step_index is higher then the
            number of steps.

        References:
            test_management.addAttachmentToTestStep
        """
        record_index = self._get_index_of_test_record(test_case_id)
        self._verify_test_step_count(record_index, test_step_index)
        data = self._get_file_data(path)
        filename = os.path.basename(path)
        self.session.test_management_client.service.addAttachmentToTestStep(
            self.uri, record_index, test_step_index, filename, title, data)

    def _check_test_record_exists(self, test_case_id):
        """Searches the test run to see if the case is already a member of it
        and if so raises an exception. It should only receive one result set
        and if it returns more then that it raises a different exception.
        It searches the server for the test record in case, the record was
        added by another process.

        Notes:
            This is the best that can be done and there is no method of knowing
            if another process added the same record in between this check and
            the actual add.

        Args:
            test_case_id (str): the id of the test case to check

        Returns:
            None
        """
        check_tr = TestRun.search(
            'project.id:%s AND id:"%s" AND %s' %
            (self.project_id, self.test_run_id, test_case_id))
        if len(check_tr) not in [0, 1]:
            raise PyleroLibException(
                "The search function did not work as expected. Please report.")
        elif len(check_tr) == 1:
            raise PyleroLibException(
                "This test case is already part of the test run")
        else:
            return None

    @tx_wrapper
    def add_test_record_by_fields(self, test_case_id, test_result,
                                  test_comment, executed_by, executed,
                                  duration, defect_work_item_id=None):
        """method add_test_record_by_fields, adds a test record for the given
        test case based on the result fields passed in.
        When a test record is added, it changes the test run status to
        "inprogress" and when the last test record is run, it changes the
        status to done.

        Args:
            test_case_id (str): The id of the test case that was executed
            test_result (str): Must be one of the following values:
                                  passed
                                  failed
                                  blocked
            test_comment (str or Text object): may be None
            executed_by (str): user id
            executed (datetime):
            duration (float):
            defect_work_item_id (str): _WorkItem id of defect, default: None

        Returns:
            None

        References:
            test_management.addTestRecordToTestRun
        """
        self._verify_obj()
        self.check_valid_field_values(test_result, "result", {})
        if not executed or not test_result:
            raise PyleroLibException(
                "executed and test_result require values")
        testrec = TestRecord(self.project_id, test_case_id)
        testrec.result = test_result
        testrec.comment = test_comment
        testrec.executed_by = executed_by
        testrec.executed = executed
        testrec.duration = duration
        if defect_work_item_id:
            testrec.defect_case_id = defect_work_item_id
        self.add_test_record_by_object(testrec)

    @tx_wrapper
    def add_test_record_by_object(self, test_record):
        """method add_test_record_by_object, adds a test record for the given
        test case based on the TestRecord object passed in

        Args:
            test_record (TestRecord or Polarion TestRecord):

        Returns:
            None

        References:
            test_management.addTestRecordToTestRun
        """
        self._verify_obj()
        test_case_id = test_record.test_case_id
        self._check_test_record_exists(test_case_id)
        if isinstance(test_record, TestRecord):
            suds_object = test_record._suds_object
        elif isinstance(test_record, TestRecord()._suds_object.__class__):
            suds_object = test_record
        if test_record.result == "failed" and not test_record.defect_case_id:
            test_record.defect_case_id = \
                create_incident_report(self, test_record,
                                       TestCase(work_item_id=test_case_id))
        self.session.test_management_client.service.addTestRecordToTestRun(
            self.uri, suds_object)
        self._status_change()

    def create_summary_defect(self, defect_template_id=None):
        """method create_summary_defect, adds a new summary _WorkItem for the
        test case based on the _WorkItem template id passed in. If not template
        is passed in, it creates it based on the default template.

        Args:
            defect_template_id (str): the _WorkItem template id to base the
            new summary defect. can be null. default: None

        Returns:
            the created _WorkItem

        References:
            test_management.createSummaryDefect
        """

        self._verify_obj()
        defect_template_uri = None
        if defect_template_id:
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
            test_case_id: The test case to delete the attachment from
            filename: name of the file to delete

        Returns:
            None

        References:
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
            test_case_id: The test case to delete the attachment from
            filename: name of the file to delete

        Returns:
            None

        References:
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
            filename: filename to delete

        Returns:
            None

        References:
            test_management.deleteTestRunAttachment
        """
        self._verify_obj()
        self.session.test_management_client.service. \
            deleteTestRunAttachment(self.uri, filename)

    def get_attachment(self, filename):
        """Gets Test Run Attachment specified by attachment's
        file name. Method is applicable also on Test Run Template.

        Args:
            filename: filename to delete

        Returns:
            TestRunAttachment object

        References:
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

        References:
            test_management.getTestRunAttachments
        """
        self._verify_obj()
        lst_suds_attach = self.session.test_management_client.service. \
            getTestRunAttachments(self.uri)
        lst_attach = [TestRunAttachment(suds_object=suds_attach)
                      for suds_attach in lst_suds_attach]
        return lst_attach

    def get_custom_field(self, field_name):
        """gets custom field values.

        Args:
            field_name: name of the custom field

        Returns:
            value of the custom field.

        Note: Polarion WSDL currently does not publish the list of custom
              fields, so this function cannot do any verification if the field
              is valid.
        """
        self._verify_obj()
        cf = self._custom_fields
        match = [x for x in cf if x.key == field_name]
        if match:
            return match[0].value
        else:
            return Custom(field_name, None)

    def get_wiki_content(self):
        """method get_wiki_content returns the wiki content for the Test Run

        Args:
            None

        Returns:
            Text object containing the wiki content

        References:
            test_management.getWikiContentForTestRun
        """
        self._verify_obj()
        suds_wiki = self.session.test_management_client.service. \
            getWikiContentForTestRun(self.uri)
        return Text(suds_object=suds_wiki)

    def _set_custom_field(self, field_name, value):
        """sets custom field values.

        Args:
            field_name: name of the custom field

        Returns:
            value of the custom field.

        Note: Polarion WSDL currently does not publish the list of custom
              fields, so this function cannot do any verification if the field
              or value is valid.
        """
        self._verify_obj()
        cf = self._custom_fields
        cust = Custom()
        cust.key = field_name
        cust.value = value
        if cf:
            # check if the custom field already exists and if so, modify it.
            match = [x for x in cf if x.key == field_name]
            if match:
                match[0].value = value
            else:
                cf.append(cust)
        else:
            cf = [cust]
        self._custom_fields = cf

    def update(self):
        """method update updates the testRun object with the attribute values
        currently in the object.

        Args:
            None

        Returns
            None

        References:
            test_management.updateTestRun
        """
        self._verify_obj()
        self.verify_required()
        for field in self._changed_fields:
            self._set_custom_field(field, self._changed_fields[field])
        self._changed_fields = {}
        self.session.test_management_client.service.updateTestRun(
            self._suds_object)

    def update_attachment(self, path, original_filename, title):
        """method update_attachment updates the specified attachment to the
        current test run

        Args:
            path: file path to upload
            original_filename: The file that we want to overwrite with the new
                               file
            title: u.User friendly name of the file

        Returns:
            None

        Notes:
            Raises an error if the test run object is not populated.

        References:
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
            source (string): source of the summary defect, used to generate
                              the description content.
            total_failures (int): amount of total failures in the test run,
                                  used to generate the description content.
            total_errors (int): amount of total errors in the test run,
                                used to generate the description content.
            total_tests (int): amount of total tests in the test run,
                               used to generate the description content.
            defect_template_id: ID of the defect template Work Item to be
                                used, the configured template will be used if
                                None.

        Returns:
            the created or updated _WorkItem

        References:
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

    @tx_wrapper
    def update_test_record_by_fields(self, test_case_id,
                                     test_result,
                                     test_comment,
                                     executed_by,
                                     executed,
                                     duration,
                                     defect_work_item_id=None):
        """method update_test_record_by_fields updates a test record.

        Args:
            test_case_id: id of the test case to update.
            test_result: Must be one of the following values:
                                   passed
                                   failed
                                   blocked
            test_comment: (str or Text object) - may be None
            executed_by (str): user id
            executed: date when the test case has been executed
            duration: duration of the test case execution, any negative value
                      is treated as None.
            defect_work_item_id: _WorkItem id of defect, can be None
                                Default: None

        Returns:
            None

        Notes:
            Only a test case that has already been executed may be updated
            using this function. To execute a test record use the
            add_test_record_by_fields function

        References:
            test_management.updateTestRecord
        """
        self._verify_obj()
        testrec = TestRecord(self.project_id, test_case_id)
        testrec.result = test_result
        testrec.comment = test_comment
        testrec.executed_by = executed_by
        testrec.executed = executed
        testrec.duration = duration
        if defect_work_item_id:
            testrec.defect_case_id = defect_work_item_id
        self.update_test_record_by_object(test_case_id, testrec)

    @tx_wrapper
    def update_test_record_by_object(self, test_case_id, test_record):
        """method update_test_record_by_object, adds a test record for the
        given test case based on the TestRecord object passed in

        Args:
            test_case_id (str): the test case id that the record is related to.
            test_record (TestRecord or Polarion TestRecord)

        Returns:
            None

        References:
            test_management.updateTestRecordAtIndex
        """
        self._verify_obj()
        # this function cannot use the _get_index_of_test_record function
        # because this function (specifically and not documented) uses the
        # actual index of the test records and not the index of all
        # executed records.
        test_case_ids = [rec.test_case_id for rec in self._records]
        if test_case_id not in test_case_ids:
            self.add_test_record_by_object(test_record)
        else:
            if test_record.result == "failed" and \
                    not test_record.defect_case_id:
                test_record.defect_case_id = \
                    create_incident_report(self, test_record,
                                           TestCase(work_item_id=test_case_id))
            index = test_case_ids.index(test_case_id)
            if isinstance(test_record, TestRecord):
                suds_object = test_record._suds_object
            elif isinstance(test_record, TestRecord()._suds_object.__class__):
                suds_object = test_record
            self.session.test_management_client.service. \
                updateTestRecordAtIndex(self.uri, index, suds_object)
            self._status_change()

    def update_wiki_content(self, content):
        """method update_wiki_content updates the wiki for the current TestRun

        Args:
            Content (str or Text object)

        Returns:
            None

        References:
            test_management.updateWikiContentForTestRun
        """
        self._verify_obj()
        if content:
            if isinstance(content, basestring):
                obj_content = Text(content=content)
                suds_content = obj_content._suds_object
            elif isinstance(content, Text):
                suds_content = content._suds_object
            else:  # is a suds object
                suds_content = content
        else:
            suds_content = suds.null()
        self.session.test_management_client.service. \
            updateWikiContentForTestRun(self.uri, suds_content)

    def verify_required(self):
        """function that checks if all required fields are passed in

        Exceptions:
            PyleroLibException - if required params are not passed in
        """
        fields = ""
        for req in self._required_fields:
            if not getattr(self, req):
                fields += (", " if fields else "") + req
        if fields:
            raise PyleroLibException("These parameters are required: {0}".
                                     format(fields))

    def verify_params(self, **kwargs):
        """function that checks if all the kwargs are valid attributes.

        Args:
            **kwargs: keyword arguments. Test run attributes can be passed in
                      to be set upon creation. Required fields must be passed
                      in
        Exceptions:
            PyleroLibException - if params are unknown
        """
        params = ""
        for param in kwargs:
            if param not in self._cls_suds_map:
                params += (", " if params else "") + param

        if params:
            raise PyleroLibException("These parameters are unknown: {0}".
                                     format(params))
