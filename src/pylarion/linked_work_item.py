# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals
from pylarion.base_polarion import BasePolarion
from pylarion.enum_option_id import EnumOptionId
from pylarion.subterra_uri import SubterraURI


class LinkedWorkItem(BasePolarion):
    """Object to handle the Polarion WSDL tns5:LinkedWorkItem class

    Attributes (for specific details, see Polarion):
        revision (string)
        role (EnumOptionId)
        suspect (boolean)
        work_item_uri (SubterraURI)
"""
    _cls_suds_map = {"revision": "revision",
                     "role":
                     {"field_name": "role",
                      "cls": EnumOptionId},
                     "suspect": "suspect",
                     "work_item_uri":
                     {"field_name": "workItemURI",
                      "cls": SubterraURI},
                     "uri": "_uri",
                     "_unresolved": "_unresolved"}
    _obj_client = "builder_client"
    _obj_struct = "tns5:LinkedWorkItem"


class ArrayOfLinkedWorkItem(BasePolarion):
    _obj_client = "builder_client"
    _obj_struct = "tns5:ArrayOfLinkedWorkItem"
