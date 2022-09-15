# -*- coding: utf8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from pylero.base_polarion import BasePolarion
from pylero.enum_option_id import EnumOptionId
from pylero.work_item import _WorkItem


class BuildLinkedWorkItem(BasePolarion):
    """Object to handle the Polarion WSDL tns2:BuildLinkedWorkItem class

    Attributes:
        revision (string)
        role (EnumOptionId)
        work_item (WorkItem)"""

    _cls_suds_map = {
        "revision": "revision",
        "role": {
            "field_name": "role",
            "cls": EnumOptionId,
            "enum_id": "workitem-link-role",
        },
        "work_item": {"field_name": "workItem", "cls": _WorkItem},
        "uri": "_uri",
        "_unresolved": "_unresolved",
    }
    _obj_client = "builder_client"
    _obj_struct = "tns2:BuildLinkedWorkItem"


class ArrayOfBuildLinkedWorkItem(BasePolarion):
    _obj_client = "builder_client"
    _obj_struct = "tns2:ArrayOfBuildLinkedWorkItem"
