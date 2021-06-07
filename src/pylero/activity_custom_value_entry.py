# -*- coding: utf8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from pylero.activity_custom_value import ActivityCustomValue
from pylero.base_polarion import BasePolarion


class ActivityCustomValueEntry(BasePolarion):
    """Object to handle the Polarion WSDL tns3:ActivityCustomValueEntry class

    Attributes:
        custom_values (ActivityCustomValue)
        key (string)
"""
    _cls_suds_map = {"custom_values":
                     {"field_name": "customValues",
                      "cls": ActivityCustomValue},
                     "key": "key",
                     "uri": "_uri",
                     "_unresolved": "_unresolved"}
    _obj_client = "tracker_client"
    _obj_struct = "tns3:ActivityCustomValueEntry"
