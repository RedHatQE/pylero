# -*- coding: utf8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from pylero.base_polarion import BasePolarion


class Property(BasePolarion):
    """Object to handle the Polarion WSDL tns4:property class

    Attributes:
        key (string)
        value (string)"""

    _cls_suds_map = {
        "key": "key",
        "value": "value",
        "uri": "_uri",
        "_unresolved": "_unresolved",
    }
    _obj_client = "builder_client"
    _obj_struct = "tns4:property"
