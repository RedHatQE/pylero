# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals
import pylarion.base_polarion as bp
import pylarion.enum_option_id as eoi
import pylarion.subterra_uri as stu


class LinkedWorkItem(bp.BasePolarion):
    """Object to handle the Polarion WSDL tns5:LinkedWorkItem class

    Attributes (for specific details, see Polarion):
        revision (string)
        role (eoi.EnumOptionId)
        suspect (boolean)
        work_item_uri (SubterraURI)
"""
    _cls_suds_map = {"revision": "revision",
                     "role": {"field_name": "role", "cls": eoi.EnumOptionId},
                     "suspect": "suspect",
                     "work_item_uri": {"field_name": "workItemURI",
                                       "cls": stu.SubterraURI},
                     "uri": "_uri",
                     "_unresolved": "_unresolved"}
    _obj_client = "builder_client"
    _obj_struct = "tns5:LinkedWorkItem"


class ArrayOfLinkedWorkItem(bp.BasePolarion):
    _obj_client = "builder_client"
    _obj_struct = "tns5:ArrayOfLinkedWorkItem"
