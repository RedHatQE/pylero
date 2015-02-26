# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals
import suds
import os
from pylarion.exceptions import PylarionLibException
import pylarion.base_polarion as bp
import pylarion.approval as app
import pylarion.attachment as att
import pylarion.user as u
import pylarion.category as cat
import pylarion.comment as com
import pylarion.custom as custom
import pylarion.custom_field as cf
import pylarion.custom_field_type as cft
import pylarion.text as t
import pylarion.externally_linked_work_item as elwi
import pylarion.hyperlink as hyp
import pylarion.revision as rev
import pylarion.linked_work_item as lwi
import pylarion.subterra_uri as stu
import pylarion.planning_constraint as pc
import pylarion.enum_option_id as eoi
import pylarion.priority_option_id as poi
import pylarion.project as p
import pylarion.test_steps as steps
import pylarion.test_step as step
import pylarion.time_point as tp
import pylarion.work_record as wr
import pylarion.workflow_action as wfa


class WorkItem(bp.BasePolarion):
    """Object to handle the Polarion WSDL tns5:WorkItem class

    Attributes (for specific details, see Polarion):
        approvals (ArrayOfApproval)
        assignee (ArrayOfUser)
        attachments (ArrayOfAttachment)
        author (User)
        auto_suspect (boolean)
        categories (ArrayOfCategory)
        comments (ArrayOfComment)
        created (dateTime)
        custom_fields (ArrayOfCustom)
        description (Text)
        due_date (date)
        externally_linked_work_items (ArrayOfExternallyLinkedWorkItem)
        hyperlinks (ArrayOfHyperlink)
        initial_estimate (duration)
        linked_revisions (ArrayOfRevision)
        linked_revisions_derived (ArrayOfRevision)
        linked_work_items (ArrayOfLinkedWorkItem)
        linked_work_items_derived (ArrayOfLinkedWorkItem)
        location (Location)
        module_uri (SubterraURI)
        outline_number (string)
        planned_end (dateTime)
        planned_in (ArrayOfPlan)
        planned_start (dateTime)
        planning_constraints (ArrayOfPlanningConstraint)
        previous_status (eoi.EnumOptionId)
        priority (PriorityOptionId)
        project (Project)
        remaining_estimate (duration)
        resolution (eoi.EnumOptionId)
        resolved_on (dateTime)
        severity (eoi.EnumOptionId)
        status (eoi.EnumOptionId)
        time_point (TimePoint)
        time_spent (duration)
        title (string)
        type (eoi.EnumOptionId)
        updated (dateTime)
        work_item_id (string)
        work_records (ArrayOfWorkRecord)
"""
    _cls_suds_map = {"approvals": {"field_name": "approvals",
                                   "is_array": True,
                                   "cls": app.Approval,
                                   "arr_cls": app.ArrayOfApproval,
                                   "inner_field_name": "Approval"},
                     "assignee": {"field_name": "assignee",
                                  "is_array": True,
                                  "cls": u.User,
                                  "arr_cls": u.ArrayOfUser,
                                  "inner_field_name": "User"},
                     "attachments": {"field_name": "attachments",
                                     "is_array": True,
                                     "cls": att.Attachment,
                                     "arr_cls": att.ArrayOfAttachment,
                                     "inner_field_name": "Attachment"},
                     "author": {"field_name": "author", "cls": u.User},
                     "auto_suspect": "autoSuspect",
                     "categories": {"field_name": "categories",
                                    "is_array": True,
                                    "cls": cat.Category,
                                    "arr_cls": cat.ArrayOfCategory,
                                    "inner_field_name": "Category"},
                     "comments": {"field_name": "comments",
                                  "is_array": True,
                                  "cls": com.Comment,
                                  "arr_cls": com.ArrayOfComment,
                                  "inner_field_name": "Comment"},
                     "created": "created",
                     "custom_fields": {"field_name": "customFields",
                                       "is_array": True,
                                       "cls": custom.Custom,
                                       "arr_cls": custom.ArrayOfCustom,
                                       "inner_field_name": "Custom"},
                     "description": {"field_name": "description",
                                     "cls": t.Text},
                     "due_date": "dueDate",
                     "externally_linked_work_items":
                     {"field_name":
                      "externallyLinkedWorkItems",
                      "is_array": True,
                      "cls": elwi.ExternallyLinkedWorkItem,
                      "arr_cls": elwi.ArrayOfExternallyLinkedWorkItem,
                      "inner_field_name": "ExternallyLinkedWorkItem"},
                     "hyperlinks": {"field_name": "hyperlinks",
                                    "is_array": True,
                                    "cls": hyp.Hyperlink,
                                    "arr_cls": hyp.ArrayOfHyperlink,
                                    "inner_field_name": "Hyperlink"},
                     "initial_estimate": "initialEstimate",
                     "linked_revisions": {"field_name": "linkedRevisions",
                                          "is_array": True,
                                          "cls": rev.Revision,
                                          "arr_cls": rev.ArrayOfRevision,
                                          "inner_field_name": "Revision"},
                     "linked_revisions_derived": {"field_name":
                                                  "linkedRevisionsDerived",
                                                  "is_array": True,
                                                  "cls": rev.Revision,
                                                  "arr_cls":
                                                  rev.ArrayOfRevision,
                                                  "inner_field_name":
                                                  "Revision"},
                     "linked_work_items": {"field_name": "linkedWorkItems",
                                           "is_array": True,
                                           "cls": lwi.LinkedWorkItem,
                                           "arr_cls":
                                           lwi.ArrayOfLinkedWorkItem,
                                           "inner_field_name":
                                           "LinkedWorkItem"},
                     "linked_work_items_derived": {"field_name":
                                                   "linkedWorkItemsDerived",
                                                   "is_array": True,
                                                   "cls": lwi.LinkedWorkItem,
                                                   "arr_cls":
                                                   lwi.ArrayOfLinkedWorkItem,
                                                   "inner_field_name":
                                                   "LinkedWorkItem"},
                     "location": "location",
                     "module_uri": {"field_name": "moduleURI", "cls":
                                    stu.SubterraURI},
                     "outline_number": "outlineNumber",
                     "planned_end": "plannedEnd",
                     # planned_in completed in the _fix_circular_imports func
                     "planned_in": {"field_name": "plannedIn"},
                     "planned_start": "plannedStart",
                     "planning_constraints": {"field_name":
                                              "planningConstraints",
                                              "is_array": True,
                                              "cls": pc.PlanningConstraint,
                                              "arr_cls":
                                              pc.ArrayOfPlanningConstraint,
                                              "inner_field_name":
                                              "PlanningConstraint"},
                     "previous_status": {"field_name": "previousStatus",
                                         "cls": eoi.EnumOptionId},
                     "priority": {"field_name": "priority",
                                  "cls": poi.PriorityOptionId},
                     "project": {"field_name": "project", "cls": p.Project},
                     "remaining_estimate": "remainingEstimate",
                     "resolution": {"field_name": "resolution", "cls":
                                    eoi.EnumOptionId},
                     "resolved_on": "resolvedOn",
                     "severity": {"field_name": "severity", "cls":
                                  eoi.EnumOptionId},
                     "status": {"field_name": "status",
                                "cls": eoi.EnumOptionId},
                     "time_point": {"field_name": "timePoint", "cls":
                                    tp.TimePoint},
                     "time_spent": "timeSpent",
                     "title": "title",
                     "type": {"field_name": "type", "cls": eoi.EnumOptionId},
                     "updated": "updated",
                     "work_item_id": "id",
                     "work_records": {"field_name": "workRecords",
                                      "is_array": True,
                                      "cls": wr.WorkRecord,
                                      "arr_cls": wr.ArrayOfWorkRecord,
                                      "inner_field_name": "WorkRecord"},
                     "uri": "_uri",
                     "_unresolved": "_unresolved"}
    _id_field = "work_item_id"
    _obj_client = "builder_client"
    _obj_struct = "tns5:WorkItem"
    has_query = True

    @classmethod
    def create(cls, work_item_id, project_id, wi_type, title, desc):
        """Creates a new work item with the given content. The project and the
        type have to be set for the workitem for the creation to succeed. The
        uri MUST NOT be set otherwise the creation will fail. To create a work
        item in a specific location e.g. a LiveDoc set the location of the
        work item to the desired target location. To create a work item in a
        specific Module/Document set the Module/Document of the work item to
        the desired target Module/Document.

        Args:
            work_item_id (string) - id of new WorkItem
            project_id - id of project to create work item in
            wi_type - type of work item (functionaltestcase,...)
            title - title of WorkItem
            desc - description of WorkItem
        Returns:
            new wi.WorkItem
        Implements:
            Tracker.createWorkItem
        """
        wi = WorkItem()
        wi.work_item_id = work_item_id
        wi.project = p.Project(project_id)
        wi.type = wi_type
        wi.title = title
        wi.description = desc
        wi_uri = cls.session.tracker_client.service.createWorkItem(
            wi._suds_object)
        return WorkItem(uri=wi_uri)

    @classmethod
    def get_query_result_count(cls, query):
        """Counts number of workitems returned by given query.

        Args:
            query - the lucene query to be used.
        Returns
            int
        Implements:
            Tracker.getWorkItemsCount
        """
        return cls.session.tracker_client.service.getWorkItemsCount(query)

    @classmethod
    def query(cls, query, is_sql=False, fields=[], sort="work_item_id",
              limit=-1, baseline_revision=None, query_uris=False):
        """Searches for Work Items.
        Args:
            query - query, either Lucene or SQL
            is_sql (bool), determines if the query is SQL or Lucene
            fields - array of field names to fill in the returned
                     Modules/Documents (can be null). For nested structures in
                     the lists you can use following syntax to include only
                     subset of fields: myList.LIST.key
                     (e.g. linkedWorkItems.LIST.role).
                     For custom fields you can specify which fields you want to
                     be filled using following syntax:
                     customFields.CUSTOM_FIELD_ID (e.g. customFields.risk).
            sort - Lucene sort string (can be null)
            limit - how many results to return (-1 means everything)
            baseline_revision (str) if populated, query done in specified rev
            query_uris (bool) - returns a list of URI of the Modules found
        Returns:
            list of wi.WorkItem objects
        Implements:
            Tracker.queryWorkItemUris
            Tracker.queryWorkItemUrisBySQL
            Tracker.queryWorkItemUrisInBaseline
            Tracker.queryWorkItemUrisInBaselineBySQL
            Tracker.queryWorkItemUrisInBaselineLimited
            Tracker.queryWorkItemUrisLimited
            Tracker.queryWorkItems
            Tracker.queryWorkItemsBySQL
            Tracker.queryWorkItemsInBaseline
            Tracker.queryWorkItemsInBaselineBySQL
            Tracker.queryWorkItemsInBaselineLimited
            Tracker.queryWorkItemsLimited
        """
        if not query_uris:
            base_name = "queryWorkItems"
        else:
            base_name = "queryWorkItemUris"
        return bp.BasePolarion._query(
            base_name, query, is_sql, fields=fields, sort=sort, limit=limit,
            baseline_revision=baseline_revision, has_fields=not query_uris)

    def __init__(self, work_item_id=None, suds_object=None, project_id=None,
                 uri=None, fields=None, revision=None):
        """WorkItem constructor.

        Args:
            work_item_id - when given, the object is populated with the
                          wi.WorkItem's data . Requires project_id parameter
            suds_object - Polarion wi.WorkItem object. When given, the object
                          is populated by object data.
            project_id - the Polarion project that the wi.WorkItem is located
                         in.
                    Required if work_item_id is passed in
            uri - the uri that references the Polarion wi.WorkItem
            fields - the fields that are requested to be populated.
                    if this is null then it will return all fields.
            revision - if given, get the wi.WorkItem in the specified revision
                       Is only relevant if URI is given.
        Notes:
            Either test_run_id and project or suds_object or uri can be passed
            in or none of them. If none of the identifying parameters are
            passed in an empty object is created
        Implements:
            Tracker.getWorkItemById
            Tracker.getWorkItemByIdsWithFields
            Tracker.getWorkItemByUri
            Tracker.getWorkItemByUriInRevision
            Tracker.getWorkItemByUriInRevisionWithFields
            Tracker.getWorkItemByUriWithFields
        """
        super(self.__class__, self).__init__(work_item_id, suds_object)
        p_fields = self._convert_obj_fields_to_polarion(fields)
        if work_item_id:
            if not project_id:
                raise PylarionLibException("When work_item_id is passed in, "
                                           "project_id is required")
        if work_item_id or uri:
            function_name = "getWorkItemBy"
            parms = []
            if work_item_id:
                function_name += "Id" if not p_fields else "IdsWithFields"
                parms = [project_id, work_item_id] + \
                    ([p_fields] if p_fields else [])
            elif uri:
                function_name += "Uri" + ("InRevision" if revision else "") + \
                    ("WithFields" if p_fields else "")
                parms = [uri] + ([revision] if revision else []) + \
                    ([p_fields] if p_fields else [])
            self._suds_object = getattr(self.session.tracker_client.service,
                                        function_name)(*parms)
        if not suds_object:
            if not (hasattr(self._suds_object, "_unresolvable") or
                    self._suds_object._unresolvable):
                raise PylarionLibException(
                    "The wi.WorkItem {0} was not found.".format(work_item_id))

    def _fix_circular_refs(self):
        # This module imports plan and plan imports this module.
        # The module references itself as a class attribute, which is not
        # allowed, so the self reference is defined here.
        import pylarion.plan as plan
        self._cls_suds_map["planned_in"]["is_array"] = True
        self._cls_suds_map["planned_in"]["cls"] = plan.Plan
        self._cls_suds_map["planned_in"]["arr_cls"] = plan.ArrayOfPlan
        self._cls_suds_map["planned_in"]["inner_field_name"] = "Plan"

    def add_approvee(self, approvee_id):
        """method add_approvee adds an approvee to the current wi.WorkItem

        Args:
            approvee_id (str) - user_id of approvee to add
        Returns:
            None
        Implements:
            Tracker.addApprovee
        """
        self._verify_obj()
        self.session.tracker_client.service.addApprovee(self.uri, approvee_id)

    def add_assignee(self, assignee_id):
        """method add_assignee adds an assignee to the current wi.WorkItem

        Args:
            assignee_id (str) - user_id of assignee to add
        Returns:
            bool
        Implements:
            Tracker.addAssignee
        """
        self._verify_obj()
        return self.session.tracker_client.service.addAssignee(self.uri,
                                                               assignee_id)

    def add_category(self, category_id):
        """method add_category adds a category to the current wi.WorkItem

        Args:
            category_id (str) - id of the category to add
        Returns:
            bool
        Implements:
            Tracker.addCategoy
        """
        self._verify_obj()
        return self.session.tracker_client.service.addCategory(self.uri,
                                                               category_id)

    def add_external_linked_revision(self, repository_name, revision_id):
        """method add_external_linked_revision links a revision from external
        repository.

        Args:
            repository_name (str) - name of external repository
            revision_id (str) - the id of the revision to add
        Returns:
            bool
        Implements:
            Tracker.addExternalLinkedRevision
        """
        self._verify_obj()
        return self.session.tracker_client.service.addExternalLinkedRevision(
            self.uri, repository_name, revision_id)

    def add_hyperlink(self, url, role):
        """method add_hyperlink adds a hyperlink to a wi.WorkItem

        Args:
            url - the url of the hyperlink to add.
            role - the role of the hyperlink to add.
        Returns:
            bool
        Implements:
            Tracker.addHyperlink
        """
        self._verify_obj()
        return self.session.tracker_client.service.addHyperlink(self.uri, url,
                                                                role)

    def add_linked_item(self, linked_work_item_id, role,
                        revision=None, suspect=None):
        """method add_linked_item adds a linked wi.WorkItem to current wi.WorkItem

        Args:
            linked_work_item_id - the URI of the target work item the link
                                  points to.
            role (str) - the role of the hyperlink to add.
            revision (str) - optional, specific revision for linked item
                      (None means HEAD revision)
            suspect (bool)- true if the link should be marked with suspect flag
                      Only valid if revision is set.
        Returns:
            bool
        Implements:
            Tracker.addLinkedItem
            Tracker.addLinkedItemWithRev
        """
        self._verify_obj()
        wi_linked = WorkItem(work_item_id=linked_work_item_id,
                             project_id=self.project.project_id)
        function_name = "addLinkedItem"
        parms = [self.uri, wi_linked.uri, role]
        if revision:
            function_name += "WithRev"
            parms += [revision, suspect]
        return getattr(self.session.tracker_client.service,
                       function_name)(*parms)

    def add_linked_revision(self, revision):
        """method add_linked_revision links a revision to the current wi.WorkItem

        Args:
            revision - the revision to add.
        Returns:
            bool
        Implements:
            Tracker.addLinkedRevision
        """
        self._verify_obj()
        return self.session.tracker_client.service.addLinkedRevision(self.uri,
                                                                     revision)

    def create_attachment(self, path, title):
        """method create_attachment adds the given attachment to the current
        wi.WorkItem

        Args:
            path - file path to upload
            title - u.User friendly name of the file
        Notes:
            Raises an error if the wi.WorkItem object is not populated
        Implements
            Tracker.createAttachment
        """
        self._verify_obj()
        data = self._get_file_data(path)
        filename = os.path.basename(path)
        self.session.tracker_client.service. \
            createAttachment(self.uri, filename, title, data)

    def create_comment(self, content):
        """method create_comment adds a comment to the current wi.WorkItem

        Args:
            content (Text or str)
        Returns:
            None
        Implements:
            Tracker.createComment
        """
        self._verify_obj()
        if content:
            if isinstance(content, str):
                obj_content = t.Text(obj_id=content)
                suds_content = obj_content._suds_object
            elif isinstance(content, t.Text):
                suds_content = content._suds_object
            else:  # is a suds object
                suds_content = content
        else:
            suds_content = suds.null()

        self.session.tracker_client.service.createComment(self.uri,
                                                          suds_content)

    def create_work_record(self, user_id, date_worked, time_spent,
                           record_type=None, record_comment=None):
        """Creates a work record
        Args:
            user_id - the user for the work record.
            date_worked - the date of the work record.
            time_spent - the time spent for the work record.
            record_type - the type of the work record
            record-comment - work record comment
        Returns:
            None
        Implements
            Tracker.createWorkRecord
            Tracker.createWorkRecordWithTypeAndComment
        """
        self._verify_obj()
        user = u.User(user_id=user_id)
        function_name = "createWorkRecord"
        parms = [self.uri, user._suds_object, date_worked]
        if record_type or record_comment:
            if not record_type:
                record_type = suds.null()
            if not record_comment:
                record_comment = suds.null()
            function_name += "WithTypeAndComment"
            parms += [record_type, time_spent, record_comment]
        else:
            parms += [time_spent]
        getattr(self.session.tracker_client.service, function_name)(*parms)

    def delete_attachment(self, attachment_id):
        """method delete_attachment removes the specified attachment from the
        current wi.WorkItem

        Args:
            attachment_id (str) - the ID of the attachment to be removed.
        Returns;
            None
        Implements:
            Tracker.deleteAttachment
        """
        self._verify_obj()
        self.session.tracker_client.deleteAttachment(self.uri, attachment_id)

    def do_auto_suspect(self):
        """Triggers auto suspect.

        Args:
            None
        Returns:
            None
        Implements:
            Tracker.doAutoSuspect
        """
        self._verify_obj()
        self.session.tracker_client.doAutoSuspect(self.uri)

    def do_auto_assign(self):
        """Triggers auto assignment.

        Args:
            None
        Returns:
            None
        Implements:
            Tracker.doAutoAssign
        """
        self._verify_obj()
        self.session.tracker_client.doAutoAssign(self.uri)

    def edit_approval(self, approvee_id, status):
        """Changes the status of an approval.

        Args:
            approveeId - the user id of the approvee.
            status - the new status to set.
        Returns:
            None
        Implements:
            Tracker.editApproval
        """
        self._verify_obj()
        self.session.tracker_client.editApproval(self.uri, approvee_id, status)

    def get_allowed_approvers(self):
        """Gets all allowed approvers"

        Args:
            None
        Returns
            list of u.Users
        Implements:
            Tracker.getAllowedApprovers
        """
        users = []
        for suds_user in self.session.tracker_client.service. \
                getAllowedApprovers(self.uri):
            users.append(u.User(suds_object=suds_user))
        return users

    def get_allowed_assignees(self):
        """Gets all allowed assignees"

        Args:
            None
        Returns
            list of u.Users
        Implements:
            Tracker.getAllowedAssignees
        """
        users = []
        for suds_user in self.session.tracker_client.service. \
                getAllowedAssignees(self.uri):
            users.append(u.User(suds_object=suds_user))
        return users

    def get_available_actions(self):
        """Gets the actions that can be used on the workflow object in its
        current state. Conditions of the action are checked and those with
        failed condition(s) are not returned.

        Args:
            None
        Returns
            list of WorkFlowActions
        Implements:
            Tracker.getAvailableActions
        """
        self._verify_obj()
        actions = []
        for suds_action in self.session.tracker_client.service. \
                getAvailableActions(self.uri):
            actions.append(wfa.WorkflowAction(suds_object=suds_action))
        return actions

    def get_back_linked_work_items(self):
        """Gets the back linked work items, work items linking to the specified
        work item.

        Args:
            None
        Returns
            list of LinkedWorkItems
        Implements:
            Tracker.getbackLinkedWorkitems
        """
        self._verify_obj()
        linked_work_items = []
        for suds_lwi in self.session.tracker_client.service. \
                getbackLinkedWorkitems(self.uri):
            linked_work_items.append(lwi.LinkedWorkItem(suds_object=suds_lwi))
        return linked_work_items

    def get_custom_field(self, key):
        """method get_custom_field gets a custom field of a work item.

        Args:
            key - The key of the custom field
        Returns:
            CustomField object
        Implements:
            Tracker.getCustomField
        """
        self._verify_obj()
        suds_custom = self.session.tracker_client.service.getCustomField(
            self._uri, key)
        return cf.CustomField(suds_object=suds_custom)

    def get_custom_field_keys(self):
        """method get_custom_field_keys Gets the names of defined custom
        fields.

        Args:
            None
        Returns
            list of keys
        Implements:
            Tracker.getCustomFieldKeys
        """
        self._verify_obj()
        return self.session.tracker_client.service.getCustomFieldKeys(self.uri)

    def get_custom_field_type(self, key):
        """method get_custom_field_type gets custom field definition of a
        work item.

        Args:
            key - The key of the custom field
        Returns:
            CustomFieldType object
        Implements:
            Tracker.getCustomFieldType
        """
        self._verify_obj()
        suds_custom = self.session.tracker_client.service.getCustomFieldType(
            self._uri, key)
        return cft.CustomFieldType(suds_object=suds_custom)

    def get_custom_field_types(self):
        """method get_custom_field_types gets all custom field definitions for
        a specific workitem fields.

        Args:
            None
        Returns
            list of CustomFieldType
        Implements:
            Tracker.getCustomFieldTypes
        """
        self._verify_obj()
        custom_types = []
        for suds_custom in self.session.tracker_client.service. \
                getCustomFieldTypes(self.uri):
            custom_types.append(cft.CustomFieldType(suds_object=suds_custom))

    def get_enum_control_key_for_id(self, enum_id):
        """Gets the enumeration control key for the specified work item key.

        Args:
            enum_id - the id of the enumeration to get the control key for.
        Returns:
            Enumeration control key
        Implements:
            Tracker.getEnumControlKeyForId
        """
        return self.session.tracker_client.service.getEnumControlKeyForId(
            self.project_id, enum_id)

    def get_enum_control_key_for_key(self, key):
        """Gets the enumeration control key for the specified work item key.

        Args:
            key - the key of the field containing the enumeration to get the
            control key for

        Returns:
            Enumeration control key
        Implements:
            Tracker.getEnumControlKeyForId
        """
        return self.session.tracker_client.service.getEnumControlKeyForId(
            self.project_id, key)

    def get_initial_workflow_action(self, work_item_type=None):
        """Gets the initial workflow action for the specified object, returns
        null if there is no initial action for the corresponding workflow.

        Args:
            work_item_type - the type of the work item to get the
                             available actions from. can be null
        Returns:
            WorkFlowAction object
        Implements:
            Tracker.getInitialWorkflowAction
            Tracker.getInitialWorkflowActionForProjectAndType
        """
        self._verify_obj()
        function_name = "getInitialWorkflowAction"
        parm = [self.uri]
        if work_item_type:
            function_name += "ForProjectAndType"
            parm += [work_item_type]
        suds_action = getattr(self.session.tracker_client.service,
                              function_name)(*parm)
        return wfa.WorkflowAction(suds_object=suds_action)

    def get_test_steps(self):
        """method get_test_steps retrieves the test steps of the current
        WorkItem. If the wi.WorkItem is not populated, it returns an exception.
        Args:
            None
        Returns:
            a TestSteps object
        Implements:
            Tracker.getTestSteps
        """
        self._verify_obj()
        suds_ts = self.session.test_management_client.service. \
            getTestSteps(self.uri)
        return steps.TestSteps(suds_object=suds_ts)

    def get_unavailable_actions(self):
        """Gets the actions that can not be used on the work item in the
        current state because of unsatisfied condition(s). Conditions of the
        action are checked and those with failed condition(s) are returned.
        The reason of unavailability is returned by
        WorkflowAction.getUnavailabilityMessage().

        Args:
            None
        Returns:
            list of WorkflowAction objects
        Implements:
            Tracker.getUnavailableActions
        """
        self._verify_obj()
        actions = []
        for suds_action in self.session.tracker_client.service. \
                getUnavailableActions(self.uri):
            actions.append(wfa.WorkflowAction(suds_object=suds_action))
        return actions

    def perform_workflow_action(self, action_id):
        """Executes a workflow action. The actions that can be performed can be
        received by wi.WorkItem.getAvailableActions(java.lang.String).

        Args:
            actionId - the id of the action to execute.
        Retuns:
            None
        Implements:
            Tracker.performWorkflowAction
        """
        self._verify_obj()
        self.session.tracker_client.service.performWorkflowAction(self.uri,
                                                                  action_id)

    def remove_assignee(self, assignee_id):
        """removes an assignee from the wi.WorkItem.
        Args:
            assignee_id - user id of the assignee to remove
        Returns
            bool
        Implements:
            Tracker.removeAssignee
        """
        self._verify_obj()
        return self.session.tracker_client.service.removeAssignee(self.uri,
                                                                  assignee_id)

    def remove_category(self, category_id):
        """removes a category from the wi.WorkItem.
        Args:
            assignee_id - user id of the assignee to remove
        Returns
            bool
        Implements:
            Tracker.removeCategory
        """
        self._verify_obj()
        return self.session.tracker_client.service.removeCategory(self.uri,
                                                                  category_id)

    def remove_external_linked_revision(self, repository_name, revision_id):
        """Removes a revision from external repository.

        Args:
            repository_name - the ID of the external repository.
            revision_id - the ID of the revision to remove.
        Returns
            bool
        Implements:
            Tracker.removeExternalLinkedRevision
        """
        self._verify_obj()
        return self.session.tracker_client.service. \
            removeExternalLinkedRevision(self.uri, repository_name,
                                         revision_id)

    def remove_externally_linked_item(self, linked_external_workitem_id, role):
        """Removes an externally linked work item.

        Args:
            linked_external_workitem_id - the ID of the linked item to remove
            role - the role of the linked item to remove
        Returns
            bool
        Implements:
            Tracker.removeExternallyLinkedItem
        """
        self._verify_obj()
        external_wi = WorkItem(uri=linked_external_workitem_id)
        return self.session.tracker_client.service. \
            removeExternallyLinkedItem(self.uri, external_wi.uri, role)

    def remove_hyperlink(self, url):
        """Removes a hyperlink from the wi.WorkItem

        Args:
            url - the url of the hyperlink to remove
        Returns
            bool
        Implements:
            Tracker.removeHyperlink
        """
        self._verify_obj()
        return self.session.tracker_client.service. \
            removeHyperlink(self.uri, url)

    def remove_linked_item(self, linked_item_id, role):
        """Removes a linked work item.

        Args:
            linked_item_id - the ID of the linked item to remove
            role - the role of the linked item to remove
        Returns
            bool
        Implements:
            Tracker.removeLinkedItem
        """
        self._verify_obj()
        linked_wi = WorkItem(uri=linked_item_id)
        return self.session.tracker_client.service. \
            removeLinkedItem(self.uri, linked_wi.uri, role)

    def remove_linked_revision(self, revision_id):
        """Removes a revision

        Args:
            revision_id - The ID of the revision to remove
        Returns:
            bool
        Implements:
            Tracker.removeLinkedRevision
        """
        self._verify_obj()
        return self.session.tracker_client.service. \
            removeLinkedRevision(self.uri, revision_id)

    def remove_planning_constraint(self, constraint_date, constraint):
        """Removes a planning constraint

        Args:
            constraint_date  - the date of the planning constraint to remove.
            constraint - the type of constraint to remove.
        Returns:
            bool
        Implements:
            Tracker.removePlaningConstraint
        """
        self._verify_obj()
        return self.session.tracker_client.service. \
            removePlaningConstraint(self.uri, constraint_date, constraint)

    def reset_workflow(self):
        """resets the workflow for the current object. Performs initial action
        if exists and sets the initial status

        Args:
            None
        Returns:
            None
        Implements:
            Tracker.resetWorkflow
        """
        self._verify_obj()
        self.session.tracker_client.service.resetWorkflow(self.uri)

    def set_fields_null(self, fields):
        """sets the specified fields to Null.

        Args:
            fields - list of fields to set to null
        Returns:
            None
        Implements:
            Tracker.setFieldsNull
        """
        self._verify_obj()
        p_fields = self._convert_obj_fields_to_polarion(fields)
        self.session.tracker_client.service.setFieldsNull(self.uri, p_fields)

    def set_test_steps(self, test_steps=None):
        """method set_test-steps Adds Test Steps to the current Work Item (WI)
        (add operation). If WI already has Test Steps, they will be completely
        replaced (update operation). If the test_steps parameter is None, the
        content of the Test Steps field will be emptied (delete operation).

        Args:
            test_steps - a list of TestStep objects.
        Returns:
            None
         Implements:
            Test_Management.setTestSteps
        """
        self._verify_obj()
        if not test_steps:
            parm = suds.null()
        elif isinstance(test_steps, list):
            parm = []
            if isinstance(test_steps[0], step.TestStep):
                parm = [item._suds_object for item in test_steps]
            elif isinstance(test_steps[0], step.TestStep().
                            _suds_object.__class__):
                parm = test_steps
        else:
            raise PylarionLibException("Expecting a list of testStep objects")
        self.session.test_management_client.service.setTestSteps(self.uri,
                                                                 parm)

    def update(self):
        """Update the server with the current wi.WorkItem data
        Args:
            None
        Returns:
            None
        Implements:
            Tracker.updateWorkItem
        """
        self._verify_obj()
        self.session.tracker_client.service.updateWorkItem(self._suds_object)

    def update_attachment(self, attachment_id, path, title):
        """method update_attachment updates the specified attachment to the
        current wi.WorkItem

        Args:
            attachment_id - the ID of the attachment to be updated
            path - file path to upload
            title - u.User friendly name of the file
        Returns:
            None
        Notes:
            Raises an error if the test run object is not populated.
        Implements:
            Tracker.updateAttachment
        """
        self._verify_obj()
        data = self._get_file_data(path)
        filename = os.path.basename(path)
        self.session.tracker_client.service. \
            updateAttachment(self.uri, attachment_id, filename, title, data)
