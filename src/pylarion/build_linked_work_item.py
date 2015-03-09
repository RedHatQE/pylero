# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals
from pylarion.base_polarion import BasePolarion
from pylarion.enum_option_id import EnumOptionId
from pylarion.work_item import _WorkItem


class BuildLinkedWorkItem(BasePolarion):
    """Object to handle the Polarion WSDL tns2:BuildLinkedWorkItem class

    Attributes (for specific details, see Polarion):
        revision (string)
        role (EnumOptionId)
        work_item (WorkItem)
"""
    _cls_suds_map = {"revision": "revision",
                     "role":
                     {"field_name": "role",
                      "cls": EnumOptionId},
                     "work_item":
                     {"field_name": "workItem",
                      "cls": _WorkItem},
                     "uri": "_uri",
                     "_unresolved": "_unresolved"}
    _obj_client = "builder_client"
    _obj_struct = "tns2:BuildLinkedWorkItem"


class ArrayOfBuildLinkedWorkItem(BasePolarion):
    _obj_client = "builder_client"
    _obj_struct = "tns2:ArrayOfBuildLinkedWorkItem"
