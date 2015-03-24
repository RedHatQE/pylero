# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals
from pylarion.base_polarion import BasePolarion
from pylarion.signature import Signature
from pylarion.signature import ArrayOfSignature
from pylarion.user import User


class SignatureContext(BasePolarion):
    """Object to handle the Polarion WSDL tns4:SignatureContext class

    Attributes:
        signatures (ArrayOfSignature)
        target_status_id (string)
        transition_data_revision (string)
        user (User)
"""
    _cls_suds_map = {"transition_data_revision": "transitionDataRevision",
                     "signatures":
                     {"field_name": "signatures",
                      "is_array": True,
                      "cls": Signature,
                      "arr_cls": ArrayOfSignature,
                      "inner_field_name": "Signature"},
                     "target_status_id": "targetStatusId",
                     "user":
                     {"field_name": "user",
                      "cls": User}}
    _obj_client = "test_management_client"
    _obj_struct = "tns4:SignatureContext"


class ArrayOfSignatureContext(BasePolarion):
    _obj_client = "test_management_client"
    _obj_struct = "tns4:ArrayOfSignatureContext"
