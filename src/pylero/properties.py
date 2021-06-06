# -*- coding: utf8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from pylero.base_polarion import BasePolarion


class Properties(BasePolarion):
    """Object to handle the Polarion WSDL tns4:Properties class

    Attributes:
        property (property)
"""
    _cls_suds_map = {"property": "property",
                     "uri": "_uri",
                     "_unresolved": "_unresolved"}
    _obj_client = "builder_client"
    _obj_struct = "tns4:Properties"
