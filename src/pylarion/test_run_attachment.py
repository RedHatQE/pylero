# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals
import pylarion.base_polarion as bp
import pylarion.user as u


class TestRunAttachment(bp.BasePolarion):
    '''Object to manage Polarion TestManagement WS tns4:TestRunAttachment'''
    _cls_suds_map = {"author": {"field_name": "author", "cls": u.User},
                     "filename": "fileName", "id": "id",
                     "length": "length", "title": "title",
                     "updated": "updated", "url": "url",
                     "test_run_uri": "testRunURI", "_uri": "_uri",
                     "_unresolvable": "_unresolvable"}
    _obj_client = "test_management_client"
    _obj_struct = "tns4:TestRunAttachment"


class ArrayOfTestRunAttachment(bp.BasePolarion):
    _obj_client = "test_management_client"
    _obj_struct = "tns4:ArrayOfTestRunAttachment"
