# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals
import pylarion.base_polarion as bp
import pylarion.enum_option_id as eoi
import pylarion.work_item as wi


class BuildLinkedWorkItem(bp.BasePolarion):
    """Object to handle the Polarion WSDL tns2:BuildLinkedWorkItem class

    Attributes (for specific details, see Polarion):
        revision (string)
        role (eoi.EnumOptionId)
        work_item (WorkItem)
"""
    _cls_suds_map = {"revision": "revision",
                     "role": {"field_name": "role", "cls": eoi.EnumOptionId},
                     "work_item": {"field_name": "workItem",
                                   "cls": wi._WorkItem},
                     "uri": "_uri",
                     "_unresolved": "_unresolved"}
    _obj_client = "builder_client"
    _obj_struct = "tns2:BuildLinkedWorkItem"


class ArrayOfBuildLinkedWorkItem(bp.BasePolarion):
    _obj_client = "builder_client"
    _obj_struct = "tns2:ArrayOfBuildLinkedWorkItem"
