# -*- coding: utf8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from pylero.base_polarion import BasePolarion
from pylero.text import Text


class ActivityComment(BasePolarion):
    """Object to handle the Polarion WSDL tns3:ActivityComment class

    Attributes:
        text (Text)
        time_stamp (dateאime)
        user_id (string)
    """
    _cls_suds_map = {"text":
                     {"field_name": "text",
                      "cls": Text},
                     "time_stamp": "timeStamp",
                     "user_id": "userId"}
    _obj_client = "tracker_client"
    _obj_struct = "tns3:ActivityComment"
