# -*- coding: utf8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from pylero.base_polarion import BasePolarion
from pylero.enum_option_id import EnumOptionId
from pylero.user import User


class Signature(BasePolarion):
    """Object to handle the Polarion WSDL tns4:Signature class

    Attributes:
        signed_by (User)
        signed_revision (string)
        signer_role (string)
        verdict (EnumOptionId)
        verdict_time (dateTime)"""

    _cls_suds_map = {
        "verdict": {"field_name": "verdict", "cls": EnumOptionId},
        "signed_revision": "signedRevision",
        "verdict_time": "verdictTime",
        "signer_role": "signerRole",
        "signed_by": {"field_name": "signedBy", "cls": User},
    }
    _obj_client = "test_management_client"
    _obj_struct = "tns4:Signature"


class ArrayOfSignature(BasePolarion):
    _obj_client = "test_management_client"
    _obj_struct = "tns4:ArrayOfSignature"
