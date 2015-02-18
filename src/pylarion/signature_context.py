# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals
import pylarion.base_polarion as bp
import pylarion.signature as sig
import pylarion.user as u


class SignatureContext(bp.BasePolarion):
    _cls_suds_map = {"transition_data_revision": "transitionDataRevision",
                     "signatures": {"field_name": "signatures",
                                    "is_array": True,
                                    "cls": sig.Signature,
                                    "arr_cls": sig.ArrayOfSignature,
                                    "inner_field_name": "Signature"},
                     "target_status_id": "targetStatusId",
                     "user": {"field_name": "user", "cls": u.User}}
    _obj_client = "test_management_client"
    _obj_struct = "tns4:SignatureContext"


class ArrayOfSignatureContext(bp.BasePolarion):
    _obj_client = "test_management_client"
    _obj_struct = "tns4:ArrayOfSignatureContext"
