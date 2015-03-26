# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals
import os
import base64
import suds
from pylarion.exceptions import PylarionLibException
from pylarion.server import Server
from __builtin__ import classmethod
from ConfigParser import SafeConfigParser


# classproperty is a property that works on the class level
class classproperty(property):
    """Returns a classmethod as the getter so that the property can be used as
    a class property. This is needed so that the property can be set for all
    child objects. This project currently has no need of a setter or deleter.
    """
    def __get__(self, instance, cls):
        return classmethod(self.fget).__get__(instance, cls)()


class Connection(object):
    """Creates a Polarion session as a class method, so that it is used for all
    objects inherited by BasePolarion.
    The url, repo, user and password are read from config files, which are
    located either the user's file at ~/.pylarion or the machine file at
    /etc/pylarion/pylarion.cfg
    """
    connected = False
    session = None
    GLOBAL_CONFIG = "/etc/pylarion/pylarion.cfg"
    LOCAL_CONFIG = os.path.expanduser("~") + "/.pylarion"
    CONFIG_SECTION = "webservice"
# Look at ConfigParser - https://docs.python.org/2.6/library/configparser.html

    @classmethod
    def session(cls):
        if not cls.connected:
            config = SafeConfigParser()
            if not config.read([cls.GLOBAL_CONFIG, cls.LOCAL_CONFIG]) or \
                    not config.has_section(cls.CONFIG_SECTION):
                raise PylarionLibException("The config files do not exist or"
                                           " are not of the correct format."
                                           " Valid files are: {0} or {1}"
                                           .format(cls.GLOBAL_CONFIG,
                                                   cls.LOCAL_CONFIG))
            server_url = config.get(cls.CONFIG_SECTION, "url")
            repo = config.get(cls.CONFIG_SECTION, "svn_repo")
            login = config.get(cls.CONFIG_SECTION, "user")
            pwd = config.get(cls.CONFIG_SECTION, "password")
            proj = config.get(cls.CONFIG_SECTION, "default_project")
            if not (server_url and login and pwd and proj):
                raise PylarionLibException("The config files must contain "
                                           "valid values for: url, user, "
                                           "password and default_project")
            srv = Server(server_url, login, pwd)
            cls.session = srv.session()
            cls.session._login()
            cls.connected = True
            cls.session.default_project = proj
            cls.session.user_id = login
            cls.session.password = pwd
            cls.session.repo = repo
        return cls.session


class BasePolarion(object):
    """BasePolarion is the parent class for all the WSDL Polarion objects that
    are published. Using the _cls_suds_map, the class creates a property for
    each attribute so that any access of the object attribute, will access the
    WSDL object that is contained by it.

    Attributes:
        _cls_suds_map (dict): maps the Polarion attribute names to the Pylarion
                        attribute names. Pylarion attribute names use the
                        Red Hat global CI naming conventions.
                        Attributes that reference either objects or an array of
                        objects have the properties relate to the relationship
                        meaning that accessing the property will give access to
                        the object or list of objects.
        _id_field (str): the field that represents an id field, used in the
                         child class's constructor. when a child's class
                         defines the field it allows this constructor to accept
                         an obj_id as a parameter
        _obj_client (str): The Polarion client the child's WSDL object is
                           defined by
        _obj_struct (str): The data type defined by the WSDL library. The
                           structure of the datatype is tnsX:ObjectName, the X
                           is per datatype and has no default.
        session (Session): The Polarion Session object, initialized by the
                           Connection class. This attribute connects to the
                           server one time per session, no matter how many
                           objects are instantiated.
        has_query (bool): Set by a child class if it can use the parent's query
                          method.
        default_project (str): The user's default project, to be used when
                          project_id is needed and there is none given
    """
    _cls_suds_map = {}
    _id_field = None
    _obj_client = None
    _obj_struct = None
    _session = None
    _default_project = None
    has_query = False
    _cache = {
        "enums": {},
        "custom_field_types": [],
        "projects": {}
    }

    @classproperty
    def session(cls):
        # Uses a class property for the session, so that the library doesn't
        # connect to the server until the library is actually used.
        if BasePolarion._session:
            return BasePolarion._session
        else:
            # For some reason, using the cls attribute makes it into a class
            # attribute for the specific class but not for all the other
            # Pylarion objects.
            BasePolarion._session = Connection.session()
            BasePolarion._default_project = cls._session.default_project
            BasePolarion.user_id = cls._session.user_id
            # stores password in the session so it can be used for direct svn
            # operations
            BasePolarion.password = cls._session.password
            BasePolarion.repo = cls._session.repo
            return BasePolarion._session

    @classproperty
    def default_project(cls):
        # Uses a class property for the session, so that the library connects
        # when accessing it.
        if not BasePolarion._default_project:
            cls.session
        return BasePolarion._default_project

    @classmethod
    def _convert_obj_fields_to_polarion(cls, fields=[]):
        """All child methods that take a fields parameter should pass the field
        array and it converts it to the Polarion attribute name using the
        _cls_suds_map. It uses the python map function over the fields list to
        return the list of its Polarion attribute name.
        """
        p_fields = []
        if fields:
            if not isinstance(fields, list):
                fields = [fields]
            # convert given fields to Polarion fields
            p_fields = map(lambda x: cls._cls_suds_map[x]
                           if not isinstance(cls._cls_suds_map[x], dict)
                           else cls._cls_suds_map[x]["field_name"], fields)
        return p_fields

    @classmethod
    def _query(cls, base_function_name, query, is_sql=False, fields=[],
               sort=suds.null(), limit=-1, baseline_revision=None,
               has_fields=True):
        """Searches the given object using the object's query function

        Args:
            base_function_name: start of the Polarion function name.
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

        Returns:
            list of objects
        """
        function_name = base_function_name
        p_fields = cls._convert_obj_fields_to_polarion(fields)
        if baseline_revision:
            function_name += "InBaseline"
        if is_sql:
            function_name += "BySQL"
            parms = [query]
        else:
            # unsure of the sort format. Probably need to convert to Polarion.
            parms = [query, sort]
        if baseline_revision:
            parms += [baseline_revision]
        parms += ([p_fields] if has_fields else []) + \
                 ([limit] if not is_sql and limit is not None else [])
        suds_objs = getattr(cls.session.tracker_client.service,
                            function_name)(*parms)
        # some functions return list of strings and not objects.
        if suds_objs and isinstance(suds_objs[0], basestring):
            return suds_objs
        else:
            objs = []
            for suds_obj in suds_objs:
                objs.append(cls(suds_object=suds_obj))
            return objs

    @classmethod
    def get_global_roles(cls):
        """Returns all global roles.

        Args:
            None

        Returns:
            list of global roles

        References:
            Security.\ :security:`getGlobalRoles()`
        """
        return cls.session.security_client.service.getGlobalRoles()

    @classmethod
    def has_current_user_permission(cls, permission, project_id):
        """Checks if given permission is granted to the current user.

        Args:
            permission: the permission to check.
            project_id: the id of the project to check the permission in,
                        None to check global permissions.

        Returns:
            bool

        References:
            Security.hasCurrentUserPermission
        """
        return cls.session.security_client.service.hasCurrentuserPermission(
            permission, project_id)

    def __init__(self, obj_id=None, suds_object=None):
        # _fix_circular_refs is a function that allows objects to contain
        # circular references by applying the reference only after the class
        # has been instantiated. Some objects contain references to themselves,
        # for example a parent attribute.
        if hasattr(self, "_fix_circular_refs"):
            self._fix_circular_refs()
        # if _id_field has not been set in the child class, the obj_id field
        # cannot be passed as a parameter.
        if obj_id and not self._id_field:
            raise PylarionLibException(
                "{0} only accepts a suds object, not an obj_id".format(
                    self.__class__.__name))
        if suds_object:
            self._suds_object = suds_object
        else:
            self._get_suds_object()
        # initialize all instance attributes as properties
        # check if the property already exists. If so, use existing.
        for key in self._cls_suds_map.keys():
            if not hasattr(self.__class__, key):
                # require default values for lambda or it evaluates all
                # variables
                # at the end of function (self._cls_suds_map[key] was evaluated
                # as the last key value in the for loop for all defined lambdas
                # Property Builder, parses _cls_suds_map to build properties:
                # custom fields:
                #    getter has parameters:
                #        suds_field_name
                #        Pylarion class related to property
                #    setter has parameters:
                #        val - the value that the property is set to
                #        suds_field_name
                #        Pylarion class related to property
                #        enum_id - the name of the enum to get from the server
                #        additional_parms - Some TestRun custom fields must
                #            instantiate an object and this parameter is
                #            populated if the constructor needs an additional
                #            parameter.
                #        enum_override - valid values that the server does not
                #                        return in validation check
                # array object fields:
                #    getter has parameters:
                #        suds_field_name
                #        Pylarion class related to property
                #    setter has parameters:
                #        val - the value that the property is set to
                #        suds_field_name
                #        Pylarion class related to property
                #        Pylarion Array class related to the property
                #        inner_field_name - the field within the Pylarion array
                # object fields:
                #    getter has parameters:
                #        suds_field_name
                #        Pylarion class related to property
                #        named_arg - argument name to pas to the constructor
                #    setter has parameters:
                #        val - the value that the property is set to
                #        suds_field_name
                #        Pylarion class related to property
                #        sync_field - the field from the instantiated class
                #                     that the attribute is set to
                #        additional_args - args needed for the obj constructor
                #        enum_id - the name of the enum to get from the server
                #        enum_override - valid values that the server does not
                #                        return in validation check
                # regular fields;
                #    use getattr and setattr
                if isinstance(self._cls_suds_map[key], dict):
                    if "is_custom" in self._cls_suds_map[key]:
                        setattr(self.__class__, key, property(
                            lambda self,
                            suds_field_name=self._cls_suds_map[key]
                                ["field_name"],
                                obj_cls=self._cls_suds_map[key].get("cls"):
                                    self._custom_getter(
                                        suds_field_name, obj_cls),
                                lambda self, val,
                                suds_field_name=self._cls_suds_map[key]
                                    ["field_name"],
                                obj_cls=self._cls_suds_map[key].get("cls"),
                                enum_id=self._cls_suds_map[key].get("enum_id"),
                                additional_parms=self._cls_suds_map[key].get(
                                    "additional_parms", {}),
                                enum_override=self._cls_suds_map[key].get(
                                    "enum_override", []):
                                    self._custom_setter(val, suds_field_name,
                                                        obj_cls, enum_id,
                                                        additional_parms,
                                                        enum_override)))
                    elif "is_array" in self._cls_suds_map[key]:
                        setattr(self.__class__, key, property(
                            lambda self,
                            suds_field_name=self._cls_suds_map[key]
                                ["field_name"],
                                obj_cls=self._cls_suds_map[key]["cls"]:
                                    self._arr_obj_getter(
                                        suds_field_name, obj_cls),
                                lambda self, val,
                                suds_field_name=self._cls_suds_map[key]
                                    ["field_name"],
                                obj_cls=self._cls_suds_map[key]["cls"],
                                arr_cls=self._cls_suds_map[key]["arr_cls"],
                                suds_arr_inner_field_name=self._cls_suds_map
                                    [key]["inner_field_name"]:
                                    self._arr_obj_setter(
                                        val, suds_field_name, obj_cls, arr_cls,
                                        suds_arr_inner_field_name)))
                    else:
                        setattr(self.__class__, key, property(
                            lambda self,
                            suds_field_name=self._cls_suds_map[key]
                                ["field_name"],
                                obj_cls=self._cls_suds_map[key]["cls"],
                                named_arg=self._cls_suds_map[key].get(
                                    "named_arg"):
                                self._obj_getter(suds_field_name, obj_cls,
                                                 named_arg),
                                lambda self, val,
                                suds_field_name=self._cls_suds_map[key]
                                ["field_name"],
                                obj_cls=self._cls_suds_map[key]["cls"],
                                sync_field=self._cls_suds_map[key].get(
                                    "sync_field"),
                                additional_parms=self._cls_suds_map[key].get(
                                    "additional_parms", {}),
                                enum_id=self._cls_suds_map[key].get("enum_id"),
                                enum_override=self._cls_suds_map[key].get(
                                    "enum_override", []):
                                self._obj_setter(
                                    val, suds_field_name, obj_cls,
                                    sync_field, additional_parms, enum_id,
                                    enum_override))
                                )
                else:
                    setattr(self.__class__, key, property(
                        # if the attribute doesn't exist in the current object
                        # return None
                        lambda self, suds_key=self._cls_suds_map[key]:
                            getattr(self._suds_object, suds_key, None),
                        lambda self, value, suds_key=self._cls_suds_map[key]:
                            setattr(self._suds_object, suds_key, value)))
# after all properties are defined set the id field to the value passed in.
        if obj_id is not None:
            setattr(self, self._id_field, obj_id)

    def _get_suds_object(self):
        """Returns the WSDL object as created by the Polarion WSDL factory"""
        if self._obj_client and self._obj_struct:
            self._suds_object = getattr(self.session, self._obj_client). \
                factory.create(self._obj_struct)
        else:
            self._suds_object = None

    def _obj_getter(self, suds_field_name, obj_cls, named_arg):
        """get function for attributes that reference an object.
        Returns the referenced object. If the WSDL attribute contains a value
        that value is given to the object as its obj_id. Classes that have an
        _id_field attribute will return only that attribute when the property
        is gotten

        Args:
            suds_field_name: the field name of the Polarion object to get
            obj_cls: the Pylarion object that the field references
            named_arg: the named parameter to pass to the constructor
        """
        if not named_arg:
                named_arg = "suds_object"
        if hasattr(self._suds_object, suds_field_name):
            args = {}
            args[named_arg] = getattr(self._suds_object, suds_field_name, None)
            obj = obj_cls(**args)
        else:
            obj = obj_cls()
        if obj._id_field:
            return getattr(obj, obj._id_field)
        else:
            return obj

    def _obj_setter(self, val, suds_field_name, obj_cls,
                    sync_field, additional_parms, enum_id, enum_override):
        """set function for attributes that reference an object. It can accept
        a string, a Pylarion object or a raw WSDL object. If a string is given,
        it is passed in to the object as its obj_id.

        Args:
            val: the value that the property is being set to
            suds_field_name: the field name of the Polarion object to set
            obj_cls: the Pylarion object that the field references
            sync_field: the field of the referenced object to set the property
            additional_parms: named parms to pass into the contructor
            enum_id: the name of the enum to get from the server
            enum_override: valid values that the server does not
                           return in validation check
        """
        if isinstance(val, basestring):
            if enum_id and val not in enum_override:
                self.check_valid_field_values(val, enum_id, {})
        if not sync_field:
            sync_field = "_suds_object"
        if isinstance(val, basestring):
            additional_parms[obj_cls._id_field] = val
            obj = obj_cls(**additional_parms)
            setattr(self._suds_object, suds_field_name,
                    getattr(obj, sync_field))
        elif isinstance(val, obj_cls):
            setattr(self._suds_object, suds_field_name,
                    getattr(val, sync_field))
        else:  # suds_object
            obj = obj_cls()
            if sync_field in obj._cls_suds_map:
                suds_sync_field = obj._cls_suds_map[sync_field]
                # if sync_field is given, the attribute will be simple
                val = getattr(val, suds_sync_field)
            setattr(self._suds_object, suds_field_name, val)

    def _arr_obj_getter(self, suds_field_name, obj_cls):
        """get function for attributes that reference an array of objects.
        The Polarion array object always has a single Python list item which
        contains a list of the WSDL objects. This function converts each WSDL
        object to its Pylarion object and returns that list

        Args:
            suds_field_name: the field name of the Polarion object to get
            obj_cls: the Pylarion object that the field references
        """
        if getattr(self._suds_object, suds_field_name, None):
            obj_lst = []
            # ArrayOf Polarion objects have a double list.
            for inst in getattr(self._suds_object, suds_field_name)[0]:
                obj_lst.append(obj_cls(suds_object=inst))
            return obj_lst
        else:
            return []

    def _arr_obj_setter(self, val, suds_field_name, obj_cls, arr_cls,
                        suds_arr_inner_field_name):
        """set function for attributes that reference an array of objects. It
        requires a single instance or list of either Pylarion or WSDL objects
        or an empty list.
        An empty list erases the attribute value.
        Otherwise it sets the attribute the value passed in.

        Args:
            val: the value that the property is set to
            suds_field_name: the field name of the Polarion object to set
            obj_cls: Pylarion class related to property
            arr_cls: Pylarion Array class related to the property
            suds_arr_inner_field_name: field name within the Pylarion array
        """
        # TODO: Still needs to be fully tested. Looks like there are some bugs.
        arr_inst = arr_cls()
        obj_inst = obj_cls()
        # obj_attach =
        if not isinstance(val,
                          (list, arr_inst.__class__,
                           arr_inst._suds_object.__class__)):
            raise PylarionLibException(
                "{0}s must be a list of {1}").format(
                    suds_field_name, obj_inst.__class__.__name__)
        elif not val:
            setattr(self._suds_object, suds_field_name, arr_inst._suds_object)
        elif isinstance(val, arr_inst._suds_object.__class__):
            setattr(self._suds_object, suds_field_name, val)
        elif isinstance(val, arr_inst.__class__):
            setattr(self._suds_object, suds_field_name, val._suds_object)
        else:
            if isinstance(val, list):
                # if str values are based in, try instantiating a class with
                # the vals and then using that list. Then continue processing
                if isinstance(val[0], basestring):
                    val = [obj_cls(item) for item in val]

                if isinstance(val[0], obj_inst._suds_object.__class__):
                    setattr(getattr(self._suds_object, suds_field_name),
                            suds_arr_inner_field_name, val)
                else:
                    setattr(self._suds_object, suds_field_name,
                            arr_inst._suds_object)
                    for item in val:
                        getattr(getattr(self._suds_object, suds_field_name),
                                suds_arr_inner_field_name).append(
                                    item._suds_object)

    def custom_obj(self):
        # This returns a custom Polarion object. It can't use the Custom class
        # as that is a child of this class.
        return self.session.test_management_client.factory.create(
            "tns4:Custom")

    def _custom_getter(self, suds_field_name, obj_cls):
        """Works with custom fields that has attributes stored differently
        if the attribute has been changed, it gets it from there.

        Args:
            suds_field_name: the field name of the Polarion object to get
            obj_cls: the Pylarion object that the field references
        """
        if suds_field_name in self._changed_fields:
            if obj_cls:
                obj = obj_cls(suds_object=self._changed_fields
                              [suds_field_name])
            else:
                obj = self._changed_fields[suds_field_name]
        elif self.uri:
            cf = self.get_custom_field(suds_field_name)
            if not cf:
                return None
            if isinstance(cf, basestring):
                obj = cf
            elif obj_cls:
                obj = obj_cls(suds_object=cf._suds_object.value)
            else:
                obj = cf.value
        else:
            obj = None
        if getattr(obj, "_id_field", None):
            return getattr(obj, obj._id_field)
        else:
            return obj

    def _custom_setter(self, val, suds_field_name, obj_cls, enum_id,
                       additional_parms, enum_override):
        """Works with custom fields that has to keep track of values and what
        changed so that on update it can also update all the custom fields at
        the same time.

        Args:
            val: the value that the property is being set to
            suds_field_name: the field name of the Polarion object to set
            obj_cls: the Pylarion object that the field references
            enum_id: contains the name of the enum to get from the server
            additional_parms: Some TestRun custom fields must instantiate an
                              object and this parameter is populated if the
                              constructor needs an additional parameter.
            enum_override: valid values that the server does not
                           return in validation check
        """
        if not val:
            self._changed_fields[suds_field_name] = None
        elif isinstance(val, basestring):
            if enum_id and val not in enum_override:
                self.check_valid_field_values(val, enum_id,
                                              additional_parms or {})
            self._changed_fields[suds_field_name] = obj_cls(val)._suds_object \
                if obj_cls else val
        elif isinstance(val, obj_cls):
            self._changed_fields[suds_field_name] = val._suds_object
        elif isinstance(val, obj_cls()._suds_object.__class__):
            self._changed_fields[suds_field_name] = val
        elif not val:
            self._changed_fields[suds_field_name] = None
        else:
            raise PylarionLibException("The value must be of type {0}.".format(
                obj_cls.__name__))
        # move the custom fields to within the object, otherwise each custom
        # field is a seperate SVN commit. testSteps, does not work unless it
        # is uploaded using the set_test_steps function.
        if suds_field_name != "testSteps":
            cf = self._suds_object.customFields[0]
            cust = self.custom_obj()
            cust.key = suds_field_name
            cust.value = self._changed_fields[suds_field_name]
            self._changed_fields.pop(suds_field_name, None)
            if cf:
                # check if the custom field already exists and modify it.
                match = filter(lambda x: x.key == suds_field_name, cf)
                if match:
                    match[0].value = cust.value
                else:
                    cf.append(cust)
                    self.custom_fields = cf
            else:
                self.custom_fields = [cust]

    def _get_file_data(self, path):
        """Method for getting attachment data that can be passed to the soap
        library. Is used by a number of child classes.

        Args:
            path: the file path

        Returns:
            base64 encoded binary data.
        """

        f = open(path, "rb")
        bdata = f.read()
        f.close()
        return base64.b64encode(bdata)

    def _verify_obj(self):
        # verifies if the object contains a suds object from the server by
        # checking if the uri field is populated. If no URI it didn't come from
        # the server
        if not getattr(self, "uri", None):
            raise PylarionLibException("There is no {0} loaded".format(
                self.__class__.__name__))

    def can_add_element_to_key(self, key):
        """Checks if the current user can add elements to the collection at
        given key of the current object.

        Args:
            key: the key of the field that contains the collection.

        Returns:
            bool

        References:
            Security.canAddElementToKey
        """
        self._verify_obj()
        return self.session.security_client.service.canAddElementToKey(
            self.uri, key)

    def can_delete_instance(self):
        """Checks if the current user can delete the current object

        Args:
            None

        Returns:
            bool

        References:
            Security.canDeleteInstance
        """
        self._verify_obj()
        return self.session.security_client.service.canDeleteInstance(self.uri)

    def can_modify_instance(self):
        """Checks if the current user can modify the current object

        Args:
            None

        Returns:
            bool

        References:
            Security.canModifyInstance
        """
        self._verify_obj()
        return self.session.security_client.service.canModifyInstance(self.uri)

    def can_modify_key(self, key):
        """Checks if the current user can modify the field with given key of
        the current object.

        Args:
            key: the key of the field that contains the collection.

        Returns:
            bool

        References:
            Security.canModifyKey
        """
        self._verify_obj()
        return self.session.security_client.service.canModifyKey(self.uri, key)

    def can_read_instance(self):
        """Checks if the current user can read the current object

        Args:
            None

        Returns:
            bool

        References:
            Security.canReadInstance
        """
        self._verify_obj()
        return self.session.security_client.service.canReadInstance(self.uri)

    def can_read_key(self, key):
        """Checks if the current user can read the field with given key of
        the current object.

        Args:
            key: the key of the field that contains the collection.

        Returns:
            bool

        References:
            Security.canReadKey
        """
        self._verify_obj()
        return self.session.security_client.service.canReadKey(self.uri, key)

    def can_remove_element_from_key(self, key):
        """Checks if the current user can remove elements from the collection
        at given key of the current object.

        Args:
            key: the key of the field that contains the collection.

        Returns:
            bool

        References:
            Security.canRemoveElementFromKey
        """
        self._verify_obj()
        return self.session.security_client.service.canRemoveElementFromKey(
            self.uri, key)

    def get_location(self):
        """Returns the location of the current object. In the context of this
        service the method should be used to get the location of a
        project(-group).

        Args:
            None

        Returns:
            location (string)

        References:
            Security.getLocationForURI
        """
        self._verify_obj()
        return self.session.security_client.service.getLocationForURI(self.uri)

    def check_valid_field_values(self, val, enum_id, additional_parms):
        if isinstance(enum_id, type):
            try:
                # try to instantiate the object with the value and additional
                # parms. If that works, it is a valid value
                enum_id(val, **additional_parms)
            except Exception:
                raise PylarionLibException(
                    "{0} is not a valid value for {1}"
                    .format(val, enum_id.__name__))
        else:
            valid_values = self.get_valid_field_values(enum_id)
            if val not in valid_values:
                raise PylarionLibException("Acceptable values for {0} are:"
                                           "{1}".format(enum_id, valid_values))

    def get_valid_field_values(self, enum_id):
        """Gets the available enumeration options.
        Uses a cache dict because the time to get valid fields from server
        is time prohibitive.

        Args:
            enum_id: The enum code to get values for

        Returns:
            Array of EnumOptions

        References:
            Tracker.getEnumOptionsForId
        """
        project_id = getattr(self, "project_id", self.default_project)
        enums = self._cache["enums"].get(enum_id)
        if not enums:
            enums = self.session.tracker_client.service. \
                getEnumOptionsForIdWithControl(project_id, enum_id)
            self._cache["enums"][enum_id] = enums
        return [enum.id for enum in enums]
