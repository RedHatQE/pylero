# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals
import pylarion.base_polarion as bp
import pylarion.enum_option_id as eoi
import pylarion.user as u


class Signature(bp.BasePolarion):
    _cls_suds_map = {"verdict": {"field_name": "verdict",
                                 "cls": eoi.EnumOptionId},
                     "signed_revision": "signedRevision",
                     "verdict_time": "verdictTime",
                     "signer_role": "signerRole",
                     "signed_by": {"field_name": "signedBy", "cls": u.User}}
    _obj_client = "test_management_client"
    _obj_struct = "tns4:Signature"


class ArrayOfSignature(bp.BasePolarion):
    _obj_client = "test_management_client"
    _obj_struct = "tns4:ArrayOfSignature"
