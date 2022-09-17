# -*- coding: utf8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from pylero.base_polarion import BasePolarion


class ActivitySource(BasePolarion):
    """Object to handle the Polarion WSDL tns3:ActivitySource class

    Attributes:
        activity_source_id (string)
        prefix (string)
        types (ArrayOf_xsd_string)"""

    _cls_suds_map = {
        "activity_source_id": "id",
        "prefix": "prefix",
        "types": "types",
        "uri": "_uri",
        "_unresolved": "_unresolved",
    }
    _obj_client = "tracker_client"
    _obj_struct = "tns3:ActivitySource"
