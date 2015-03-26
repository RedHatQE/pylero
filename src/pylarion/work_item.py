# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals
import suds
import os
import re
import copy
from pylarion.exceptions import PylarionLibException
from pylarion.base_polarion import BasePolarion
from pylarion.approval import Approval
from pylarion.approval import ArrayOfApproval
from pylarion.attachment import Attachment
from pylarion.attachment import ArrayOfAttachment
from pylarion.user import User
from pylarion.user import ArrayOfUser
from pylarion.category import Category
from pylarion.category import ArrayOfCategory
from pylarion.comment import Comment
from pylarion.comment import ArrayOfComment
from pylarion.custom import Custom
from pylarion.custom import ArrayOfCustom
from pylarion.custom_field import CustomField
from pylarion.custom_field_type import CustomFieldType
from pylarion.enum_custom_field_type import EnumCustomFieldType
from pylarion.text import Text
from pylarion.externally_linked_work_item import ExternallyLinkedWorkItem
from pylarion.externally_linked_work_item \
    import ArrayOfExternallyLinkedWorkItem
from pylarion.hyperlink import Hyperlink
from pylarion.hyperlink import ArrayOfHyperlink
from pylarion.revision import Revision
from pylarion.revision import ArrayOfRevision
from pylarion.linked_work_item import LinkedWorkItem
from pylarion.linked_work_item import ArrayOfLinkedWorkItem
from pylarion.subterra_uri import SubterraURI
from pylarion.planning_constraint import PlanningConstraint
from pylarion.planning_constraint import ArrayOfPlanningConstraint
from pylarion.enum_option_id import EnumOptionId
# ArrayOfEnumOptionId is used in dynamic code for custom fields
from pylarion.enum_option_id import ArrayOfEnumOptionId
from pylarion.priority_option_id import PriorityOptionId
from pylarion.project import Project
from pylarion.test_steps import TestSteps
from pylarion.test_step import TestStep
from pylarion.time_point import TimePoint
from pylarion.work_record import WorkRecord
from pylarion.work_record import ArrayOfWorkRecord
from pylarion.workflow_action import WorkflowAction


class _WorkItem(BasePolarion):
    """Object to handle the Polarion WSDL tns5:WorkItem class

    Attributes:
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
        previous_status (EnumOptionId)
        priority (PriorityOptionId)
        project_id (Project)
        remaining_estimate (duration)
        resolution (EnumOptionId)
        resolved_on (dateTime)
        severity (EnumOptionId)
        status (EnumOptionId)
        time_point (TimePoint)
        time_spent (duration)
        title (string)
        type (EnumOptionId)
        updated (dateTime)
        work_item_id (string)
        work_records (ArrayOfWorkRecord)
"""
    _cls_suds_map = {
        "approvals":
            {"field_name": "approvals",
             "is_array": True,
             "cls": Approval,
             "arr_cls": ArrayOfApproval,
             "inner_field_name": "Approval"},
        "assignee":
            {"field_name": "assignee",
             "is_array": True,
             "cls": User,
             "arr_cls": ArrayOfUser,
             "inner_field_name": "User"},
        "attachments":
            {"field_name": "attachments",
             "is_array": True,
             "cls": Attachment,
             "arr_cls": ArrayOfAttachment,
             "inner_field_name": "Attachment"},
        "author":
            {"field_name": "author",
             "cls": User},
        "auto_suspect": "autoSuspect",
        "categories":
            {"field_name": "categories",
             "is_array": True,
             "cls": Category,
             "arr_cls": ArrayOfCategory,
             "inner_field_name": "Category"},
        "comments":
            {"field_name": "comments",
             "is_array": True,
             "cls": Comment,
             "arr_cls": ArrayOfComment,
             "inner_field_name": "Comment"},
        "created": "created",
        "custom_fields":
            {"field_name": "customFields",
             "is_array": True,
             "cls": Custom,
             "arr_cls": ArrayOfCustom,
             "inner_field_name": "Custom"},
        "description":
            {"field_name": "description",
             "cls": Text},
        "due_date": "dueDate",
        "externally_linked_work_items":
            {"field_name": "externallyLinkedWorkItems",
             "is_array": True,
             "cls": ExternallyLinkedWorkItem,
             "arr_cls": ArrayOfExternallyLinkedWorkItem,
             "inner_field_name": "ExternallyLinkedWorkItem"},
        "hyperlinks":
            {"field_name": "hyperlinks",
             "is_array": True,
             "cls": Hyperlink,
             "arr_cls": ArrayOfHyperlink,
             "inner_field_name": "Hyperlink"},
        "initial_estimate": "initialEstimate",
        "linked_revisions":
            {"field_name": "linkedRevisions",
             "is_array": True,
             "cls": Revision,
             "arr_cls": ArrayOfRevision,
             "inner_field_name": "Revision"},
        "linked_revisions_derived":
            {"field_name": "linkedRevisionsDerived",
             "is_array": True,
             "cls": Revision,
             "arr_cls": ArrayOfRevision,
             "inner_field_name": "Revision"},
        "linked_work_items":
            {"field_name": "linkedWorkItems",
             "is_array": True,
             "cls": LinkedWorkItem,
             "arr_cls": ArrayOfLinkedWorkItem,
             "inner_field_name": "LinkedWorkItem"},
        "linked_work_items_derived":
            {"field_name": "linkedWorkItemsDerived",
             "is_array": True,
             "cls": LinkedWorkItem,
             "arr_cls": ArrayOfLinkedWorkItem,
             "inner_field_name": "LinkedWorkItem"},
        "location": "location",
        "module_uri":
            {"field_name": "moduleURI",
             "cls": SubterraURI},
        "outline_number": "outlineNumber",
        "planned_end": "plannedEnd",
        # planned_in completed in the _fix_circular_imports func
        "planned_in":
            {"field_name": "plannedIn"},
        "planned_start": "plannedStart",
        "planning_constraints":
            {"field_name": "planningConstraints",
             "is_array": True,
             "cls": PlanningConstraint,
             "arr_cls": ArrayOfPlanningConstraint,
             "inner_field_name": "PlanningConstraint"},
        "previous_status":
            {"field_name": "previousStatus",
             "cls": EnumOptionId,
             "enum_id": "status"},
        "priority":
            {"field_name": "priority",
             "cls": PriorityOptionId,
             "enum_id": "priority"},
        "project_id":
            {"field_name": "project",
             "cls": Project},
        "remaining_estimate": "remainingEstimate",
        "resolution":
            {"field_name": "resolution",
             "cls": EnumOptionId,
             "enum_id": "resolution"},
        "resolved_on": "resolvedOn",
        "severity":
            {"field_name": "severity",
             "cls": EnumOptionId,
             "enum_id": "severity"},
        "status":
            {"field_name": "status",
             "cls": EnumOptionId,
             "enum_id": "status"},
        "time_point":
            {"field_name": "timePoint",
             "cls": TimePoint},
        "time_spent": "timeSpent",
        "title": "title",
        "type":
            {"field_name": "type",
             "cls": EnumOptionId,
             "enum_id": "workitem-type",
             "enum_override": ["heading"]},
        "updated": "updated",
        "work_item_id": "id",
        "work_records":
            {"field_name": "workRecords",
             "is_array": True,
             "cls": WorkRecord,
             "arr_cls": ArrayOfWorkRecord,
             "inner_field_name": "WorkRecord"},
        "uri": "_uri",
        "_unresolved": "_unresolved"}
    _id_field = "work_item_id"
    _obj_client = "tracker_client"
    _obj_struct = "tns3:WorkItem"
    has_query = True

    @classmethod
    def create(cls, project_id, wi_type, title, desc, status, **kwargs):
        """Creates a new work item with the given content. The project and the
        type have to be set for the workitem for the creation to succeed. The
        uri MUST NOT be set otherwise the creation will fail. To create a work
        item in a specific location e.g. a LiveDoc set the location of the
        work item to the desired target location. To create a work item in a
        specific Module/Document set the Module/Document of the work item to
        the desired target Module/Document.

        Args:
            project_id: id of project to create work item in
            wi_type: type of work item (functionaltestcase,...)
            title: title of WorkItem
            desc: description of WorkItem
            status: initial status of the WorkItem, draft by default

        Returns:
            new _WorkItem

        References:
            Tracker.createWorkItem
        """
        wi = cls()
        wi.project_id = project_id
        wi.type = wi_type
        wi.title = title
        wi.description = desc
        wi.status = status
        wi_uri = cls.session.tracker_client.service.createWorkItem(
            wi._suds_object)
        new_wi = _WorkItem(uri=wi_uri)
        for field in kwargs:
            setattr(new_wi, field, kwargs[field])
        new_wi.update()
        return new_wi

    @classmethod
    def get_query_result_count(cls, query):
        """Counts number of workitems returned by given query.

        Args:
            query: the lucene query to be used.

        Returns
            int

        References:
            Tracker.getWorkItemsCount
        """
        return cls.session.tracker_client.service.getWorkItemsCount(query)

    @classmethod
    def get_defined_custom_field_types(cls, project_id, wi_type):
        """Gets all the custom fields defined for the specified wi_type.
        the custom fields are all either of type CustomFieldType or
        EnumCustomFieldType in the case where the field is an enumeration.
        These 2 classes are mostly interchangeable.

        Args:
            project_id: the project to get the custom fields from
            wi_type: The type of work item to get the custom fields for

        Returns:
            list of all the custom fields

        References:
            tracker.getDefinedCustomFieldTypes
        """
        if not cls._cache["custom_field_types"]:
            cfts = cls.session.tracker_client.service. \
                getDefinedCustomFieldTypes(project_id, wi_type)
            cls._cache["custom_field_types"] = cfts
        else:
            cfts = cls._cache.get("custom_field_types")
        results = [CustomFieldType(suds_object=item)
                   if isinstance(item,
                                 CustomFieldType()._suds_object.__class__)
                   else EnumCustomFieldType(suds_object=item)
                   for item in cfts]
        return results

    @classmethod
    def query(cls, query, is_sql=False, fields=[], sort="work_item_id",
              limit=-1, baseline_revision=None, query_uris=False):
        """Searches for Work Items.

        Args:
            query: query, either Lucene or SQL
            is_sql (bool): determines if the query is SQL or Lucene
            fields: array of field names to fill in the returned
                    Modules/Documents (can be null). For nested structures in
                    the lists you can use following syntax to include only
                    subset of fields: myList.LIST.key
                    (e.g. linkedWorkItems.LIST.role).
                    For custom fields you can specify which fields you want to
                    be filled using following syntax:
                    customFields.CUSTOM_FIELD_ID (e.g. customFields.risk).
            sort: Lucene sort string (can be null)
            limit: how many results to return (-1 means everything)
            baseline_revision (str): if populated, query done in specified rev
            query_uris (bool): returns a list of URI of the Modules found

        Returns:
            list of _WorkItem objects

        References:
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
        return BasePolarion._query(
            base_name, query, is_sql, fields=fields, sort=sort, limit=limit,
            baseline_revision=baseline_revision, has_fields=not query_uris)

    def __init__(self, project_id=None, work_item_id=None, suds_object=None,
                 uri=None, fields=None, revision=None):
        """WorkItem constructor.

        Args:
            project_id: the Polarion project that the _WorkItem is located
                        in.
            work_item_id: when given, the object is populated with the
                         _WorkItem's data . Requires project_id parameter
            suds_object: Polarion _WorkItem object. When given, the object
                         is populated by object data.
            uri: the uri that references the Polarion _WorkItem
            fields: the fields that are requested to be populated.
                    if this is null then it will return all fields.
            revision: if given, get the _WorkItem in the specified revision
                       Is only relevant if URI is given.

        Notes:
            Either test_run_id and project or suds_object or uri can be passed
            in or none of them. If none of the identifying parameters are
            passed in an empty object is created

        References:
            Tracker.getWorkItemById
            Tracker.getWorkItemByIdsWithFields
            Tracker.getWorkItemByUri
            Tracker.getWorkItemByUriInRevision
            Tracker.getWorkItemByUriInRevisionWithFields
            Tracker.getWorkItemByUriWithFields
        """

        self._required_fields = getattr(self, "_required_fields", [])
        self._changed_fields = getattr(self, "_changed_fields", {})
        # because other classes inherit from this. If super uses self.__class__
        # it will be a infinite loop for the derived class.
        super(_WorkItem, self).__init__(work_item_id, suds_object)
        p_fields = self._convert_obj_fields_to_polarion(fields)
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
            if getattr(self._suds_object, "_unresolvable", True):
                raise PylarionLibException(
                    "The WorkItem {0} was not found.".format(work_item_id))
        if not self.project_id:
            self.project_id = self.default_project

    def _fix_circular_refs(self):
        # This module imports plan and plan imports this module.
        # The module references itself as a class attribute, which is not
        # allowed, so the self reference is defined here.
        from pylarion.plan import Plan
        from pylarion.plan import ArrayOfPlan
        self._cls_suds_map["planned_in"]["is_array"] = True
        self._cls_suds_map["planned_in"]["cls"] = Plan
        self._cls_suds_map["planned_in"]["arr_cls"] = ArrayOfPlan
        self._cls_suds_map["planned_in"]["inner_field_name"] = "Plan"

    def add_approvee(self, approvee_id):
        """method add_approvee adds an approvee to the current _WorkItem

        Args:
            approvee_id (str):er_id of approvee to add

        Returns:
            None

        References:
            Tracker.addApprovee
        """
        self._verify_obj()
        self.session.tracker_client.service.addApprovee(self.uri, approvee_id)

    def add_assignee(self, assignee_id):
        """method add_assignee adds an assignee to the current _WorkItem

        Args:
            assignee_id (str): user_id of assignee to add

        Returns:
            bool

        References:
            Tracker.addAssignee
        """
        self._verify_obj()
        return self.session.tracker_client.service.addAssignee(self.uri,
                                                               assignee_id)

    def add_category(self, category_id):
        """method add_category adds a category to the current _WorkItem

        Args:
            category_id (str): id of the category to add

        Returns:
            bool

        References:
            Tracker.addCategoy
        """
        self._verify_obj()
        return self.session.tracker_client.service.addCategory(self.uri,
                                                               category_id)

    def add_external_linked_revision(self, repository_name, revision_id):
        """method add_external_linked_revision links a revision from external
        repository.

        Args:
            repository_name (str): name of external repository
            revision_id (str): the id of the revision to add

        Returns:
            bool

        References:
            Tracker.addExternalLinkedRevision
        """
        self._verify_obj()
        return self.session.tracker_client.service.addExternalLinkedRevision(
            self.uri, repository_name, revision_id)

    def add_hyperlink(self, url, role):
        """method add_hyperlink adds a hyperlink to a _WorkItem

        Args:
            url: the url of the hyperlink to add.
            role: the role of the hyperlink to add.

        Returns:
            bool

        References:
            Tracker.addHyperlink
        """
        self._verify_obj()
        return self.session.tracker_client.service.addHyperlink(self.uri, url,
                                                                role)

    def add_linked_item(self, linked_work_item_id, role,
                        revision=None, suspect=None):
        """method add_linked_item adds a linked _WorkItem to current _WorkItem

        Args:
            linked_work_item_id - the URI of the target work item the link
                                  points to.
            role (str): the role of the hyperlink to add.
            revision (str): optional, specific revision for linked item
                           (None means HEAD revision)
            suspect (bool): true if the link should be marked with suspect flag
                      Only valid if revision is set.

        Returns:
            bool

        References:
            Tracker.addLinkedItem
            Tracker.addLinkedItemWithRev
        """
        self._verify_obj()
        wi_linked = _WorkItem(work_item_id=linked_work_item_id,
                              project_id=self.project_id)
        function_name = "addLinkedItem"
        parms = [self.uri, wi_linked.uri, role]
        if revision:
            function_name += "WithRev"
            parms += [revision, suspect]
        return getattr(self.session.tracker_client.service,
                       function_name)(*parms)

    def add_linked_revision(self, revision):
        """method add_linked_revision links a revision to the current _WorkItem

        Args:
            revision: the revision to add.

        Returns:
            bool

        References:
            Tracker.addLinkedRevision
        """
        self._verify_obj()
        return self.session.tracker_client.service.addLinkedRevision(self.uri,
                                                                     revision)

    def create_attachment(self, path, title):
        """method create_attachment adds the given attachment to the current
        _WorkItem

        Args:
            path: file path to upload
            title: u.User friendly name of the file

        Notes:
            Raises an error if the _WorkItem object is not populated

        Implements
            Tracker.createAttachment
        """
        self._verify_obj()
        data = self._get_file_data(path)
        filename = os.path.basename(path)
        self.session.tracker_client.service. \
            createAttachment(self.uri, filename, title, data)

    def create_comment(self, content):
        """method create_comment adds a comment to the current _WorkItem

        Args:
            content (Text or str)

        Returns:
            None

        References:
            Tracker.createComment
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

        self.session.tracker_client.service.createComment(self.uri,
                                                          suds_content)

    def create_work_record(self, user_id, date_worked, time_spent,
                           record_type=None, record_comment=None):
        """Creates a work record

        Args:
            user_id: the user for the work record.
            date_worked: the date of the work record.
            time_spent: the time spent for the work record.
            record_type: the type of the work record
            record-comment: work record comment

        Returns:
            None

        Implements
            Tracker.createWorkRecord
            Tracker.createWorkRecordWithTypeAndComment
        """
        self._verify_obj()
        user = User(user_id=user_id)
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
        current _WorkItem

        Args:
            attachment_id (str): the ID of the attachment to be removed.

        Returns:
            None

        References:
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

        References:
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

        References:
            Tracker.doAutoAssign
        """
        self._verify_obj()
        self.session.tracker_client.doAutoAssign(self.uri)

    def edit_approval(self, approvee_id, status):
        """Changes the status of an approval.

        Args:
            approveeId: the user id of the approvee.
            status: the new status to set.

        Returns:
            None

        References:
            Tracker.editApproval
        """
        self._verify_obj()
        self.session.tracker_client.editApproval(self.uri, approvee_id, status)

    def get_allowed_approvers(self):
        """Gets all allowed approvers"

        Args:
            None

        Returns:
            list of u.Users

        References:
            Tracker.getAllowedApprovers
        """
        users = []
        for suds_user in self.session.tracker_client.service. \
                getAllowedApprovers(self.uri):
            users.append(User(suds_object=suds_user))
        return users

    def get_allowed_assignees(self):
        """Gets all allowed assignees"

        Args:
            None

        Returns:
            list of u.Users

        References:
            Tracker.getAllowedAssignees
        """
        users = []
        for suds_user in self.session.tracker_client.service. \
                getAllowedAssignees(self.uri):
            users.append(User(suds_object=suds_user))
        return users

    def get_available_actions(self):
        """Gets the actions that can be used on the workflow object in its
        current state. Conditions of the action are checked and those with
        failed condition(s) are not returned.

        Args:
            None

        Returns:
            list of WorkFlowActions

        References:
            Tracker.getAvailableActions
        """
        self._verify_obj()
        actions = []
        for suds_action in self.session.tracker_client.service. \
                getAvailableActions(self.uri):
            actions.append(WorkflowAction(suds_object=suds_action))
        return actions

    def get_back_linked_work_items(self):
        """Gets the back linked work items, work items linking to the specified
        work item.

        Args:
            None

        Returns:
            list of LinkedWorkItems

        References:
            Tracker.getbackLinkedWorkitems
        """
        self._verify_obj()
        linked_work_items = []
        for suds_lwi in self.session.tracker_client.service. \
                getbackLinkedWorkitems(self.uri):
            linked_work_items.append(LinkedWorkItem(suds_object=suds_lwi))
        return linked_work_items

    def get_custom_field(self, key):
        """method get_custom_field gets a custom field of a work item.

        Args:
            key: The key of the custom field

        Returns:
            CustomField object

        References:
            Tracker.getCustomField
        """
        self._verify_obj()
        suds_custom = self.session.tracker_client.service.getCustomField(
            self.uri, key)
        return CustomField(suds_object=suds_custom)

    def get_custom_field_keys(self):
        """method get_custom_field_keys Gets the names of defined custom
        fields.

        Args:
            None

        Returns:
            list of keys

        References:
            Tracker.getCustomFieldKeys
        """
        self._verify_obj()
        return self.session.tracker_client.service.getCustomFieldKeys(self.uri)

    def get_custom_field_type(self, key):
        """method get_custom_field_type gets custom field definition of a
        work item.

        Args:
            key: The key of the custom field

        Returns:
            CustomFieldType object

        References:
            Tracker.getCustomFieldType
        """
        self._verify_obj()
        suds_custom = self.session.tracker_client.service.getCustomFieldType(
            self.uri, key)
        return CustomFieldType(suds_object=suds_custom)

    def get_custom_field_types(self):
        """method get_custom_field_types gets all custom field definitions for
        a specific workitem fields.

        Args:
            None

        Returns:
            list of CustomFieldType

        References:
            Tracker.getCustomFieldTypes
        """
        self._verify_obj()
        custom_types = []
        for suds_custom in self.session.tracker_client.service. \
                getCustomFieldTypes(self.uri):
            custom_types.append(CustomFieldType(suds_object=suds_custom))

    def get_enum_control_key_for_id(self, enum_id):
        """Gets the enumeration control key for the specified work item key.

        Args:
            enum_id: the id of the enumeration to get the control key for.

        Returns:
            Enumeration control key

        References:
            Tracker.getEnumControlKeyForId
        """
        return self.session.tracker_client.service.getEnumControlKeyForId(
            self.project_id, enum_id)

    def get_enum_control_key_for_key(self, key):
        """Gets the enumeration control key for the specified work item key.

        Args:
            key: the key of the field containing the enumeration to get the
                 control key for

        Returns:
            Enumeration control key

        References:
            Tracker.getEnumControlKeyForId
        """
        return self.session.tracker_client.service.getEnumControlKeyForId(
            self.project_id, key)

    def get_initial_workflow_action(self, work_item_type=None):
        """Gets the initial workflow action for the specified object, returns
        null if there is no initial action for the corresponding workflow.

        Args:
            work_item_type: the type of the work item to get the
                             available actions from. can be null
        Returns:
            WorkFlowAction object

        References:
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
        return WorkflowAction(suds_object=suds_action)

    def get_test_steps(self):
        """method get_test_steps retrieves the test steps of the current
        WorkItem. If the _WorkItem is not populated, it returns an exception.
        Args:
            None

        Returns:
            a TestSteps object

        References:
            Tracker.getTestSteps
        """
        self._verify_obj()
        suds_ts = self.session.test_management_client.service. \
            getTestSteps(self.uri)
        return TestSteps(suds_object=suds_ts)

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

        References:
            Tracker.getUnavailableActions
        """
        self._verify_obj()
        actions = []
        for suds_action in self.session.tracker_client.service. \
                getUnavailableActions(self.uri):
            actions.append(WorkflowAction(suds_object=suds_action))
        return actions

    def perform_workflow_action(self, action_id):
        """Executes a workflow action. The actions that can be performed can be
        received by _WorkItem.getAvailableActions(java.lang.String).

        Args:
            action_id: the id of the action to execute.

        Retuns:
            None

        References:
            Tracker.performWorkflowAction
        """
        self._verify_obj()
        self.session.tracker_client.service.performWorkflowAction(self.uri,
                                                                  action_id)

    def remove_assignee(self, assignee_id):
        """removes an assignee from the _WorkItem.

        Args:
            assignee_id: user id of the assignee to remove

        Returns:
            bool

        References:
            Tracker.removeAssignee
        """
        self._verify_obj()
        return self.session.tracker_client.service.removeAssignee(self.uri,
                                                                  assignee_id)

    def remove_category(self, category_id):
        """removes a category from the _WorkItem.

        Args:
            category_id: id of category to remove

        Returns:
            bool

        References:
            Tracker.removeCategory
        """
        self._verify_obj()
        return self.session.tracker_client.service.removeCategory(self.uri,
                                                                  category_id)

    def remove_external_linked_revision(self, repository_name, revision_id):
        """Removes a revision from external repository.

        Args:
            repository_name: the ID of the external repository.
            revision_id: the ID of the revision to remove.

        Returns:
            bool

        References:
            Tracker.removeExternalLinkedRevision
        """
        self._verify_obj()
        return self.session.tracker_client.service. \
            removeExternalLinkedRevision(self.uri, repository_name,
                                         revision_id)

    def remove_externally_linked_item(self, linked_external_workitem_id, role):
        """Removes an externally linked work item.

        Args:
            linked_external_workitem_id: the ID of the linked item to remove
            role: the role of the linked item to remove

        Returns:
            bool

        References:
            Tracker.removeExternallyLinkedItem
        """
        self._verify_obj()
        external_wi = _WorkItem(uri=linked_external_workitem_id)
        return self.session.tracker_client.service. \
            removeExternallyLinkedItem(self.uri, external_wi.uri, role)

    def remove_hyperlink(self, url):
        """Removes a hyperlink from the _WorkItem

        Args:
            url: the url of the hyperlink to remove

        Returns:
            bool

        References:
            Tracker.removeHyperlink
        """
        self._verify_obj()
        return self.session.tracker_client.service. \
            removeHyperlink(self.uri, url)

    def remove_linked_item(self, linked_item_id, role):
        """Removes a linked work item.

        Args:
            linked_item_id: the ID of the linked item to remove
            role: the role of the linked item to remove

        Returns:
            bool

        References:
            Tracker.removeLinkedItem
        """
        self._verify_obj()
        linked_wi = _WorkItem(uri=linked_item_id)
        return self.session.tracker_client.service. \
            removeLinkedItem(self.uri, linked_wi.uri, role)

    def remove_linked_revision(self, revision_id):
        """Removes a revision

        Args:
            revision_id: The ID of the revision to remove

        Returns:
            bool

        References:
            Tracker.removeLinkedRevision
        """
        self._verify_obj()
        return self.session.tracker_client.service. \
            removeLinkedRevision(self.uri, revision_id)

    def remove_planning_constraint(self, constraint_date, constraint):
        """Removes a planning constraint

        Args:
            constraint_date: the date of the planning constraint to remove.
            constraint: the type of constraint to remove.

        Returns:
            bool

        References:
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

        References:
            Tracker.resetWorkflow
        """
        self._verify_obj()
        self.session.tracker_client.service.resetWorkflow(self.uri)

    def _set_custom_field(self, key, value):
        """sends the custom field value to the server

        Args:
            key: the suds field name
            value:

        Returns:
            None

        References:
            Tracker.setCustomField
        """
        c = CustomField()
        c.key = key
        c.value = value
        c.parent_item_uri = self.uri
        self.session.tracker_client.service.setCustomField(c._suds_object)

    def set_fields_null(self, fields):
        """sets the specified fields to Null.

        Args:
            fields: list of fields to set to null

        Returns:
            None

        References:
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
            test_steps: a list of TestStep objects.

        Returns:
            None

         References:
            Test_Management.setTestSteps
        """
        self._verify_obj()
        if not test_steps:
            parm = suds.null()
        elif isinstance(test_steps, list):
            parm = []
            if isinstance(test_steps[0], TestStep):
                parm = [item._suds_object for item in test_steps]
            elif isinstance(test_steps[0], TestStep().
                            _suds_object.__class__):
                parm = test_steps
        else:
            raise PylarionLibException("Expecting a list of testStep objects")
        self.session.test_management_client.service.setTestSteps(self.uri,
                                                                 parm)

    def update(self):
        """Update the server with the current _WorkItem data

        Args:
            None

        Returns:
            None

        References:
            Tracker.updateWorkItem
        """
        self._verify_obj()
        self.session.tracker_client.service.updateWorkItem(self._suds_object)

    def update_attachment(self, attachment_id, path, title):
        """method update_attachment updates the specified attachment to the
        current _WorkItem

        Args:
            attachment_id: the ID of the attachment to be updated
            path: file path to upload
            title: u.User friendly name of the file

        Returns:
            None

        Notes:
            Raises an error if the test run object is not populated.

        References:
            Tracker.updateAttachment
        """
        self._verify_obj()
        data = self._get_file_data(path)
        filename = os.path.basename(path)
        self.session.tracker_client.service. \
            updateAttachment(self.uri, attachment_id, filename, title, data)

    def verify_required(self):
        for field in self._required_fields:
            if not getattr(self, field):
                raise PylarionLibException(
                    "{0} is a required field".format(field))

    def which_test_runs(self):
        """Gives the user a list of TestRun objects that the current WorkItem
        instance is contained in.

        Args:
            None

        Returns:
            list of TestRun objects
        """
        # import done in the function so as not to cause circular refs
        from pylarion.test_run import TestRun
        return TestRun.search(self.work_item_id)


class _SpecificWorkItem(_WorkItem):
    """specific work item is a class that contains the WorkItem implementation
    that is different per WorkItem type. Classes that inherit from this class
    must define the _wi_type class attribute as a minimum.
    """
    _wi_type = ""

    @classmethod
    def create(cls, project_id, title, desc, status="draft", **kwargs):
        """Creates the specific type of work item, requiring the base fields to
        be passed in and all required custom fields as key word args. If not
        all required fields are passed in or key word fields that are not
        custom, it raises an exception.

        Args:
            project_id: The project to create the WorkItem in
            work_item_id: The unique id for the WorkItem
            title: the title of the WorkItem
            desc: the Description of the WorkItem
            status: the initial status of the WorkItem, draft by default
            kwargs: keyword arguments for custom fields. All required custom
                    fields must appear as keyword arguments.
        """
        all_fields, reqs = cls.get_custom_fields(project_id)
        fields = ""
        for req in reqs:
            if req not in kwargs:
                fields += (", " if fields else "") + req
        if fields:
            raise PylarionLibException("These parameters are required: {0}".
                                       format(fields))
        for field in kwargs:
            if field not in all_fields and field not in cls._cls_suds_map:
                fields += (", " if fields else "") + field
        if fields:
            raise PylarionLibException("These parameters are unknown: {0}".
                                       format(fields))
        return super(_SpecificWorkItem, cls).create(
            project_id, cls._wi_type, title, desc, status, **kwargs)

    @classmethod
    def get_custom_fields(cls, project_id):
        """List of custom fields for the project and specific wi_type

        Args:
            project_id: project that the user is working with

        Returns:
            tuple containing:
                a) list of all custom fields
                b) list of all required fields
        """
        cfts = cls.get_defined_custom_field_types(project_id,
                                                  cls._wi_type)
        all_fields = []
        required_fields = []
        for cft in cfts:
                # convert the custom field name to use code convention, where
                # possible
                split_name = re.findall('[a-zA-Z][^A-Z]*', cft.id)
                local_name = "_".join(split_name).replace("U_R_I", "uri"). \
                    replace("W_I", "wi").lower()
                all_fields.append(local_name)
                if cft.required:
                    required_fields.append(local_name)
        return (all_fields, required_fields)

    def __init__(self, project_id=None, work_item_id=None, suds_object=None,
                 uri=None, fields=None, revision=None):
        """In this constructor, it adds the custom fields per WorkItem type to
        the _cls_suds_map along with the is_custom and is_enum fields.
        In the property builder of the base class, it defines special behavior
        for custom fields so they are treated like regular attributes
        """
        if not project_id:
            project_id = self.default_project
        self._required_fields = []
        self._changed_fields = {}
        cfts = self.get_defined_custom_field_types(project_id,
                                                   self._wi_type)
        for cft in cfts:
            # try to convert custom field names to use the coding conventions
            split_name = re.findall('[a-zA-Z][^A-Z]*', cft.id)
            local_name = "_".join(split_name).replace("U_R_I", "uri"). \
                replace("W_I", "wi").lower()
            self._cls_suds_map[local_name] = {}
            self._cls_suds_map[local_name]["field_name"] = cft.id
            # types are returned in format:
            # * nsX:obj_type for objects and
            # * xsd:string for native types
            # for all object types, I need special processing.
            parse_type = cft.type.split(":")
            if parse_type[0].startswith("ns"):
                self._cls_suds_map[local_name]["cls"] = \
                    globals()[parse_type[1]]
            self._cls_suds_map[local_name]["enum_id"] = getattr(cft,
                                                                "enum_id",
                                                                None)
            self._cls_suds_map[local_name]["is_custom"] = True
            if cft.required:
                self._required_fields.append(local_name)
        super(_SpecificWorkItem, self).__init__(project_id, work_item_id,
                                                suds_object, uri, fields,
                                                revision)
        if not self.type:
            self.type = self._wi_type
        if self.type != self._wi_type:
            raise PylarionLibException("This is of type {0}, not type {1}".
                                       format(self.type, self._wi_type))

    def update(self):
        """calls update on changes to the work item.
        It first verifies that required fields are all set, then calls update
        on the object and then iterates the custom fields and updates each one
        """
        self.verify_required()
        super(_SpecificWorkItem, self).update()
        for field in self._changed_fields:
            if field == "testSteps":
                self.set_test_steps(self._changed_fields[field].steps[0])
            else:
                self._set_custom_field(field, self._changed_fields[field])
        self._changed_fields = {}


# each workitem class has a few special attributes in the _cls_suds_map
# so it requires a deep copy so it doesn't interfere with the class
# attribute.
class FunctionalTestCase(_SpecificWorkItem):
    _wi_type = "functionaltestcase"
    _cls_suds_map = copy.deepcopy(_SpecificWorkItem._cls_suds_map)
    _cls_suds_map["previous_status"]["enum_id"] = "functionaltestcase-status"
    _cls_suds_map["status"]["enum_id"] = "functionaltestcase-status"


class NonFunctionalTestCase(_SpecificWorkItem):
    _wi_type = "nonfunctionaltestcase"
    _cls_suds_map = copy.deepcopy(_SpecificWorkItem._cls_suds_map)
    _cls_suds_map["previous_status"]["enum_id"] = \
        "nonfunctionaltestcase-status"
    _cls_suds_map["status"]["enum_id"] = "nonfunctionaltestcase-status"


class StructuralTestCase(_SpecificWorkItem):
    _wi_type = "structuraltestcase"
    _cls_suds_map = copy.deepcopy(_SpecificWorkItem._cls_suds_map)
    _cls_suds_map["previous_status"]["enum_id"] = "structuraltestcase-status"
    _cls_suds_map["status"]["enum_id"] = "structuraltestcase-status"


class TestSuite(_SpecificWorkItem):
    _wi_type = "testsuite"
    _cls_suds_map = copy.deepcopy(_SpecificWorkItem._cls_suds_map)
    _cls_suds_map["previous_status"]["enum_id"] = "testsuite-status"
    _cls_suds_map["status"]["enum_id"] = "testsuite-status"


class UnitTestCase(_SpecificWorkItem):
    _wi_type = "unittestcase"
    _cls_suds_map = copy.deepcopy(_SpecificWorkItem._cls_suds_map)
    _cls_suds_map["previous_status"]["enum_id"] = "unittestcase-status"
    _cls_suds_map["status"]["enum_id"] = "unittestcase-status"


class BusinessCase(_SpecificWorkItem):
    _wi_type = "businesscase"
    _cls_suds_map = copy.deepcopy(_SpecificWorkItem._cls_suds_map)
    _cls_suds_map["previous_status"]["enum_id"] = "businesscase-status"
    _cls_suds_map["status"]["enum_id"] = "businesscase-status"


class Requirement(_SpecificWorkItem):
    _wi_type = "requirement"
    _cls_suds_map = copy.deepcopy(_SpecificWorkItem._cls_suds_map)
    _cls_suds_map["previous_status"]["enum_id"] = "requirement-status"
    _cls_suds_map["status"]["enum_id"] = "requirement-status"
    _cls_suds_map["resolution"]["enum_id"] = "requirement-resolution"
    _cls_suds_map["severity"]["enum_id"] = "requirement-severity"


class ChangeRequest(_SpecificWorkItem):
    _wi_type = "changerequest"


class Incident(_SpecificWorkItem):
    _wi_type = "incident"
    _cls_suds_map = copy.deepcopy(_SpecificWorkItem._cls_suds_map)
    _cls_suds_map["previous_status"]["enum_id"] = "incident-status"
    _cls_suds_map["status"]["enum_id"] = "incident-status"
    _cls_suds_map["resolution"]["enum_id"] = "incident-resolution"
    _cls_suds_map["severity"]["enum_id"] = "incident-severity"
    _cls_suds_map["priority"]["enum_id"] = "incident-priority"


class Defect(_SpecificWorkItem):
    _wi_type = "defect"
    _cls_suds_map = copy.deepcopy(_SpecificWorkItem._cls_suds_map)
    _cls_suds_map["severity"]["enum_id"] = "defect-severity"
    _cls_suds_map["priority"]["enum_id"] = "defect-priority"


class Task(_SpecificWorkItem):
    _wi_type = "task"
    _cls_suds_map = copy.deepcopy(_SpecificWorkItem._cls_suds_map)
    _cls_suds_map["severity"]["enum_id"] = "task-severity"


class Risk(_SpecificWorkItem):
    _wi_type = "risk"
    _cls_suds_map = copy.deepcopy(_SpecificWorkItem._cls_suds_map)
    _cls_suds_map["previous_status"]["enum_id"] = "risk-status"
    _cls_suds_map["status"]["enum_id"] = "risk-status"
    _cls_suds_map["resolution"]["enum_id"] = "risk-resolution"
