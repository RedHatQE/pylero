# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals
import pylarion.base_polarion as bp


class LanguageDefinition(bp.BasePolarion):
    """Object to handle the Polarion WSDL tns3:LanguageDefinition class

    Attributes (for specific details, see Polarion):
        language_definition_id (string)
        label (string)
"""
    _cls_suds_map = {"language_definition_id": "id",
                     "label": "label",
                     "uri": "_uri",
                     "_unresolved": "_unresolved"}
    _obj_client = "tracker_client"
    _obj_struct = "tns3:LanguageDefinition"
