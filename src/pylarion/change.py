# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals
import pylarion.base_polarion as bp
import pylarion.field_diff as fd


class Change(bp.BasePolarion):
    """Object to handle the Polarion WSDL tns3:Change class

    Attributes (for specific details, see Polarion):
        creation (boolean)
        date (dateTime)
        diffs (ArrayOf_tns3_FieldDiff)
        empty (boolean)
        invalid (boolean)
        revision (string)
        user (string)
"""
    _cls_suds_map = {"creation": "creation",
                     "date": "date",
                     "diffs": "diffs",
                     "empty": "empty",
                     "invalid": "invalid",
                     "revision": "revision",
                     "user": "user",
                     "uri": "_uri",
                     "_unresolved": "_unresolved"}
    _obj_client = "tracker_client"
    _obj_struct = "tns3:Change"
