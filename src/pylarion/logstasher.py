# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals
import logging
import logstash
import traceback
import types
import sys
from functools import wraps

"""Logstash python class plugin, that will automagically send usage logs of all
function calls to a logstash server.

Requirements:
* python-logstash

Usage:
* install python-logstash (pip install python-logstash)
* Modify global vars
* set your variables that you want to pass in to logstash in the data dict.
* Add this file (logstasher.py) to your project.
* import LoggingMeta to your base class and add it as your class's
    __metaclass__. If you class already has a __metaclass__, you can set that
    to inherit from this one and then you gain the same functionality
* Add data elements from your class to the logstash using the
    _logstash_elements class attribute. This attribute must be in the form of a
    list of tuples, of which the first element is the data element name and the
    second is the name of the class or instance attribute. (e.g
    _logstash_elements = [("v_user_name","user_name"),
                          ("v_project_id", "project_id)]
    This attribute is evaluated during the logging session as:
        getattr(self, {attribute}, None), where self is either the instance or
        class object.
* Initialize automatically in BaseClass:
    * Add Logstash URL to your base class using _logstash_url attribute
    * Add Logstash port to your base class using _logstash_port attribute.
      This is optional. Default port is 9300
    * Add System name to your base class using _logstash_system. This is
      optional.
      Default is My Logs
* Initialize manually in your class:
    * from logstasher import LoggingMeta, init_logger
    * ...
    * init_logger(logstash_url, logstash_port)


Example:
from logstasher import LoggingMeta

class MyClass(object):
    __metaclass__ = LoggingMeta
    _logstash_elements = [("v_user_name","user_name"),
                          ("v_project_id", "project_id)]
    _logstash_url =

Note:
This works for python 2.6, in python 2.7+
    change:
    attrs[item] = classmethod(log_wrapper(attr_val.__get__(object).__func__))
    to:
    attrs[item] = classmethod(log_wrapper(attr_val.__func__))

kudos to Shai Berger <shai@platonix.com> who figured out the last piece of the
puzzle, which was how to get the class function name by passing object into the
get function.
"""

LOGSTASH_INITIALIZED = False
SYSTEM_NAME = "My Logs"
_class_elements = []
_logger = None
_logging = False


def init_logger(logstash_url, logstash_port=9300):
    global _logger
    global LOGSTASH_INITIALIZED
    _logger = logging.getLogger('python-logstash-logger')
    _logger.setLevel(logging.INFO)
    _logger.addHandler(
        logstash.LogstashHandler(
            logstash_url,
            logstash_port,
            version=1))
    LOGSTASH_INITIALIZED = True


def log_wrapper(func):
    # decorator function to log function usage.
    @wraps(func)
    def wrapper(*args, **kwargs):
        # This is supposed to act as a plugin, so it must be self-contained
        global _logging
        global _class_elements
        self = args[0]
        # Only log the initial call. any inner calls should not be logged.
        # if the logstash was not initialized above, ignore plugin.
        if _logging or not LOGSTASH_INITIALIZED:
            return func(*args, **kwargs)
        else:
            _logging = True
            data = {}
            if isinstance(self, (types.ClassType, LoggingMeta)):
                class_name = self.__name__
            else:
                class_name = self.__class__.__name__
            try:
                data["v_cls"] = class_name
                data["v_method"] = {}
                data["v_method"]["raw"] = "%s.%s" % (class_name, func.__name__)
                data["v_args"] = args
                data["v_kwargs"] = kwargs
                data["v_pyver"] = sys.version.split(" ")[0]
                for item in _class_elements:
                    # when a class method is used, some of its attributes
                    # are not available because they are uninstantiated
                    # properties.
                    if not isinstance(getattr(self, item[1], None), property):
                        data[item[0]] = getattr(self, item[1], None)
                _logger.info(SYSTEM_NAME, extra=data)
            except Exception, e:
                print(e)
            try:
                res = func(*args, **kwargs)
            except Exception, e:
                res = None
                data["v_error"] = traceback.format_exc()
                data["v_errormsg"] = e
                _logger.error(SYSTEM_NAME, extra=data)
                raise
            finally:
                _logging = False
            return res
    return wrapper


class LoggingMeta(type):
    def __new__(cls, name, bases, attrs):
        global _class_elements
        global SYSTEM_NAME
        logstash_parms = {}
        for item, attr_val in attrs.items():
            if isinstance(attr_val, types.FunctionType):
                attrs[item] = log_wrapper(attr_val)
            elif isinstance(attr_val, classmethod):
                attrs[item] = classmethod(
                    log_wrapper(attr_val.__get__(object).__func__))
            elif item == "_logstash_elements":
                _class_elements = attr_val
            elif item == "_logstash_url":
                logstash_parms["logstash_url"] = attr_val
            elif item == "_logstash_port":
                logstash_parms["logstash_port"] = attr_val
            elif item == "_logstash_system":
                SYSTEM_NAME = attr_val
        if logstash_parms:
            init_logger(**logstash_parms)
        return super(LoggingMeta, cls).__new__(cls, name, bases, attrs)
