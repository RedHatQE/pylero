# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals
import pylarion.base_polarion as bp
import pylarion.text as t
import pylarion.subterra_uri as stu
from pylarion.exceptions import PylarionLibException


class User(bp.BasePolarion):
    """Object to handle the Polarion WSDL tns3:User class

    Attributes (for specific details, see Polarion):
        description (Text)
        disabled_notifications (boolean)
        email (string)
        user_id (string)
        name (string)
        vote_uris (ArrayOfSubterraURI)
        watche_uris (ArrayOfSubterraURI)
"""
    _cls_suds_map = {"description": {"field_name": "description",
                                     "cls": t.Text},
                     "disabled_notifications": "disabledNotifications",
                     "email": "email",
                     "user_id": "id",
                     "name": "name",
                     "vote_uris": {"field_name": "voteURIs",
                                   "is_array": True,
                                   "cls": stu.SubterraURI,
                                   "arr_cls": stu.ArrayOfSubterraURI,
                                   "inner_field_name": "SubterraURI"},
                     "watche_uris": {"field_name": "watcheURIs",
                                     "is_array": True,
                                     "cls": stu.SubterraURI,
                                     "arr_cls": stu.ArrayOfSubterraURI,
                                     "inner_field_name": "SubterraURI"},
                     "uri": "_uri",
                     "_unresolved": "_unresolved"}
    _id_field = "user_id"
    _obj_client = "project_client"
    _obj_struct = "tns2:User"

    @classmethod
    def create_user(cls, user_id):
        """class method create_user that creates a Polarion user.

        Args:
            user_id - the id of the user to create (login name)
        Returns
            new User object
        Implements:
            p.Project.createUser
        """
        suds_object = cls.session.project_client.service.createUser(user_id)
        user = User()
        user._suds_object = suds_object
        return user

    @classmethod
    def get_user_from_token(cls, token):
        """Returns the username of the user that has the assigned token.
        Args:
            token
        Returns:
            user_id
        Implements:
            Security.getUserFromToken
        """
        return cls.session.security_client.service.getuserFromToken(token)

    @classmethod
    def get_users(cls):
        """class method that returns all the system users

        Args:
            None

        Returns:
            list containing User objects for all users.
        Implements:
            p.Project.getUsers
        """
        users = []
        suds_objects = cls.session.project_client.service.getUsers()
        for suds_object in suds_objects:
            user = User()
            user._suds_object = suds_object
            users.append(user)
        return users

    def __init__(self, user_id=None, suds_object=None, uri=None):
        """User constructor.

        Args:
            user_id - when given, the object is populated with user's data
            suds_object - Polarion User object. When given, the object is
                          populated by object data.
            uri - when given, the object is populated with user's data
        Notes:
            Either user_id, suds_object or uri can be passed in, not multiple
        Implements:
            p.Project.getUser
            p.Project.getUserByUri
        """
        super(self.__class__, self).__init__(user_id, suds_object)
# user_id will be null if called from the get_users class function
        if user_id or uri:
            if user_id:
                self._suds_object = \
                    self.session.project_client.service.getUser(user_id)
            elif uri:
                self._suds_object = self.session.project_client.service. \
                    getUserByUri(uri)
            if not getattr(self._suds_object, "_unresolvable", None):
                raise PylarionLibException(
                    "The user {0} was not found.".format(user_id))

    def get_context_roles(self, location):
        """Returns the context (project) roles for the user at given location.

        Args:
            location - the location of the context (project/project group)
        Returns:
            list of roles
        Implements:
            Security.getContextRolesForUser
        """
        self._verify_obj()
        return self.session.security_client.service.getContextRolesForUser(
            self.user_id, location)

    def get_roles(self, location):
        """Returns all global and context roles for the context at given
        location assigned to the user.

        Args:
            location
        Returns:
            list of roles
        Implements:
            Security.getRolesForUser
        """
        self._verify_obj()
        return self.session.security_client.service.getRolesForUser(
            self.user_id, location)

# getUserAvatarURL parameter is misnamed in the docs. it really takes user id.
    def get_user_avatar_url(self):
        """method get_user_avatar_url, returns a string with the relative URL
        of the user's avatar.

        Args:
            None

        Notes:
            Raises an error if the User is not populated.
        Implements:
            p.Project.getUserAvatarURL
        """
        if self.user_id:
            return self.session.project_client.service.getUserAvatarURL(
                self.user_id)
        else:
            raise PylarionLibException("The user object is empty")

    def has_permission(self, permission, project_id):
        """Checks if given permission is granted to the user.

        Args:
            permission - the permission to check.
            projectId - the id of the project to check the permission in,
                        None to check global permissions.
        Returns:
            bool
        Implements:
            Security.hasPermission
        """
        self._verify_obj()
        return self.session.security_client.service.hasPermission(self.user_id,
                                                                  permission,
                                                                  project_id)

    def update(self):
        """method update, updates Polarion with the User attributes

        Args:
            None

        Notes:
            Raises an error if the User is not populated.
        Implements:
            p.Project.updateUser
        """
        if self.user_id:
            # self._map_to_suds()
            self.session.project_client.service.updateUser(self._suds_object)
            # CHECK for verification
        else:
            raise PylarionLibException("The user object is empty")


class ArrayOfUser(bp.BasePolarion):
    _obj_client = "builder_client"
    _obj_struct = "tns3:ArrayOfUser"
