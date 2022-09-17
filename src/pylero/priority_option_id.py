# -*- coding: utf8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from pylero.base_polarion import BasePolarion


class PriorityOptionId(BasePolarion):
    """Object to handle the Polarion WSDL tns5:PriorityOptionId class

    Attributes:
        id (string)"""

    _cls_suds_map = {"id": "id", "uri": "_uri", "_unresolved": "_unresolved"}
    _id_field = "id"
    _obj_client = "builder_client"
    _obj_struct = "tns5:PriorityOptionId"

    def __init__(self, id=None, uri=None, suds_object=None):
        """PriorityOptionID Constructor

        Args:
            id: value of the priority
            uri: the SubterraURI of the priority
            suds_object: the Polarion Plan object

        Returns:
            None

        References:
            _WorkItem.priority
        """
        super(self.__class__, self).__init__(id, suds_object)


class ArrayOfPriorityOptionId(BasePolarion):
    _obj_client = "builder_client"
    _obj_struct = "tns5:ArrayOfPriorityOptionId"
