# -*- coding: utf8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from pylero.base_polarion import BasePolarion
from pylero.user import User


class WikiPageAttachment(BasePolarion):
    """Object to handle the Polarion WSDL tns3:WikiPageAttachment class

    Attributes:
        author (User)
        file_name (string)
        wiki_page_attachment_id (string)
        length (long)
        title (string)
        updated (dateTime)
        url (string)
"""
    _cls_suds_map = {"author":
                     {"field_name": "author",
                      "cls": User},
                     "file_name": "fileName",
                     "wiki_page_attachment_id": "id",
                     "length": "length",
                     "title": "title",
                     "updated": "updated",
                     "url": "url",
                     "uri": "_uri",
                     "_unresolved": "_unresolved"}
    _obj_client = "tracker_client"
    _obj_struct = "tns3:WikiPageAttachment"


class ArrayOfWikiPageAttachment(BasePolarion):
    _obj_client = "tracker_client"
    _obj_struct = "tns3:ArrayOfWikiPageAttachment"
