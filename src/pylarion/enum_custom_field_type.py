# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals
import pylarion.base_polarion as bp


class EnumCustomFieldType(bp.BasePolarion):
    """Object to handle the Polarion WSDL tns5:EnumCustomFieldType class

    Attributes (for specific details, see Polarion):
        default_value (anyType)
        depends_on (string)
        description (string)
        enum_id (string)
        id (string)
        name (string)
        required (boolean)
        type (string)
"""
# id field is called id and not enum_custom_field_type_id because it is often
# mixed with custom_field_type and they need to be accessed interchangeably
    _cls_suds_map = {"default_value": "defaultValue",
                     "depends_on": "dependsOn",
                     "description": "description",
                     "enum_id": "enumId",
                     "id": "id",
                     "name": "name",
                     "required": "required",
                     "type": "type",
                     "uri": "_uri",
                     "_unresolved": "_unresolved"}
    _obj_client = "builder_client"
    _obj_struct = "tns5:EnumCustomFieldType"
