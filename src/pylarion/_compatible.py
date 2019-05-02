"""
    _compatible.py

    This is a compatibility module that assists on keeping the pylarion
    Library compatible with python 2.x and python 3.x.

    :copyright: (c) 2017 Red Hat, Inc.
    :license: GPLv3, see LICENSE for more details.
"""

try:
    import __builtin__ as builtins
except ImportError:
    import builtins

try:
    from builtins import object
except ImportError:
    from __builtin__ import object

try:
    from builtins import classmethod
except ImportError:
    from __builtin__ import classmethod

try:
    from builtins import range
except ImportError:
    from __builtin__ import range

try:
    from builtins import str
except ImportError:
    from __builtin__ import str

try:
    string_types = (str, unicode)
except NameError:
    string_types = (str, )

try:
    from __builtin__ import basestring
except ImportError:
    basestring = (str, bytes)

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse

try:
    from ConfigParser import ConfigParser
except ImportError:
    from configparser import ConfigParser

try:
    from ConfigParser import SafeConfigParser
except ImportError:
    from configparser import SafeConfigParser