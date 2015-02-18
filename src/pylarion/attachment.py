# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals
import pylarion.base_polarion as bp
import pylarion.user as u


class Attachment(bp.BasePolarion):
    """Object to handle the Polarion WSDL tns5:Attachment class

    Attributes (for specific details, see Polarion):
        author (User)
        file_name (string)
        attachment_id (string)
        length (long)
        title (string)
        updated (dateTime)
        url (string)
"""
    _cls_suds_map = {"author": {"field_name": "author", "cls": u.User},
                     "file_name": "fileName",
                     "attachment_id": "id",
                     "length": "length",
                     "title": "title",
                     "updated": "updated",
                     "url": "url",
                     "uri": "_uri",
                     "_unresolved": "_unresolved"}
    _obj_client = "builder_client"
    _obj_struct = "tns5:Attachment"


class ArrayOfAttachment(bp.BasePolarion):
    _obj_client = "builder_client"
    _obj_struct = "tns5:ArrayOfAttachment"
