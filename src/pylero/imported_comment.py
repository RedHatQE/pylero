# -*- coding: utf8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from pylero.base_polarion import BasePolarion


class ImportedComment(BasePolarion):
    """Object to handle the Polarion WSDL tns4:ImportedComment class

    Attributes:
        author (string)
        created (dateTime)
        initials (string)"""

    _cls_suds_map = {
        "author": "author",
        "created": "created",
        "initials": "initials",
        "uri": "_uri",
        "_unresolved": "_unresolved",
    }
    _obj_client = "test_management_client"
    _obj_struct = "tns4:ImportedComment"
