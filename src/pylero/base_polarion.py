# -*- coding: utf8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import base64
import copy
import os
import re
from functools import wraps
from getpass import getpass

import suds
from pylero._compatible import basestring
from pylero._compatible import classmethod
from pylero._compatible import ConfigParser
from pylero.exceptions import PyleroLibException
from pylero.server import Server


# classproperty is a property that works on the class level
class ClassProperty(property):
    """Returns a classmethod as the getter so that the property can be used as
    a class property. This is needed so that the property can be set for all
    child objects. This project currently has no need of a setter or deleter.
    """

    def __get__(self, instance, cls):
        return classmethod(self.fget).__get__(instance, cls)()


class Configuration(object):
    pkgdir = os.path.dirname(__file__)
    GLOBAL_CONFIG = "%s/pylero.cfg" % pkgdir
    LOCAL_CONFIG = os.path.expanduser("~") + "/.pylero"
    CURDIR_CONFIG = ".pylero"
    CONFIG_SECTION = "webservice"
    # Look at ConfigParser
    # https://docs.python.org/2.6/library/configparser.html

    def __init__(self):
        defaults = {"cachingpolicy": "0", "timeout": "120"}
        config = ConfigParser(defaults)
        # Check for existence of config file and config_section
        if not config.read(
            [self.GLOBAL_CONFIG, self.LOCAL_CONFIG, self.CURDIR_CONFIG]
        ) or not config.has_section(self.CONFIG_SECTION):
            # Check for mandatory environ variables if config file is not found
            if not all(
                os.environ.get(item)
                for item in (
                    "POLARION_URL",
                    "POLARION_REPO",
                    "POLARION_USERNAME",
                    "POLARION_PASSWORD",
                    "POLARION_PROJECT",
                )
            ):
                raise PyleroLibException(
                    "The config files/ENV vars do not "
                    "exist or are not of the correct "
                    "format. Valid files are: {0}, {1} "
                    "or {2}".format(
                        self.GLOBAL_CONFIG, self.LOCAL_CONFIG, self.CURDIR_CONFIG
                    )
                )
        self.server_url = os.environ.get("POLARION_URL") or config.get(
            self.CONFIG_SECTION, "url"
        )
        self.repo = os.environ.get("POLARION_REPO") or config.get(
            self.CONFIG_SECTION, "svn_repo"
        )
        self.login = os.environ.get("POLARION_USERNAME") or config.get(
            self.CONFIG_SECTION, "user"
        )
        self.pwd = os.environ.get("POLARION_PASSWORD") or config.get(
            self.CONFIG_SECTION, "password"
        )

        try:
            self.timeout = os.environ.get("POLARION_TIMEOUT") or config.get(
                self.CONFIG_SECTION, "timeout"
            )
        except Exception:
            self.timeout = config.defaults["timeout"]

        try:
            self.timeout = int(self.timeout)
        except ValueError:
            raise PyleroLibException(
                "The timeout value in the config" " file must be an integer"
            )
        self.proj = os.environ.get("POLARION_PROJECT") or config.get(
            self.CONFIG_SECTION, "default_project"
        )
        try:
            self.cert_path = os.environ.get("POLARION_CERT_PATH") or config.get(
                self.CONFIG_SECTION, "cert_path"
            )
        except Exception:
            self.cert_path = None

        if not (self.server_url and self.login and self.proj):
            raise PyleroLibException(
                "The config files must contain "
                "valid values for: url, user, "
                "password and default_project"
            )

        try:
            self.disable_manual_auth = os.environ.get(
                "POLARION_DISABLE_MANUAL_AUTH"
            ) or config.getboolean(self.CONFIG_SECTION, "disable_manual_auth")
        except Exception:
            self.disable_manual_auth = False


class Connection(object):
    """Creates a Polarion session as a class method, so that it is used for all
    objects inherited by BasePolarion.
    The url, repo, user and password are read from config files, which are
    located either the current directory ./pylero, the user's dir ~/.pylero
    or the Library config dir LIBDIR/pylero.cfg
    These can also be overridden with the following environment variables:
    POLARION_URL
    POLARION_REPO
    POLARION_USERNAME
    POLARION_PASSWORD
    POLARION_TIMEOUT
    POLARION_PROJECT
    """

    connected = False
    session = None
    password_retries = 3

    @classmethod
    def session(cls):
        if not cls.connected:
            cfg = Configuration()
            # if the password is not supplied in the config file, ask the user
            # for it
            if not cfg.pwd:
                cfg.pwd = getpass("Password not in config file.\nEnter Password:")
            while not cls.connected and cls.password_retries:
                try:
                    srv = Server(
                        cfg.server_url,
                        cfg.login,
                        cfg.pwd,
                        timeout=cfg.timeout,
                        cert_path=cfg.cert_path,
                    )
                    cls.session = srv.session()
                    cls.session._login()
                    cls.connected = True
                except suds.WebFault as e:
                    # If we couldn't connect its because the user has typed the
                    # wrong password. So we keep asking for password till we
                    # are successfully connected
                    if (
                        "com.polarion.platform.security."
                        "AuthenticationFailedException" in e.fault.faultstring
                    ):
                        if cfg.disable_manual_auth:
                            raise PyleroLibException(
                                "Manual authentication " "is disabled"
                            )
                        cfg.pwd = getpass("Invalid Password.\nEnter Password:")
                        cls.password_retries -= 1
                    else:
                        raise
            if not cls.password_retries:
                raise PyleroLibException(
                    "Unable to establish pylero session "
                    "due to 3 incorrect login attempts"
                )
            cls.session.default_project = cfg.proj
            cls.session.user_id = cfg.login
            cls.session.password = cfg.pwd
            cls.session.repo = cfg.repo
            # must use try/except instead of or because the config file
            # may return a non empty value, such as " "
        return cls.session


def tx_wrapper(func):
    # decorator function to run specific functions in.
    # Because they have multiple modifying stmts, they should be run
    # in a transaction. It first checks if it is already in a tx and if
    # not, it starts one itself.
    @wraps(func)
    def inner(*args, **kwargs):
        # the first object is the instance or class object.
        self = args[0]
        new_tx = False
        try:
            if not self.session.tx_in():
                self.session.tx_begin()
                new_tx = True
            res = func(*args, **kwargs)
            if new_tx:
                self.session.tx_commit()
            return res
        except (suds.WebFault, PyleroLibException, Exception):
            if new_tx and self.session.tx_in():
                self.session.tx_rollback()
            raise

    return inner


class BasePolarion(object):
    """BasePolarion is the parent class for all the WSDL Polarion objects that
    are published. Using the _cls_suds_map, the class creates a property for
    each attribute so that any access of the object attribute, will access the
    WSDL object that is contained by it.

    Attributes:
        _cls_suds_map (dict): maps the Polarion attribute names to the Pylero
                        attribute names. Attributes that reference either
                        objects or an array of objects have the properties
                        relate to the relationship meaning that accessing the
                        property will give access to the object or list of
                        objects.
        _id_field (str): the field that represents an id field, used in the
                         child class's constructor. when a child's class
                         defines the field it allows this constructor to accept
                         an obj_id as a parameter
        _obj_client (str): The Polarion client child's WSDL object is
                           defined by
        _obj_struct (str): The data type defined by the WSDL library. The
                           structure of the datatype is tnsX:ObjectName, the X
                           is per datatype and has no default.
        session (Session): The Polarion Session object, initialized by the
                           Connection class. This attribute connects to the
                           server one time per session, no matter how many
                           objects are instantiated.
        default_project (str): The user's default project, to be used when
                          project_id is needed and there is none given
    """

    _cls_suds_map = {}
    _id_field = None
    _obj_client = None
    _obj_struct = None
    _session = None
    _default_project = None
    _cache = {"enums": {}, "custom_field_types": {}, "projects": {}}
    REGEX_PROJ = r"/default/(.*)\$"
    # The id in the uri is always after the last }, at times there are multiple
    REGEX_ID = ".+}(.*)$"
    # The URI_STRUCT can be overridden in a child class when needed (for
    # example, Documents). Also if there is need for a replace in the child
    # class the URI_ID lambda attributes should be overridden
    URI_STRUCT = "subterra:data-service:objects:/default/" "%(project)s${%(obj)s}%(id)s"
    # must wrap lambda with classmethod so it can be used as such
    URI_ID_GET_REPLACE = classmethod(lambda cls, x: x)
    URI_ID_SET_REPLACE = classmethod(lambda cls, x: x)

    @ClassProperty
    def session(cls):
        # Uses a class property for the session, so that the library doesn't
        # connect to the server until the library is actually used.
        if BasePolarion._session:
            return BasePolarion._session
        else:
            # For some reason, using the cls attribute makes it into a class
            # attribute for the specific class but not for all the other
            # Pylero objects.
            BasePolarion._session = Connection.session()
            BasePolarion._default_project = cls._session.default_project
            BasePolarion.logged_in_user_id = cls._session.user_id
            # stores password in the session so it can be used for direct svn
            # operations
            BasePolarion.repo = cls._session.repo
            return BasePolarion._session

    @ClassProperty
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
        return the list of its Polarion attribute name. If the field is a
        custom field, it adds the customFields. qualifier before the fieldname
        as is required for searching custom fields.

        Args:
            fields - list of fields to convert. If it is not a list, it
            converts it to one first. default: []
        """
        p_fields = []
        if fields:
            if not isinstance(fields, list):
                fields = [fields]
            # convert given fields to Polarion fields
            p_fields = [
                "%s%s"
                % (
                    "customFields."
                    if isinstance(cls._cls_suds_map[x], dict)
                    and cls._cls_suds_map[x].get("is_custom", False)
                    else "",
                    cls._cls_suds_map[x]
                    if not isinstance(cls._cls_suds_map[x], dict)
                    else cls._cls_suds_map[x]["field_name"],
                )
                for x in fields
            ]
            # Omit 'URIs' and 'URI' from URIFields
            p_fields = [(x.replace("URIs", "").replace("URI", "")) for x in p_fields]
        return p_fields

    @classmethod
    def get_global_roles(cls):
        r"""Returns all global roles.

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
            permission, project_id
        )

    def __init__(self, obj_id=None, suds_object=None):
        # cls_suds_map must be available for some parameters on the class
        # level, but gets changed on the instance level and those changes
        # should not be accessible to other instances. This is the reason
        # for overwriting it as an instance attribute.
        self._cls_suds_map = copy.deepcopy(self._cls_suds_map)
        # _fix_circular_refs is a function that allows objects to contain
        # circular references by applying the reference only after the class
        # has been instantiated. Some objects contain references to themselves,
        # for example a parent attribute.
        if hasattr(self, "_fix_circular_refs"):
            self._fix_circular_refs()
        # if _id_field has not been set in the child class, the obj_id field
        # cannot be passed as a parameter.
        if obj_id and not self._id_field:
            raise PyleroLibException(
                "{0} only accepts a suds object, not an obj_id".format(
                    self.__class__.__name
                )
            )
        if suds_object:
            self._suds_object = suds_object
        else:
            self._get_suds_object()
        # initialize all instance attributes as properties
        # check if the property already exists. If so, use existing.
        for key in list(self._cls_suds_map.keys()):
            if not hasattr(self.__class__, key):
                # require default values for lambda or it evaluates all
                # variables
                # at the end of function (self._cls_suds_map[key] was evaluated
                # as the last key value in the for loop for all defined lambdas
                # Property Builder, parses _cls_suds_map to build properties:
                # custom fields:
                #    getter has parameters:
                #        field_name
                #    setter has parameters:
                #        val: the value that the property is set to
                #        field_name
                # array object fields:
                #    getter has parameters:
                #        field_name
                #    setter has parameters:
                #        val: the value that the property is set to
                #        field_name
                # object fields:
                #    getter has parameters:
                #        field_name
                #    setter has parameters:
                #        val: the value that the property is set to
                #        field_name
                # regular fields;
                #    use getattr and setattr
                if isinstance(self._cls_suds_map[key], dict):
                    if "is_custom" in self._cls_suds_map[key]:
                        setattr(
                            self.__class__,
                            key,
                            property(
                                lambda self, field_name=key: self._custom_getter(
                                    field_name
                                ),
                                lambda self, val, field_name=key: self._custom_setter(
                                    val, field_name
                                ),
                            ),
                        )
                    elif "is_array" in self._cls_suds_map[key]:
                        setattr(
                            self.__class__,
                            key,
                            property(
                                lambda self, field_name=key: self._arr_obj_getter(
                                    field_name
                                ),
                                lambda self, val, field_name=key: self._arr_obj_setter(
                                    val, field_name
                                ),
                            ),
                        )
                    else:
                        setattr(
                            self.__class__,
                            key,
                            property(
                                lambda self, field_name=key: self._obj_getter(
                                    field_name
                                ),
                                lambda self, val, field_name=key: self._obj_setter(
                                    val, field_name
                                ),
                            ),
                        )
                else:
                    setattr(
                        self.__class__,
                        key,
                        property(
                            # if the attribute doesn't exist in the current object
                            # return None
                            lambda self, suds_key=self._cls_suds_map[key]: getattr(
                                self._suds_object, suds_key, None
                            ),
                            lambda self, value, suds_key=self._cls_suds_map[
                                key
                            ]: self._regular_setter(value, suds_key),
                        ),
                    )
        # after all properties are defined set the id field to the value passed in.
        if obj_id is not None:
            setattr(self, self._id_field, obj_id)

    def _get_suds_object(self):
        """Returns the WSDL object as created by the Polarion WSDL factory"""
        if self._obj_client and self._obj_struct:
            self._suds_object = getattr(self.session, self._obj_client).factory.create(
                self._obj_struct
            )
        else:
            self._suds_object = None

    def _obj_getter(self, field_name):
        """get function for attributes that reference an object.
        Returns the referenced object. If the WSDL attribute contains a value
        that value is given to the object as its obj_id. Classes that have an
        _id_field attribute will return only that attribute when the property
        is gotten

        Args:
            field_name: the field name of the Polarion object to get
        """
        csm = self._cls_suds_map[field_name]
        named_arg = csm.get("named_arg", "suds_object")
        suds_field_val = getattr(self._suds_object, csm.get("field_name", ""), None)
        cls_obj = csm["cls"]
        if suds_field_val:
            if named_arg == "uri" and cls_obj._id_field:
                if suds_field_val:
                    id_re = re.search(self.REGEX_ID, suds_field_val)
                    if id_re:
                        return cls_obj.URI_ID_GET_REPLACE(id_re.group(1))
            else:
                args = {}
                args[named_arg] = suds_field_val
                obj = cls_obj(**args)
        else:
            obj = cls_obj()
        if cls_obj._id_field:
            return getattr(obj, obj._id_field)
        else:
            return obj

    def _obj_setter(self, val, field_name):
        """set function for attributes that reference an object. It can accept
        a string, a Pylero object or a raw WSDL object. If a string is given,
        it is passed in to the object as its obj_id.

        Args:
            val: the value that the property is being set to
            field_name: the field name of the Polarion object to set
        """
        csm = self._cls_suds_map[field_name]
        suds_field_name = csm["field_name"]
        enum_id = csm.get("enum_id")
        enum_override = csm.get("enum_override", [])
        sync_field = csm.get("sync_field")
        obj_cls = csm.get("cls")
        # deepcopy so that changes do not stick
        add_parms = copy.deepcopy(csm.get("additional_parms", {}))
        if isinstance(val, basestring):
            val = self._check_encode(val)
            if enum_id and val not in enum_override:
                self.check_valid_field_values(
                    val,
                    enum_id,
                    {},
                    self._wi_type if hasattr(self, "_wi_type") else None,
                )
        if not sync_field:
            sync_field = "_suds_object"
        if isinstance(val, basestring) or val is None:
            add_parms[obj_cls._id_field] = val
            obj = obj_cls(**add_parms)
            setattr(self._suds_object, suds_field_name, getattr(obj, sync_field))
        elif isinstance(val, obj_cls):
            setattr(self._suds_object, suds_field_name, getattr(val, sync_field))
        elif isinstance(val, obj_cls()._suds_object.__class__):
            obj = obj_cls()
            if sync_field in obj._cls_suds_map:
                suds_sync_field = obj._cls_suds_map[sync_field]
                # if sync_field is given, the attribute will be simple
                val = getattr(val, suds_sync_field)
            setattr(self._suds_object, suds_field_name, val)
        else:
            raise PyleroLibException("the value {0} is not a valid type".format(val))

    def _arr_obj_getter(self, field_name):
        """get function for attributes that reference an array of objects.
        The Polarion array object always has a single Python list item which
        contains a list of the WSDL objects. This function converts each WSDL
        object to its Pylero object and returns that list

        Args:
            field_name: the field name of the Polarion object to get
        """
        csm = self._cls_suds_map[field_name]
        if getattr(self._suds_object, csm["field_name"], None):
            obj_lst = []
            project_id = getattr(self._suds_object, "project", None)
            if project_id:
                project_id = project_id["id"]
            # ArrayOf Polarion objects have a double list.
            for inst in getattr(self._suds_object, csm["field_name"])[0]:
                csm_obj = csm["cls"](suds_object=inst)
                if getattr(csm_obj, "project_id", None) and project_id:
                    setattr(csm_obj, "project_id", project_id)
                obj_lst.append(csm_obj)
            return obj_lst
        else:
            return []

    def _arr_obj_setter(self, val, field_name):
        """set function for attributes that reference an array of objects. It
        requires a single instance or list of either Pylero or WSDL objects
        or an empty list.
        An empty list erases the attribute value.
        Otherwise it sets the attribute the value passed in.

        Args:
            val: the value that the property is set to
            field_name: the field name of the Polarion object to set
        """
        # TODO: Still needs to be fully tested. Looks like there are some bugs.
        csm = self._cls_suds_map[field_name]
        arr_inst = csm.get("arr_cls")()
        obj_inst = csm.get("cls")()
        # obj_attach =
        if not isinstance(
            val, (list, arr_inst.__class__, arr_inst._suds_object.__class__)
        ):
            raise PyleroLibException("{0}s must be a list of {1}").format(
                csm["field_name"], obj_inst.__class__.__name__
            )
        elif not val:
            setattr(self._suds_object, csm["field_name"], arr_inst._suds_object)
        elif isinstance(val, arr_inst._suds_object.__class__):
            setattr(self._suds_object, csm["field_name"], val)
        elif isinstance(val, arr_inst.__class__):
            setattr(self._suds_object, csm["field_name"], val._suds_object)
        else:
            if isinstance(val, list):
                # if str values are based in, try instantiating a class with
                # the vals and then using that list. Then continue processing
                if isinstance(val[0], basestring):
                    val[0] = self._check_encode(val[0])
                    val = [csm["cls"](item) for item in val]

                if isinstance(val[0], obj_inst._suds_object.__class__):
                    setattr(
                        getattr(self._suds_object, csm["field_name"]),
                        csm["inner_field_name"],
                        val,
                    )
                else:
                    setattr(self._suds_object, csm["field_name"], arr_inst._suds_object)
                    for item in val:
                        getattr(
                            getattr(self._suds_object, csm["field_name"]),
                            csm["inner_field_name"],
                        ).append(item._suds_object)

    def custom_obj(self):
        # This returns a custom Polarion object. It can't use the Custom class
        # as that is a child of this class.
        return self.session.test_management_client.factory.create("tns4:Custom")

    def custom_array_obj(self):
        # This returns a custom Polarion object. It can't use the Custom class
        # as that is a child of this class.
        return self.session.test_management_client.factory.create("tns4:ArrayOfCustom")

    def _custom_getter(self, field_name):
        """Works with custom fields that has attributes stored differently
        then regular attributes. It first checks if there is a value in the
        local copy, which may have already been modified by the user. If not,
        it checks the server for a value.

        test_steps do not work like all other custom fields, and therefore
        require specific code. Its values are not saved in the local object.

        Args:
            field_name: the field name of the Polarion object to get
        """
        csm = self._cls_suds_map[field_name]
        if field_name == "test_steps":
            if self._changed_fields.get("testSteps"):
                return csm["cls"](suds_object=self._changed_fields.get("testSteps"))
            else:
                test_steps = self.get_test_steps()
                if test_steps:
                    return test_steps
        else:
            if ("customFields" not in self._suds_object) or (
                not self._suds_object.customFields
            ):
                self._suds_object.customFields = self.custom_array_obj()
            cf = self._suds_object.customFields[0]
            custom_fld = None
            if cf:
                # check if the custom field already exists and modify it.
                match = [x for x in cf if x.key == csm["field_name"]]
                if match:
                    custom_fld = match[0]
            if not custom_fld and self.uri:
                custom_fld = self.get_custom_field(csm["field_name"])._suds_object
            if custom_fld:
                if isinstance(custom_fld, basestring):
                    obj = custom_fld
                elif csm.get("is_array"):
                    obj = []
                    # ArrayOf Polarion objects have a double list.
                    if custom_fld.value:
                        for inst in custom_fld.value[0]:
                            if csm["cls"]._cls_inner._id_field:
                                item_inst = csm["cls"]._cls_inner(suds_object=inst)
                                obj.append(getattr(item_inst, item_inst._id_field))
                            else:
                                obj.append(csm["cls"]._cls_inner(suds_object=inst))
                elif csm.get("cls"):
                    obj = csm["cls"](suds_object=custom_fld.value)
                else:
                    obj = custom_fld.value
                if getattr(obj, "_id_field", None):
                    return getattr(obj, obj._id_field)
                else:
                    return obj
            else:
                return None

    def _custom_setter(self, val, field_name):
        """Works with custom fields that has to keep track of values and what
        changed so that on update it can also update all the custom fields at
        the same time.

        Args:
            val: the value that the property is being set to
            field_name: the field name of the Polarion object to set
        """
        csm = self._cls_suds_map[field_name]
        if field_name == "test_steps":
            if not val:
                self._changed_fields[csm["field_name"]] = None
            elif isinstance(val, csm["cls"]):
                self._changed_fields[csm["field_name"]] = val._suds_object
            elif isinstance(val, csm["cls"]()._suds_object.__class__):
                self._changed_fields[csm["field_name"]] = val
            else:
                raise PyleroLibException(
                    "The value must be a {0}".format(csm["cls"].__name__)
                )
        # move the custom fields to within the object, otherwise each custom
        # field is a seperate SVN commit. testSteps, does not work unless it
        # is uploaded using the set_test_steps function.
        else:
            cust = self.custom_obj()
            cust.key = csm["field_name"]
            if val is None:
                cust.value = None
            elif (not csm.get("cls") or isinstance(val, basestring)) and not csm.get(
                "is_array"
            ):
                # if there is no cls specified, val can be a bool, int, ...
                # if val is a string, it may be used to instantiate the class
                if isinstance(val, basestring):
                    val = self._check_encode(val)
                if csm.get("enum_id") and val not in csm.get("enum_override", []):
                    # uses deepcopy, to not affect other instances of the class
                    additional_parms = copy.deepcopy(csm.get("additional_parms", {}))
                    self.check_valid_field_values(
                        val, csm.get("enum_id"), additional_parms, csm.get("control")
                    )
                cust.value = csm["cls"](val)._suds_object if csm.get("cls") else val
            elif csm.get("is_array"):
                if not isinstance(val, list):
                    raise PyleroLibException("value must be a list")
                if csm.get("enum_id"):
                    cust.value = csm["cls"]()._suds_object
                    for i in val:
                        if i not in csm.get("enum_override", []):
                            # uses deepcopy, to not affect other instances
                            # of the class
                            additional_parms = copy.deepcopy(
                                csm.get("additional_parms", {})
                            )
                            self.check_valid_field_values(
                                i,
                                csm.get("enum_id"),
                                additional_parms,
                                self._wi_type if hasattr(self, "_wi_type") else None,
                            )
                        cust.value[0].append(csm["cls"]._cls_inner(i)._suds_object)

            elif isinstance(val, csm["cls"]):
                cust.value = val._suds_object
            elif isinstance(val, csm["cls"]()._suds_object.__class__):
                cust.value = val
            else:
                raise PyleroLibException(
                    "The value must be of type {0}.".format(csm["cls"].__name__)
                )
            if ("customFields" not in self._suds_object) or (
                not self._suds_object.customFields
            ):
                self._suds_object.customFields = self.custom_array_obj()
            cf = self._suds_object.customFields[0]
            if cf:
                # check if the custom field already exists and modify it.
                match = [x for x in cf if x.key == csm["field_name"]]
                if match:
                    match[0].value = cust.value
                else:
                    cf.append(cust)
                    self._custom_fields = cf
            else:
                self._custom_fields = [cust]

    def _regular_setter(self, value, field_name):
        """This setter is used for any attributes that are not Polarion object
        data types. If the attribute type is a string, then it validates it
        using the check_encode function

        Args:
            value (string): the value that the property is being set to
            field_name: the field name of the Polarion object to set
        """
        if isinstance(value, basestring):
            value = self._check_encode(value)
        setattr(self._suds_object, field_name, value)

    def _check_encode(self, val):
        """Validate @val is a UTF-8 because Polarion doesn't support not
        UTF-8 characters. The only use case that is not taken into account
        is when an attribute is set directly with a SUDS object. The users
        have no way of calling this function in this case.

        Args:
        val (string): the value that the property is being set to
        """
        try:
            if not isinstance(val, type("")):
                val = val.decode("utf-8")
            # replace chr(160) with space
            return val.replace("\xa0", " ")
        except UnicodeError as err:
            raise PyleroLibException(
                "String must be UTF-8 encoded. The following error was "
                "raised when converting it to unicode: {0}".format(err)
            )

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
        bencode = base64.b64encode(bdata)
        # Effectively turns in Python3 String
        try:
            # Python2
            return bencode.encode("utf8")
        except AttributeError:
            # Python3
            return bencode.decode("utf8")

    def _verify_obj(self):
        # verifies if the object contains a suds object from the server by
        # checking if the uri field is populated. If no URI it didn't come from
        # the server
        if not getattr(self, "uri", None):
            raise PyleroLibException(
                "There is no {0} loaded".format(self.__class__.__name__)
            )

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
        return self.session.security_client.service.canAddElementToKey(self.uri, key)

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
            self.uri, key
        )

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

    def check_valid_field_values(self, val, enum_id, additional_parms, control=None):
        """verifies id the value passed in is valid for the enum or object
        passed in. for example, if we want to see if a valid user is given,
        this will try to instantiate the User class with the given parameter
        and additional parms. If it fails, it is not a valid value.

        Args:
            val: the value you want to set it to.
            enum_id: the enumeration or object to validate against
            additional_parms (dict): parms needed to instantiate class passed
                                    in as enum_id
            control: the control key for the enumeration. default:None
        """
        if isinstance(enum_id, type):
            try:
                # try to instantiate the object with the value and additional
                # parms. If that works, it is a valid value
                enum_id(val, **additional_parms)
            except Exception:
                raise PyleroLibException(
                    "{0} is not a valid value for {1}".format(val, enum_id.__name__)
                )
        else:
            valid_values = self.get_valid_field_values(enum_id, control)
            if val not in valid_values:
                raise PyleroLibException(
                    "Acceptable values for {0} are:" "{1}".format(enum_id, valid_values)
                )

    def get_valid_field_values(self, enum_id, control=None):
        """Gets the available enumeration options.
        Uses a cache dict because the time to get valid fields from server
        is time prohibitive.

        Args:
            enum_id: The enum code to get values for
            control: the control key for the enumeration. default:None

        Returns:
            Array of EnumOptions

        References:
            Tracker.getEnumOptionsForId
        """
        project_id = getattr(self, "project_id", None) or self.default_project
        enum_base = self._cache["enums"].get(enum_id)
        enums = None
        if enum_base:
            enums = enum_base.get(control)
        if not enums:
            enums = self.session.tracker_client.service.getEnumOptionsForIdWithControl(
                project_id, enum_id, control
            )
            self._cache["enums"][enum_id] = {}
            self._cache["enums"][enum_id][control] = enums
        # the _cache contains _suds_object, so the id attribute is used.
        return [enum.id for enum in enums]

    def reload(self):
        """Reloads the object with data from the server.
        This function is useful if the data on the server changed or if a
        data changing function was called (such as TestRun.add_attachment)

        Notes:
            This will overwrite any unsaved data in the object.
        Args:
            None
        Returns:
            None
        """

        if getattr(self, "uri", None):
            obj = self.__class__(uri=self.uri)
            self._suds_object = obj._suds_object
