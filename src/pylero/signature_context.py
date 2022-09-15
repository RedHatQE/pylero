# -*- coding: utf8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from pylero.base_polarion import BasePolarion
from pylero.signature import ArrayOfSignature
from pylero.signature import Signature
from pylero.user import User


class SignatureContext(BasePolarion):
    """Object to handle the Polarion WSDL tns4:SignatureContext class

    Attributes:
        signatures (ArrayOfSignature)
        target_status_id (string)
        transition_data_revision (string)
        user (User)"""

    _cls_suds_map = {
        "transition_data_revision": "transitionDataRevision",
        "signatures": {
            "field_name": "signatures",
            "is_array": True,
            "cls": Signature,
            "arr_cls": ArrayOfSignature,
            "inner_field_name": "Signature",
        },
        "target_status_id": "targetStatusId",
        "user": {"field_name": "user", "cls": User},
    }
    _obj_client = "test_management_client"
    _obj_struct = "tns4:SignatureContext"


class ArrayOfSignatureContext(BasePolarion):
    _obj_client = "test_management_client"
    _obj_struct = "tns4:ArrayOfSignatureContext"
