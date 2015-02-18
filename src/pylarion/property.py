# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals
import pylarion.base_polarion as bp


class Property(bp.BasePolarion):
    """Object to handle the Polarion WSDL tns4:property class

    Attributes (for specific details, see Polarion):
        key (string)
        value (string)
"""
    _cls_suds_map = {"key": "key",
                     "value": "value",
                     "uri": "_uri",
                     "_unresolved": "_unresolved"}
    _obj_client = "builder_client"
    _obj_struct = "tns4:property"
