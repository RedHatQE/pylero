# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals
from pylarion.base_polarion import BasePolarion
from pylarion.enum_option_id import EnumOptionId


class ExternallyLinkedWorkItem(BasePolarion):
    """Object to handle the Polarion WSDL tns5:ExternallyLinkedWorkItem class

    Attributes (for specific details, see Polarion):
        role (EnumOptionId)
        work_item_uri (string)
"""
    _cls_suds_map = {"role":
                     {"field_name": "role",
                      "cls": EnumOptionId,
                      "enum_id": "workitem-link-role"},
                     "work_item_uri": "workItemURI",
                     "uri": "_uri",
                     "_unresolved": "_unresolved"}
    _obj_client = "builder_client"
    _obj_struct = "tns5:ExternallyLinkedWorkItem"


class ArrayOfExternallyLinkedWorkItem(BasePolarion):
    _obj_client = "builder_client"
    _obj_struct = "tns5:ArrayOfExternallyLinkedWorkItem"
