# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals
from pylarion.base_polarion import BasePolarion
from pylarion.category import Category
from pylarion.custom_field_type import CustomFieldType
from pylarion.text import Text
from pylarion.user import User
from pylarion.subterra_uri import SubterraURI
from pylarion.exceptions import PylarionLibException
from pylarion.tests_configuration import TestsConfiguration


class Project(BasePolarion):
    """Object to handle the Polarion WSDL tns4:Project class

    Attributes (for specific details, see Polarion):
        active (boolean)
        description (Text)
        finish (date)
        lead (User)
        location (str)
        lock_work_records_date (date)
        name (string)
        project_group_uri (SubterraURI)
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
                     "project_group_uri":
                     {"field_name": "projectGroupURI",
                      "cls": SubterraURI},
                     "project_id": "id",
                     "start": "start",
                     "tracker_prefix": "trackerPrefix",
                     "uri": "_uri",
                     "_unresolved": "_unresolved"}
    _id_field = "project_id"
    _obj_client = "project_client"
    _obj_struct = "tns2:Project"

    @classmethod
    def get_context_roles(cls, location):
        """Returns the context (project) roles for the given location.

        Args:
            location - the location of the context (project/project group)
        Returns:
            list of roles
        Implements:
            Security.getContextRoles
        """
        return cls.session.security_client.service.getContextRoles(location)

    def __init__(self, project_id=None, suds_object=None, location=None,
                 uri=None):
        """Project constructor.

        Args:
            Optional
                project_id - when given, the object is populated with the
                             Project data.
                suds_object - PolarionProject object. When given, the object
                              is populated by object data.
                location - the location of the Polarion project
                uri - the uri that references the PolarionProject
        Notes:
            Either project_id or suds_object or location or uri can be passed
            in or none of them. If none of the identifying parameters are
            passed in an empty object is created
        Implements:
            Project.getProject
            Project.getProjectatLocation
            Project.getProjectByURI
        """
        super(self.__class__, self).__init__(project_id, suds_object)
        if project_id:
            self._suds_object = self.session.project_client.service. \
                getProject(project_id)
        elif location:
            self._suds_object = self.session.project_client.service. \
                getProjectatLocation(location)
        elif uri:
            self._suds_object = self.session.project_client.service. \
                getProjectByURI(uri)
        if project_id or location or uri:
            if not getattr(self._suds_object, "_unresolvable", None):
                raise PylarionLibException("The Project was not found.")

    def create_document(self, location, document_name, document_title,
                        allowed_wi_types, structure_link_role,
                        home_page_content):
        # There is no document object.
        # don't know what to do with the URI it returns.
        """method create_document creates a document in the current project in
        the location specified.

        Args:
            location - document space location with one component or null for
                       default space (can be null)
            document_name - Document name (not null)
            document_title - Document title (can be null)
            allowed_wi_types - one type can be specified (can be null)
            structure_link_role - role which defines the hierarchy of work
                                  items inside the Document (not null)
            home_page_content - HTML markup for document home page
                                (can be null)

        Returns
            None
        Implements:
            Tracker.createDocument
        """
        self._verify_obj()
        self.session.tracker_client.service.createDocument(self.project_id,
                                                           location,
                                                           document_name,
                                                           document_title,
                                                           allowed_wi_types,
                                                           structure_link_role,
                                                           home_page_content)

    def get_categories(self):
        """ method get_categories retrieves a list of Category objects

        Args:
            None
        Returns:
            list of Category objects
        Implements:
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
            work_item_type_id - the workitem type ID.
        Returns:
            list of key for the project for the given workitem type
        Implements:
            Tracker.getDefinedCustomFieldkeys
        """
        self._verify_obj()
        return self.session.tracker_client.service.getDefinedCustomFieldkeys(
            self.project_id, work_item_type_id)

    def get_defined_custom_field_type(self, work_item_type_id, key):
        """method get_defined_custom_field_type gets custom field definition
        of a work item type for the given key.

        Args:
            work_item_type_id - the workitem type ID.
            key - The key of the custom field
        Returns:
            CustomFieldType object
        Implements:
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
            work_item_type_id - the workitem type ID.
        Returns:
            list of CustomFieldType object
        Implements:
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
        Implements:
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
        Implements:
            Tracker.getDocumentSpaces
        """
        self._verify_obj()
        return self.session.tracker_client.service. \
            getDocumentSpaces(self.project_id)

    def get_project_users(self):
        """Gets users of the project
        Args: None
        Returns:
            list of u.User objects
        Implements:
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

        Returns:
            list of configuration of the Test Steps custom field.
        Implements:
            TestManagement.getTestStepsConfiguration
        """
        self._verify_obj()
        config_steps = self.session.test_management_client.service. \
            getTestStepsConfiguration(self.project_id)
        return config_steps[0]

    def get_tests_configuration(self):
        """method get_tests_configuration retrieves the test management
        configuration for the project

        Returns:
            TestsConfiguration object
        Implements:
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
        Implements:
            Tracker.getWikiSpaces
        """
        self._verify_obj()
        return self.session.tracker_client.service.getWikiSpaces(
            self.project_id)
