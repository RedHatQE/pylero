# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals
from pylarion.base_polarion import BasePolarion
from pylarion.user import User
from pylarion.imported_comment import ImportedComment
from pylarion.subterra_uri import SubterraURI
from pylarion.subterra_uri import ArrayOfSubterraURI
from pylarion.signature_data import SignatureData
from pylarion.enum_option_id import EnumOptionId
from pylarion.enum_option_id import ArrayOfEnumOptionId
from pylarion.text import Text


class ModuleComment(BasePolarion):
    """Object to handle the Polarion WSDL tns4:ModuleComment class

    Attributes:
        author (User)
        child_comment_uris (ArrayOfSubterraURI)
        created (dateTime)
        module_comment_id (string)
        imported_comment (ImportedComment)
        parent_comment_uri (SubterraURI)
        referred_work_item_uri (SubterraURI)
        resolved (boolean)
        signature_data (SignatureData)
        tags (ArrayOfEnumOptionId)
        text (Text)
"""
    _cls_suds_map = {"author":
                     {"field_name": "author",
                      "cls": User},
                     "child_comment_uris":
                     {"field_name": "childCommentURIs",
                      "is_array": True,
                      "cls": SubterraURI,
                      "arr_cls": ArrayOfSubterraURI,
                      "inner_field_name": "SubterraURI"},
                     "created": "created",
                     "module_comment_id": "id",
                     "imported_comment":
                     {"field_name": "importedComment",
                      "cls": ImportedComment},
                     "parent_comment_uri":
                     {"field_name": "parentCommentURI",
                      "cls": SubterraURI},
                     "referred_work_item_uri":
                     {"field_name": "referredWorkItemURI",
                      "cls": SubterraURI},
                     "resolved": "resolved",
                     "signature_data":
                     {"field_name": "signatureData",
                      "cls": SignatureData},
                     "tags":
                     {"field_name": "tags",
                      "is_array": True,
                      "cls": EnumOptionId,
                      "arr_cls": ArrayOfEnumOptionId,
                      "inner_field_name": "EnumOptionId"},
                     "text":
                     {"field_name": "text",
                      "cls": Text},
                     "uri": "_uri",
                     "_unresolved": "_unresolved"}
    _obj_client = "test_management_client"
    _obj_struct = "tns4:ModuleComment"


class ArrayOfModuleComment(BasePolarion):
    _obj_client = "test_management_client"
    _obj_struct = "tns4:ArrayOfModuleComment"
