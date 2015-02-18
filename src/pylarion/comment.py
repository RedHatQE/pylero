# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals
import pylarion.base_polarion as bp
import pylarion.user as u
import pylarion.subterra_uri as stu
import pylarion.signature_data as sigdat
import pylarion.text as t
import pylarion.enum_option_id as eoi


class Comment(bp.BasePolarion):
    """Object to handle the Polarion WSDL tns5:Comment class

    Attributes (for specific details, see Polarion):
        author (User)
        child_comment_uris (ArrayOfSubterraURI)
        created (dateTime)
        comment_id (string)
        parent_comment_uri (SubterraURI)
        resolved (boolean)
        signature_data (SignatureData)
        tags (ArrayOfeoi.EnumOptionId)
        text (Text)
        title (string)
        visible_to (ArrayOfstring)
"""
    _cls_suds_map = {"author": {"field_name": "author", "cls": u.User},
                     "child_comment_uris": {"field_name": "childCommentURIs",
                                            "is_array": True,
                                            "cls": stu.SubterraURI,
                                            "arr_cls": stu.ArrayOfSubterraURI,
                                            "inner_field_name": "SubterraURI"},
                     "created": "created",
                     "comment_id": "id",
                     "parent_comment_uri": {"field_name": "parentCommentURI",
                                            "cls": stu.SubterraURI},
                     "resolved": "resolved",
                     "signature_data": {"field_name": "signatureData",
                                        "cls": sigdat.SignatureData},
                     "tags": {"field_name": "tags",
                              "is_array": True,
                              "cls": eoi.EnumOptionId,
                              "arr_cls": eoi.ArrayOfEnumOptionId,
                              "inner_field_name": "eoi.EnumOptionId"},
                     "text": {"field_name": "text", "cls": t.Text},
                     "title": "title",
                     "visible_to": "visibleTo",
                     "uri": "_uri",
                     "_unresolved": "_unresolved"}
    _obj_client = "builder_client"
    _obj_struct = "tns5:Comment"


class ArrayOfComment(bp.BasePolarion):
    _obj_client = "builder_client"
    _obj_struct = "tns5:ArrayOfComment"
