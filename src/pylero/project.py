# -*- coding: utf8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import copy

from pylero.base_polarion import BasePolarion
from pylero.category import Category
from pylero.custom_field_type import CustomFieldType
from pylero.exceptions import PyleroLibException
from pylero.tests_configuration import TestsConfiguration
from pylero.text import Text
from pylero.user import User


class Project(BasePolarion):
    """Object to handle the Polarion WSDL tns4:Project class

    Attributes:
        active (boolean)
        description (Text)
        finish (date)
        lead (User)
        location (str)
        lock_work_records_date (date)
        name (string)
        project_group (ProjectGroup)
        project_id (string)
        start (date)
        tracker_prefix (string)
"""
    _cls_suds_map = {"active": "active",
                     "description":
                     {"field_name": "description",
                      "cls": Text},
                     "finish": "finish",
                     "lead":
                     {"field_name": "lead",
                      "cls": User},
                     "location": "location",
                     "lock_work_records_date": "lockWorkRecordsDate",
                     "name": "name",
                     "project_group":
                     {"field_name": "projectGroupURI",
                      # cls is defined in _fix_circular_refs function
                      "named_arg": "uri",
                      "sync_field": "uri"},
                     "project_id": "id",
                     "start": "start",
                     "tracker_prefix": "trackerPrefix",
                     "uri": "_uri",
                     "_unresolved": "_unresolved"}
    _id_field = "project_id"
    _obj_client = "project_client"
    _obj_struct = "tns2:Project"

    URI_STRUCT = "subterra:data-service:objects:/default/" \
                 "%(id)s${%(obj)s}%(id)s"

    @classmethod
    def get_context_roles(cls, location):
        """Returns the context (project) roles for the given location.

        Args:
            location: the location of the context (project/project group)

        Returns:
            list of roles

        References:
            Security.getContextRoles
        """
        return cls.session.security_client.service.getContextRoles(location)

    def __init__(self, project_id=None, suds_object=None, location=None,
                 uri=None):
        """Project constructor.

        Args:
            project_id: when given, the object is populated with the
                         Project data.
            suds_object: PolarionProject object. When given, the object
                          is populated by object data.
            location: the location of the Polarion project
            uri: the uri that references the PolarionProject

        Notes:
            Either project_id or suds_object or location or uri can be passed
            in or none of them. If none of the identifying parameters are
            passed in an empty object is created

        References:
            Project.getProject
            Project.getProjectatLocation
            Project.getProjectByURI
        """
        super(self.__class__, self).__init__(project_id, suds_object)
        if project_id:
            # if the project is already cached, make a deep copy and use it.
            # If not, get it and add it to the cache.
            project = self._cache["projects"].get(project_id)
            if project:
                self._suds_object = copy.deepcopy(project)
            else:
                self._suds_object = self.session.project_client.service. \
                    getProject(project_id)
                self._cache["projects"][project_id] = self._suds_object
        elif location:
            self._suds_object = self.session.project_client.service. \
                getProjectatLocation(location)
        elif uri:
            self._suds_object = self.session.project_client.service. \
                getProjectByURI(uri)
        if project_id or location or uri:
            if getattr(self._suds_object, "_unresolvable", True):
                raise PyleroLibException("The Project was not found.")

    def _fix_circular_refs(self):
        # The module references ProjectGroup, which references this class
        # This is not allowed, so the self reference is defined here.
        from pylero.project_group import ProjectGroup
        self._cls_suds_map["project_group"]["cls"] = ProjectGroup

    def get_categories(self):
        """ method get_categories retrieves a list of Category objects

        Args:
            None

        Returns:
            list of Category objects

        References:
            Tracker.getCategories
        """
        self._verify_obj()
        categories = []
        for suds_cat in self.session.tracker_client.service. \
                getCategories(self.project_id):
            categories.append(Category(suds_object=suds_cat))
        return categories

    def get_defined_custom_field_keys(self, work_item_type_id):
        """Gets all custom field keys defined for a workitem type in a project.

        Args:
            work_item_type_id: the workitem type ID.

        Returns:
            list of key for the project for the given workitem type

        References:
            Tracker.getDefinedCustomFieldkeys
        """
        self._verify_obj()
        return self.session.tracker_client.service.getDefinedCustomFieldkeys(
            self.project_id, work_item_type_id)

    def get_defined_custom_field_type(self, work_item_type_id, key):
        """method get_defined_custom_field_type gets custom field definition
        of a work item type for the given key.

        Args:
            work_item_type_id: the workitem type ID.
            key: The key of the custom field

        Returns:
            CustomFieldType object

        References:
            Tracker.getDefinedCustomFieldType
        """
        self._verify_obj()
        suds_custom = self.session.tracker_client.service. \
            getDefinedCustomFieldType(self._uri, work_item_type_id, key)
        return CustomFieldType(suds_object=suds_custom)

    def get_defined_custom_field_types(self, work_item_type_id):
        """method get_defined_custom_field_type gets custom field definition
        of a work item type all keys.

        Args:
            work_item_type_id: the workitem type ID.

        Returns:
            list of CustomFieldType object

        References:
            Tracker.getDefinedCustomFieldType
        """
        self._verify_obj()
        customs = []
        for suds_custom in self.session.tracker_client.service. \
                getDefinedCustomFieldType(self._uri, work_item_type_id):
            customs.append(CustomFieldType(suds_object=suds_custom))
        return customs

    def get_document_locations(self):
        """Gets the document locations (e.g. LiveDocuments) for a project.

        Args:
            None

        Returns:
            list of (string) document locations

        References:
            Tracker.getDocumentLocations
        """
        self._verify_obj()
        return self.session.tracker_client.service. \
            getDocumentLocations(self.project_id)

    def get_document_spaces(self):
        """Gets the Module/Document spaces for the project.

        Args:
            None

        Returns:
            list of (string) document spaces

        References:
            Tracker.getDocumentSpaces
        """
        self._verify_obj()
        return self.session.tracker_client.service. \
            getDocumentSpaces(self.project_id)

    def get_project_users(self):
        """Gets users of the project

        Args:
            None

        Returns:
            list of u.User objects

        References:
            Project.getProjectUsers
        """
        self._verify_obj()
        users = []
        for suds_user in self.session.project_client.service. \
                getProjectUsers(self.project_id):
            users.append(User(suds_object=suds_user))

    def get_test_steps_configuration(self):
        """method get_test_steps_configuration retrieves a list of the
        Test Steps configuration for the project

        Args:
            None

        Returns:
            list of configuration of the Test Steps custom field.

        References:
            TestManagement.getTestStepsConfiguration
        """
        self._verify_obj()
        config_steps = self.session.test_management_client.service. \
            getTestStepsConfiguration(self.project_id)
        return config_steps[0]

    def get_tests_configuration(self):
        """method get_tests_configuration retrieves the test management
        configuration for the project

        Args:
            None

        Returns:
            TestsConfiguration object

        References:
            TestManagement.getTestsConfiguration
        """
        self._verify_obj()
        tests_config = self.session.test_management_client.service. \
            getTestsConfiguration(self.project_id)
        return TestsConfiguration(suds_object=tests_config)

    def get_wiki_spaces(self):
        """Returns Wiki spaces from current project

        Args:
            None

        Returns:
            Array of string

        References:
            Tracker.getWikiSpaces
        """
        self._verify_obj()
        return self.session.tracker_client.service.getWikiSpaces(
            self.project_id)
