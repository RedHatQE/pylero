# -*- coding: utf8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from pylero.base_polarion import BasePolarion
from pylero.enum_option_id import ArrayOfEnumOptionId
from pylero.enum_option_id import EnumOptionId
from pylero.signature_data import SignatureData
from pylero.subterra_uri import ArrayOfSubterraURI
from pylero.subterra_uri import SubterraURI
from pylero.text import Text
from pylero.user import User


class Comment(BasePolarion):
    """Object to handle the Polarion WSDL tns5:Comment class

    Attributes:
        author (User)
        child_comment_uris (ArrayOfSubterraURI)
        created (dateTime)
        comment_id (string)
        parent_comment_uri (SubterraURI)
        resolved (boolean)
        signature_data (SignatureData)
        tags (ArrayOfEnumOptionId)
        text (Text)
        title (string)
        visible_to (ArrayOfstring)
    """

    _cls_suds_map = {
        "author": {"field_name": "author", "cls": User},
        "child_comment_uris": {
            "field_name": "childCommentURIs",
            "is_array": True,
            "cls": SubterraURI,
            "arr_cls": ArrayOfSubterraURI,
            "inner_field_name": "SubterraURI",
        },
        "created": "created",
        "comment_id": "id",
        "parent_comment_uri": {"field_name": "parentCommentURI", "cls": SubterraURI},
        "resolved": "resolved",
        "signature_data": {"field_name": "signatureData", "cls": SignatureData},
        "tags": {
            "field_name": "tags",
            "is_array": True,
            "cls": EnumOptionId,
            "arr_cls": ArrayOfEnumOptionId,
            "inner_field_name": "EnumOptionId",
        },
        "text": {"field_name": "text", "cls": Text},
        "title": "title",
        "visible_to": "visibleTo",
        "uri": "_uri",
        "_unresolved": "_unresolved",
    }
    _obj_client = "builder_client"
    _obj_struct = "tns5:Comment"


class ArrayOfComment(BasePolarion):
    _obj_client = "builder_client"
    _obj_struct = "tns5:ArrayOfComment"
