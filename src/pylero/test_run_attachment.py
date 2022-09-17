# -*- coding: utf8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from pylero.base_polarion import BasePolarion
from pylero.user import User


class TestRunAttachment(BasePolarion):
    """Object to handle the Polarion WSDL tns4:TestRunAttachment class

    Attributes:
        author (User)
        file_name (string)
        id (string)
        length (long)
        test_run_uri (SubterraURI)
        title (string)
        updated (dateTime)
        url (string)"""

    _cls_suds_map = {
        "author": {"field_name": "author", "cls": User},
        "filename": "fileName",
        "id": "id",
        "length": "length",
        "title": "title",
        "updated": "updated",
        "url": "url",
        "test_run_uri": "testRunURI",
        "_uri": "_uri",
        "_unresolvable": "_unresolvable",
    }
    _obj_client = "test_management_client"
    _obj_struct = "tns4:TestRunAttachment"


class ArrayOfTestRunAttachment(BasePolarion):
    _obj_client = "test_management_client"
    _obj_struct = "tns4:ArrayOfTestRunAttachment"
