# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals
import pylarion.base_polarion as bp
import pylarion.enum_option_id as eoi


class WorkflowAction(bp.BasePolarion):
    """Object to handle the Polarion WSDL tns3:WorkflowAction class

    Attributes (for specific details, see Polarion):
        action_id (int)
        action_name (string)
        cleaned_features (ArrayOf_xsd_string)
        native_action_id (string)
        required_features (ArrayOf_xsd_string)
        suggested_features (ArrayOf_xsd_string)
        target_status (eoi.EnumOptionId)
        unavailability_message (string)
"""
    _cls_suds_map = {"action_id": "actionId",
                     "action_name": "actionName",
                     "cleaned_features": "cleaned_features",
                     "native_action_id": "nativeActionId",
                     "required_features": "requiredFeatures",
                     "suggested_features": "suggestedFeatures",
                     "target_status": {"field_name": "targetStatus",
                                       "cls": eoi.EnumOptionId},
                     "unavailability_message": "unavailabilityMessage",
                     "uri": "_uri",
                     "_unresolved": "_unresolved"}
    _obj_client = "tracker_client"
    _obj_struct = "tns3:WorkflowAction"
