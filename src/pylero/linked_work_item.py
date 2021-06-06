# -*- coding: utf8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from pylero.base_polarion import BasePolarion
from pylero.enum_option_id import EnumOptionId


class LinkedWorkItem(BasePolarion):
    """Object to handle the Polarion WSDL tns5:LinkedWorkItem class

    Attributes:
        revision (string)
        role (EnumOptionId)
        suspect (boolean)
        work_item_id (string)
"""
    _cls_suds_map = {
        "revision": "revision",
        "role":
            {"field_name": "role",
             "cls": EnumOptionId,
             "enum_id": "workitem-link-role"},
        "suspect": "suspect",
        "work_item_id":  # class added in _fix_circular_refs function
            {"field_name": "workItemURI",
             "named_arg": "uri",
             "sync_field": "uri"}
    }
    _obj_client = "builder_client"
    _obj_struct = "tns5:LinkedWorkItem"
    _id_field = "work_item_id"

    def __init__(self, project_id=None, work_item_id=None, suds_object=None):
        self.project_id = project_id if project_id else self.default_project
        super(self.__class__, self).__init__(work_item_id, suds_object)

    def _fix_circular_refs(self):
        # need to import WorkItem, but this module is used by WorkItem.
        # need to pass in the project_id parm to the Work Item,
        # but it is not given before instantiation
        from pylero.work_item import _WorkItem
        self._cls_suds_map["work_item_id"]["cls"] = _WorkItem
        self._cls_suds_map["work_item_id"]["additional_parms"] = \
            {"project_id": self.project_id}


class ArrayOfLinkedWorkItem(BasePolarion):
    _obj_client = "builder_client"
    _obj_struct = "tns5:ArrayOfLinkedWorkItem"
