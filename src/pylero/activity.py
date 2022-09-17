# -*- coding: utf8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from pylero.base_polarion import BasePolarion
from pylero.text import Text


class Activity(BasePolarion):
    """Object to handle the Polarion WSDL tns3:Activity class

    Attributes:
        activity_custom_values (list of ActivityCustomValueEntry)
        comments (list of ActivityComment)
        context_id (ContextId)
        global_id (string)
        activity_id (string)
        info (Text)
        prefix (string)
        resource_locations (list)
        source_id (string)
        timestamp (dateTime)
        type (string)
        user_id (string)"""

    _cls_suds_map = {
        "activity_custom_values": "activity_custom_values",
        "comments": "comments",  # array of ActivityComment
        "global_id": "globalId",
        "activity_id": "id",
        "info": {"field_name": "info", "cls": Text},
        "prefix": "prefix",
        "resource_locations": "resourceLocations",
        "source_id": "sourceId",
        "timestamp": "timestamp",
        "type": "type",
        "user_id": "userId",
        "uri": "_uri",
        "_unresolved": "_unresolved",
    }
    _obj_client = "tracker_client"
    _obj_struct = "tns3:Activity"
