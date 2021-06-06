# -*- coding: utf8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from pylero.base_polarion import BasePolarion


# Array of License Info is listed as: ArrayOf_tns3_LicenseInfo
class ProductLicense(BasePolarion):
    """Object to handle the Polarion WSDL tns3:ProductLicense class

    Attributes:
        concurrent_license_data (ArrayOf_tns3_LicenseInfo)
        customer_company (string)
        customer_email (string)
        customer_name (string)
        date_created (dateTime)
        expiration_date (dateTime)
        generated_by (string)
        ip_address (string)
        license_format (string)
        license_profile (string)
        mac_address (string)
        named_license_data (ArrayOf_tns3_LicenseInfo)
"""
    _cls_suds_map = {"concurrent_license_data": "concurrent_license_data",
                     "customer_company": "customerCompany",
                     "customer_email": "customerEmail",
                     "customer_name": "customerName",
                     "date_created": "dateCreated",
                     "expiration_date": "expirationDate",
                     "generated_by": "generatedBy",
                     "ip_address": "ipAddress",
                     "license_format": "licenseFormat",
                     "license_profile": "licenseProfile",
                     "mac_address": "macAddress",
                     "named_license_data": "named_license_data",
                     "uri": "_uri",
                     "_unresolved": "_unresolved"}
    _obj_client = "security_client"
    _obj_struct = "tns3:ProductLicense"
