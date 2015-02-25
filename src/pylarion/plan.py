# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals
import suds
from pylarion.exceptions import PylarionLibException
import pylarion.base_polarion as bp
import pylarion.subterra_uri as stu
import pylarion.enum_option_id as eoi
import pylarion.custom as custom
import pylarion.text as t
from pylarion.plan_record import PlanRecord
from pylarion.plan_statistics import PlanStatistics
from pylarion.plan_record import ArrayOfPlanRecord
import pylarion.work_item as wi


class Plan(bp.BasePolarion):
    """Object to handle the Polarion WSDL tns6:Plan class

    Attributes (for specific details, see Polarion):
        allowed_types (ArrayOfeoi.EnumOptionId)
        author_uri (SubterraURI)
        calculation_type (eoi.EnumOptionId)
        capacity (float)
        color (string)
        created (dateTime)
        custom_fields (ArrayOfCustom)
        default_estimate (float)
        description (Text)
        due_date (date)
        estimation_field (string)
        finished_on (dateTime)
        is_template (boolean)
        location (Location)
        name (string)
        parent (Plan)
        plan_id (string)
        previous_time_spent (duration)
        prioritization_field (string)
        project_uri (SubterraURI)
        records (ArrayOfPlanRecord)
        sort_order (int)
        start_date (date)
        started_on (dateTime)
        status (eoi.EnumOptionId)
        template_uri (SubterraURI)
        updated (dateTime)
"""
    _cls_suds_map = {"allowed_types": {"field_name": "allowedTypes",
                                       "is_array": True,
                                       "cls": eoi.EnumOptionId,
                                       "arr_cls": eoi.ArrayOfEnumOptionId,
                                       "inner_field_name": "eoi.EnumOptionId"},
                     "author_uri": {"field_name": "authorURI",
                                    "cls": stu.SubterraURI},
                     "calculation_type": {"field_name": "calculationType",
                                          "cls": eoi.EnumOptionId},
                     "capacity": "capacity",
                     "color": "color",
                     "created": "created",
                     "custom_fields": {"field_name": "customFields",
                                       "is_array": True,
                                       "cls": custom.Custom,
                                       "arr_cls": custom.ArrayOfCustom,
                                       "inner_field_name": "Custom"},
                     "default_estimate": "defaultEstimate",
                     "description": {"field_name": "description",
                                     "cls": t.Text},
                     "due_date": "dueDate",
                     "estimation_field": "estimationField",
                     "finished_on": "finishedOn",
                     "is_template": "isTemplate",
                     "location": "location",
                     "name": "name",
                     "parent": {"field_name": "parent"},
                     "plan_id": "id",
                     "previous_time_spent": "previousTimeSpent",
                     "prioritization_field": "prioritizationField",
                     "project_uri": {"field_name": "projectURI",
                                     "cls": stu.SubterraURI},
                     "records": {"field_name": "records",
                                 "is_array": True,
                                 "cls": PlanRecord,
                                 "arr_cls": ArrayOfPlanRecord,
                                 "inner_field_name": "PlanRecord"},
                     "sort_order": "sortOrder",
                     "start_date": "startDate",
                     "started_on": "startedOn",
                     "status": {"field_name": "status",
                                "cls": eoi.EnumOptionId},
                     "template_uri": {"field_name": "templateURI",
                                      "cls": stu.SubterraURI},
                     "updated": "updated",
                     "uri": "_uri",
                     "_unresolved": "_unresolved"}
    _obj_client = "builder_client"
    _obj_struct = "tns6:Plan"
    _id_field = "plan_id"

    @classmethod
    def create(cls, plan_id, plan_name, project_id, parent_id, template_id):
        """Creates a new plan

        Args:
            plan_id (str) - The id of the new plan
            plan_name - The name of the new plan
            project_id (str)- The project the plan will be created in
            parent_id - The id of the parent plan (can be null)
            template_id - The id of the template used for this plan
        Returns:
            Plan Object
        Implements
            Planning.createPlan
        """
        uri = cls.session.planning_client.service.createPlan(project_id,
                                                             plan_name,
                                                             plan_id,
                                                             parent_id,
                                                             template_id)
        return Plan(uri=uri)

    @classmethod
    def create_plan_template(cls, template_id, template_name, project_id,
                             parent_id):
        """Creates a new plan template

        Args:
            template_id (str) - The id of the new template
            template_name - The name of the new template
            project_id (str)- The project the plan will be created in
            parent_id - The id of the template the new template is based on
                        (can be null)
        Returns:
            Plan Object
        Implements:
            Planning.createPlanTemplate
        """
        uri = cls.session.planning_client.service.createPlanTemplate(
            project_id, template_name, template_id, parent_id)
        return Plan(uri=uri)

    @classmethod
    def delete_plans(cls, project_id, plan_ids):
        """Delete specified plans

        Args:
            project_id - the project the plans will be deleted in
            plan_ids - list of plan ids to delete.
        Returns:
            None
        Implements:
            Planning.deletePlans
        """
        cls.session.planning_client.service.deletePlans(project_id, plan_ids)

    @classmethod
    def search(cls, query, sort="plan_id", limit=-1, fields=[],
               search_templates=False):
        """search plans or plan templates

        Args
            query
            sort
            limit - the maximum number of records to be returned,
                    -1 for no limit.
            fields - list of the fields requested.
        Returns:
            list of Plan objects
        Implements:
            Planning.searchPlanTemplates
            Planning.searchPlanTemplatesWithFields
            Planning.searchPlans
            Planning.searchPlansWithFields
        """
        # function names and parameter lists generated dynamically based on
        # parameters passed in.
        if search_templates:
            function_name = "SearchPlanTemplates"
        else:
            function_name = "SearchPlans"
        if fields:
            function_name += "WithFields"
        parms = [query, sort, limit] + \
                [cls._convert_obj_fields_to_polarion(fields)] if fields else []
        plans = []
        for sud_plan in getattr(cls.session.planning_client.service,
                                function_name)(*parms):
            plans.append(Plan(suds_object=sud_plan))
        return plans

    def __init__(self, plan_id=None, project_id=None, uri=None,
                 suds_object=None):
        """Plan Constructor

        Args:
            plan_id - ID of the plan
            project_id - ID of the project that contains the specific plan
                         required when plan_id is given
            uri - the stu.SubterraURI of the plan to load
            suds_object - the Polarion Plan object
        Returns:
            None
        Implements:
            Planning.getPlanById
            Planning.getPlanByUri
        """
        super(self.__class__, self).__init__(obj_id=plan_id,
                                             suds_object=suds_object)
        if plan_id:
            if not project_id:
                raise PylarionLibException("When plan_id is passed in, "
                                           "project_id is required")
            self._suds_object = self.session.planning_client.service. \
                getPlanById(project_id, plan_id)
        elif uri:
            self._suds_object = self.session.planning_client.service. \
                getPlanByUri(uri)
        if plan_id or uri:
            if not (hasattr(self._suds_object, "_unresolvable") or
                    self._suds_object._unresolvable):
                raise PylarionLibException(
                    "The Plan {0} was not found.".format(plan_id))

    def _fix_circular_refs(self):
        # The module references itself as a class attribute, which is not
        # allowed, so the self reference is defined here.
        self._cls_suds_map["parent"]["cls"] = self.__class__

    def add_plan_items(self, work_items):
        """Add plan records to the plan.

        Args:
            items - list of work_item_ids
        Returns:
            None
        Implements:
            Planning.addPlanItems
        """
        self._verify_obj()
        if work_items:
            if not isinstance(work_items, list):
                raise PylarionLibException(
                    "work_items must be a list of wi.WorkItem objects")
        p_items = []
        for item in work_items:
            if isinstance(item, wi.WorkItem):
                p_items.append(item._suds_object)
            elif isinstance(item, wi.WorkItem()._suds_object.__class__):
                p_items.append(item)
        self.session.planning_client.service.addPlanItems(self.uri, p_items)

    def get_statistics(self):
        """get statistics of the plan

        Args:
            None
        Returns:
            PlanStatistics object
        Implements:
            Planning.getPlanStatistics
        """
        self._verify_obj()
        suds_stat = self.session.planning_client.service.getPlanStatistics(
            self.uri)
        return PlanStatistics(suds_object=suds_stat)

    def get_wiki_content(self):
        """Returns the wiki content of the plan

        Args:
            None
        Returns:
            t.Text object
        Implements:
            Planning.getPlanWikiContent
        """
        self._verify_obj()
        suds_obj = self.session.planning_client.service.getPlanWikiContent(
            self.uri)
        return t.Text(suds_object=suds_obj)

    def remove_plan_items(self, work_items):
        """Remove plan records to the plan.

        Args:
            items - list of work_item_ids
        Returns:
            None
        Implements:
            Planning.removePlanItems
        """
        self._verify_obj()
        if work_items:
            if not isinstance(work_items, list):
                raise PylarionLibException(
                    "work_items must be a list of wi.WorkItem objects")
        p_items = []
        for item in work_items:
            if isinstance(item, wi.WorkItem):
                p_items.append(item._suds_object)
            elif isinstance(item, wi.WorkItem()._suds_object.__class__):
                p_items.append(item)
        self.session.planning_client.service.removePlanItems(self.uri, p_items)

    def set_wiki_content(self, content):
        """method set_wiki_content updates the wiki for the current Plan

        Args:
            Content (str or t.Text object)
        Returns:
            None
        Implements:
            Planning.setPlanWikiContent
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
        self.session.planning_client.service. \
            setPlanWikiContent(self.uri, suds_content)

    def update(self):
        """updates the server with the current plan content

        Args:
            None
        Returns:
            None
        Implements:
            Planning.updatePlan
        """
        self._verify_obj()
        self.session.planning_client.service.updatePlan(self._suds_object)

    def was_started(self):
        """checks if the plan was started yet

        Args:
            None
        Returns:
            bool
        Implements:
            Planning.wasPlanStarted
        """
        self._verify_obj()
        return self.session.planning_client.service.wasPlanStarted(self.uri)


class ArrayOfPlan(bp.BasePolarion):
    _obj_client = "builder_client"
    _obj_struct = "tns6:ArrayOfPlan"
