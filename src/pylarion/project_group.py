# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals
from pylarion.exceptions import PylarionLibException
import pylarion.base_polarion as bp
import pylarion.subterra_uri as stu
import pylarion.project as p


class ProjectGroup(bp.BasePolarion):
    """Object to handle the Polarion WSDL tns2:ProjectGroup class

    Attributes (for specific details, see Polarion):
        group_uris (ArrayOfSubterraURI)
        location (Location)
        name (string)
        parent_uri (SubterraURI)
        project_ids (ArrayOfstring)
"""
    _cls_suds_map = {"group_uris": {"field_name": "groupURIs",
                                    "is_array": True,
                                    "cls": stu.SubterraURI,
                                    "arr_cls": stu.ArrayOfSubterraURI,
                                    "inner_field_name": "SubterraURI"},
                     "location": "location",
                     "name": "name",
                     "parent_uri": {"field_name": "parentURI",
                                    "cls": stu.SubterraURI},
                     "project_ids": "projectIDs",
                     "uri": "_uri",
                     "_unresolved": "_unresolved"}
    _obj_client = "project_client"
    _obj_struct = "tns2:ProjectGroup"

    @classmethod
    def get_root_project_group(cls):
        """Gets the root project group.
        Args: None
        Returns:
            p.ProjectGroup object
        Impements:
            p.Project.getRootProjectGroup
        """
        return cls(suds_object=cls.session.project_client.service.
                   getRootProjectGroup())

    def __init__(self, uri=None, location=None, suds_object=None):
        """ProjectGroup constructor.

        Args:
            uri - the uri that references the Polarion ProjectGroup
            location - the location of the Polarion ProjectGroup
            suds_object - Polarion ProjectGroup object. When given, the object
                          is populated by object data.
        Notes:
            Either uri or suds_object or location in or none of them.
            If none of the identifying parameters are
            passed in an empty object is created
        Implements:
            p.Project.getProjectGroup
            p.Project.getProjectGroupAtLocation
        """
        super(self.__class__, self).__init__(suds_object=suds_object)
        if uri:
            self._suds_object = self.session.project_client. \
                getProjectGroup(uri)
        elif location:
            self._suds_object = self.session.project_client. \
                getProjectGroupAtLocation(location)

    def get_contained_groups(self):
        """Gets all project groups located directly below the project group.
        Args:
            None
        Returns:
            list of p.ProjectGroup objects
        Implements:
            p.Project.getContainedGroups
        """
        self._verify_obj()
        groups = []
        for suds_group in self.session.project_client.service. \
                getContainedGroups(self.uri):
            groups.append(self.__class__(suds_object=suds_group))
        return groups

    def get_contained_projects(self):
        """Gets all projects located directly below the project group.
        Args:
            None
        Returns:
            list of p.Project objects
        Implements:
            p.Project.getContainedProjects
        """
        self._verify_obj()
        projects = []
        for suds_project in self.session.project_client.service. \
                getContainedProjects(self.uri):
            projects.append(p.Project(suds_object=suds_project))
        return projects

    def get_deep_contained_projects(self):
        """Gets all projects located below the project group.
        Args:
            None
        Returns:
            list of p.Project objects
        Implements:
            p.Project.getDeepContainedProjects
        """
        self._verify_obj()
        projects = []
        for suds_project in self.session.project_client.service. \
                getDeepContainedProjects(self.uri):
            projects.append(p.Project(suds_object=suds_project))
        return projects
