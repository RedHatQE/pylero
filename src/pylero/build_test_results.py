# -*- coding: utf8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from pylero.base_polarion import BasePolarion


class BuildTestResults(BasePolarion):
    """Object to handle the Polarion WSDL tns2:BuildTestResults class

    Attributes:
        error_count (int)
        failure_count (int)
        skipped_count (int)
        test_count (int)"""

    _cls_suds_map = {
        "error_count": "errorCount",
        "failure_count": "failureCount",
        "skipped_count": "skippedCount",
        "test_count": "testCount",
        "uri": "_uri",
        "_unresolved": "_unresolved",
    }
    _obj_client = "builder_client"
    _obj_struct = "tns2:BuildTestResults"
