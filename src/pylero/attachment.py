# -*- coding: utf8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from pylero.base_polarion import BasePolarion
from pylero.user import User


class Attachment(BasePolarion):
    """Object to handle the Polarion WSDL tns5:Attachment class

    Attributes:
        author (User)
        file_name (string)
        attachment_id (string)
        length (long)
        title (string)
        updated (dateTime)
        url (string)"""

    _cls_suds_map = {
        "author": {"field_name": "author", "cls": User},
        "file_name": "fileName",
        "attachment_id": "id",
        "length": "length",
        "title": "title",
        "updated": "updated",
        "url": "url",
        "uri": "_uri",
        "_unresolved": "_unresolved",
    }
    _obj_client = "builder_client"
    _obj_struct = "tns5:Attachment"


class ArrayOfAttachment(BasePolarion):
    _obj_client = "builder_client"
    _obj_struct = "tns5:ArrayOfAttachment"
