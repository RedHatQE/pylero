# -*- coding: utf8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from pylero.base_polarion import BasePolarion
from pylero.build_linked_work_item import ArrayOfBuildLinkedWorkItem
from pylero.build_linked_work_item import BuildLinkedWorkItem
from pylero.build_test_results import BuildTestResults
from pylero.user import User


class Build(BasePolarion):
    """Object to handle the Polarion WSDL tns2:Build class

    Attributes:
        author (User)
        bir_location (Location)
        build_descriptor_name (string)
        build_stamp (string)
        build_status (string)
        build_tag (string)
        build_test_results (BuildTestResults)
        calculation_descriptor_name (string)
        creation_time (dateTime)
        finish_time (dateTime)
        build_id (string)
        job_id (string)
        linked_work_items (ArrayOfBuildLinkedWorkItem)
        local_deployment_space_name (string)
        log_files (ArrayOfLocation)
        start_time (dateTime)"""

    _cls_suds_map = {
        "author": {"field_name": "author", "cls": User},
        "bir_location": "birLocation",
        "build_descriptor_name": "buildDescriptorName",
        "build_stamp": "buildStamp",
        "build_status": "buildStatus",
        "build_tag": "buildTag",
        "build_test_results": {
            "field_name": "buildTestResults",
            "cls": BuildTestResults,
        },
        "calculation_descriptor_name": "calculationDescriptorName",
        "creation_time": "creationTime",
        "finish_time": "finishTime",
        "build_id": "id",
        "job_id": "jobId",
        "linked_work_items": {
            "field_name": "linkedWorkItems",
            "is_array": True,
            "cls": BuildLinkedWorkItem,
            "arr_cls": ArrayOfBuildLinkedWorkItem,
            "inner_field_name": "BuildLinkedWorkItem",
        },
        "local_deployment_space_name": "localDeploymentSpaceName",
        "log_files": "logFiles",
        "start_time": "startTime",
        "uri": "_uri",
        "_unresolved": "_unresolved",
    }
    _obj_client = "builder_client"
    _obj_struct = "tns2:Build"
