# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals
import pylarion.base_polarion as bp
import pylarion.text as t


class Category(bp.BasePolarion):
    """Object to handle the Polarion WSDL tns5:Category class

    Attributes (for specific details, see Polarion):
        description (Text)
        category_id (string)
        name (string)
"""
    _cls_suds_map = {"description": {"field_name": "description",
                                     "cls": t.Text},
                     "category_id": "id",
                     "name": "name",
                     "uri": "_uri",
                     "_unresolved": "_unresolved"}
    _obj_client = "builder_client"
    _obj_struct = "tns5:Category"


class ArrayOfCategory(bp.BasePolarion):
    _obj_client = "builder_client"
    _obj_struct = "tns5:ArrayOfCategory"
