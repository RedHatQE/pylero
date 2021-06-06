# -*- coding: utf8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from pylero.base_polarion import BasePolarion


class Text(BasePolarion):
    """Object to manage Polarion TestManagement WS tns2:Text

    Rich text object

    Attributes:
        content (str): the formatted text
        content_type (str): indication of how content is formatted
                            (eg. text/html)
        content_lossy (bool):
    """
    _cls_suds_map = {"content": "content",
                     "content_type": "type",
                     "content_lossy": "contentLossy"}
    _id_field = "content"
    _obj_client = "test_management_client"
    _obj_struct = "tns2:Text"

    def __init__(self, content=None, suds_object=None):
        super(self.__class__, self).__init__(content, suds_object)

    def _get_suds_object(self):
        super(self.__class__, self)._get_suds_object()
        # default values
        self._suds_object.type = "text/html"
        self._suds_object.contentLossy = False


class ArrayOfText(BasePolarion):
    """Object containing list of Text objects"""
    _obj_client = "test_management_client"
    _obj_struct = "tns2:ArrayOfText"
