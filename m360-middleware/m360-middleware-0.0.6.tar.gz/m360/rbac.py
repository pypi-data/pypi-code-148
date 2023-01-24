"""
Copyright (C) 2022 Corsair M360, Inc - All Rights Reserved.
Unauthorized copying of this file, via any medium is strictly prohibited.
Proprietary and confidential.
"""

import os
import json
import logging
import traceback
from pydash import py_

from m360 import utils, service, tenant, user
from m360.gateway import connector

_logger = logging.getLogger(__name__)
_connector = connector.instance()

class Rbac(object):
    """Offers rbac related helper methods"""

    # singleton
    _instance = None

    _config = None

    def __init__(self):
        _logger.debug("Rbac created")

    @staticmethod
    def rbac_singleton():
        """Access the singleton receiver"""

        if Rbac._instance:
            return Rbac._instance

        if not Rbac._instance:
            _logger.debug("Creating rbac instance")
            Rbac._instance = Rbac()

        return Rbac._instance

    @classmethod
    def set_service_config(cls, config):
        """
        This method sets the configuration of the middleware in the RBAC library
        @param config   {dict}
        """
        cls._config = config

    @classmethod
    def get(cls, request, section=None):
        """
        This method checks that m360 is provided in the request headers.
        Then it scans to find the fields' information inside m360 and returns it.
        @param request   {dict}
        @param section   {dict}
        @returns {dict}
        """
        if not request:
            return None
        headers = utils.get_req_headers(request)
        if not headers or not headers.get("m360"):
            return None
        m360 = headers.get("m360")
        try:
            if m360:
                m360 = json.loads(m360)
        except Exception as e:
            _logger.error(e)

        if not m360 or not utils.is_dict(m360) or not m360.get("rbac"):
            return None

        if section == "resource" or section == "resources":
            section = "resources"
        elif section == "condition" or section == "conditions":
            section = "conditions"
        elif section == "field" or section == "fields":
            section = "fields"
        elif section:
            raise Exception("Invalid section: " + section)

        if section and len(section.strip()) > 0 and m360.get("rbac").get(section):
            return m360.get("rbac").get(section)

        return m360.get("rbac")

    @classmethod
    def get_rbac_fields_from_service_contract(cls, request, rbac_field_options):
        """
        This method checks if the rbac fields configuration is set for a specific endpoint in the service contract
        by cross-referencing the request method and url with the contract
        @param request              {dict}
        @param rbac_field_options   {dict}
        @returns {dict}
        """
        if not rbac_field_options:
            return None

        rbac_field_options["allow"] = []
        rbac_field_options["deny"] = []
        endpoint_info = service.instance().get_endpoint_info(request)
        if not endpoint_info or not endpoint_info.get("method") or not endpoint_info.get("endpoint"):
            return rbac_field_options

        method = endpoint_info.get("method")
        endpoint = endpoint_info.get("endpoint")
        fields = py_.get(cls._config, 'contract.apis.main.' + method + '.' + endpoint + '.rbac.fields')
        if not fields:
            return rbac_field_options

        rbac_field_options["contract"] = fields
        rbac_configured_field_list = py_.clone(rbac_field_options.get("list"))
        processed_fields = []
        for contract_field in fields:
            if rbac_configured_field_list:
                for k, v in rbac_configured_field_list.items():
                    if v == contract_field or contract_field in v:
                        if rbac_field_options.get("operator") == "allow":
                            if v not in rbac_field_options["allow"]:
                                rbac_field_options["allow"].append(v)
                        else:
                            if v not in rbac_field_options["deny"]:
                                rbac_field_options["deny"].append(v)
                        processed_fields.append(contract_field)
        for contract_field in fields:
            if contract_field not in processed_fields:
                if rbac_field_options.get("operator") == "allow":
                    if contract_field not in rbac_field_options["deny"]:
                        rbac_field_options["deny"].append(contract_field)
                else:
                    if contract_field not in rbac_field_options["allow"]:
                        rbac_field_options["allow"].append(contract_field)

        return rbac_field_options

    @classmethod
    def can_access(cls, request, mode=None, data=None):
        """
        Simplified method that wraps around the other can Access operations
        @param request  {dict}
        @param mode     {str}
        @param data     {dict}
        @returns {bool}
        """
        options = None
        if mode in ["resource", "resources"]:
            options = cls.get(request, "resources")
            return cls.can_access_resources(request, options, data)
        elif mode in ["condition", "conditions"]:
            options = cls.get(request, "conditions")
            return cls.can_access_conditions(request, options, data)
        elif mode in ["field", "fields"]:
            options = cls.get(request, "fields")
            return cls.can_access_fields(request, options, data)
        else:
            raise Exception("Unsupported RBAC Access Mode Parameter 2!")

    @classmethod
    def can_access_fields(cls, request, options=None, data=None):
        """
        This method checks if the access is granted or denied for the given data object based on the given options
        @param request  {dict}
        @param options  {dict}
        @param data     {dict}
        @returns {bool}
        """
        # get the list of configured fields
        rbac_options = py_.clone_deep(options)

        def check_all_fields_in_object(data_obj):
            # loop in configured field and for each entry check in the object
            for i in data_obj:
                # ignore the non contract fields
                if i not in rbac_options.get("contract"):
                    continue
                # return false immediately if access is denied to any of the fields
                if i in rbac_options.get("deny"):
                    return False
            # return ok, all normal
            return True

        def is_field_rbac_configured():
            return rbac_options and rbac_options.get("operator") and rbac_options["operator"] in ["allow", "deny"] \
                   and rbac_options.get("list") and len(rbac_options["list"]) > 0

        if not data or not utils.is_dict(data):
            raise Exception("Unsupported data type provided, parameter 3 should can only be of type Object")

        # default to true if no RBAC fields is configured
        if not is_field_rbac_configured():
            return True

        rbac_options = cls.get_rbac_fields_from_service_contract(request, rbac_options)
        return check_all_fields_in_object(data)

    @classmethod
    def can_access_resources(cls, request, options=None, data=None):
        """
        This method checks if the user in the request has access to the data record provided based on Configured
        RBAC Resources
        @param request  {dict}
        @param options  {dict}
        @param data     {dict}
        @returns {bool}
        """

        def check_resources_access_in_object():
            # if no user, return false
            usr = user.instance().get(request)
            if not usr:
                return False
            # if mode is any, return true
            if options.get("mode") == "any":
                return True
            # get the value from the data record
            left_field = py_.get(data, options.get("field"))
            # get the value from the request user object
            right_field = py_.get(usr, options.get("value"))
            # return true if both match
            return left_field == right_field

        def is_field_rbac_configured():
            return options and options.get("mode") and options["mode"] in ["any", "own"] and \
                   (options["mode"] == "any" or (options["mode"] == "own" and options.get("field") and
                    len(options["field"].strip()) > 0 and options.get("value") and len(options["value"].strip()) > 0))

        if not data or utils.is_array(data) or not utils.is_dict(data):
            raise Exception("Unsupported data type provided, parameter 3 should can only be of type Object")

        # default to true if no RBAC fields is configured
        if not is_field_rbac_configured():
            return True

        return check_resources_access_in_object()

    @classmethod
    def can_access_conditions(cls, request, options=None, data=None):
        """
        This method checks if the user in the request has access to the data record provided based on Configured
        RBAC Conditions
        @param request  {dict}
        @param options  {dict}
        @param data     {dict}
        @returns {bool}
        """
        allowed_methods = ["EMPTY", "NOT_EMPTY", "EQ", "NOT_EQ", "START", "NOT_START", "END", "NOT_END", "IN",
                           "NOT_IN", "CONTAIN", "NOT_CONTAIN"]

        def check_one_condition(usr, condition):
            # get the value from the data record
            left_field = py_.get(data, condition["arguments"]["field"])

            if condition["arguments"].get("tCode") and len(condition["arguments"]["tCode"].strip()) > 0:
                # if no tenant, return false
                ten = tenant.instance().get(request, condition["arguments"]["tCode"])
                if not ten:
                    return False

                left_field = py_.get(ten, condition["arguments"]["field"])

            if condition["arguments"].get("custom") and len(condition["arguments"]["custom"].strip()) > 0:
                right_field = condition["arguments"]["custom"]
            else:
                # get the value from the request user object
                right_field = py_.get(usr, condition["arguments"]["value"])

            if right_field in ["true", "false"]:
                right_field = (right_field == "true")

            # return true if function matches
            condition_status_result = False
            cond_func = condition["function"].lower()
            if cond_func == "empty":
                if not left_field:
                    condition_status_result = True
            elif cond_func == "not_empty":
                if left_field:
                    condition_status_result = True
            elif cond_func == "eq":
                if left_field == right_field:
                    condition_status_result = True
            elif cond_func == "not_eq":
                if left_field != right_field:
                    condition_status_result = True
            elif cond_func == "start":
                if left_field.startswith(right_field):
                    condition_status_result = True
            elif cond_func == "not_start":
                if not left_field.startswith(right_field):
                    condition_status_result = True
            elif cond_func == "end":
                if left_field.endswith(right_field):
                    condition_status_result = True
            elif cond_func == "not_end":
                if not left_field.endswith(right_field):
                    condition_status_result = True
            elif cond_func in ["in", "contain"]:
                if utils.is_iterable(left_field) and right_field in left_field:
                    condition_status_result = True
            elif cond_func in ["not_in", "not_contain"]:
                if utils.is_iterable(left_field) and right_field not in left_field:
                    condition_status_result = True

            return condition_status_result

        def check_configured_conditions_for_access_in_object():
            # if no user, return false
            usr = user.instance().get(request)
            if not usr:
                return False

            conditions_met = []
            for criteria in options["criteria"]:
                if criteria.get("function") and criteria["function"] in allowed_methods and criteria.get("arguments") \
                        and "field" in criteria["arguments"] and "value" in criteria["arguments"]:
                    try:
                        conditions_met.append(check_one_condition(usr, criteria))
                    except Exception as e:
                        traceback.print_exc()
                        return e
                else:
                    # return false immediately if one condition doesn't have the correct format
                    return False

            # if operator is "and", all the values in the array must be true
            if options.get("operator") == "$and":
                return False not in conditions_met
            else:
                return True in conditions_met

        def is_field_rbac_configured():
            return options and options.get("operator") and options["operator"] in ["$and", "$or"] and \
                   options.get("criteria") and utils.is_array(options["criteria"]) and len(options["criteria"]) > 0

        if not data or utils.is_array(data) or not utils.is_dict(data):
            raise Exception("Unsupported data type provided, parameter 3 should can only be of type Object")

        if is_field_rbac_configured():
            return check_configured_conditions_for_access_in_object()
        else:
            return True

    @classmethod
    def filter_fields(cls, request, data=None):
        """
        This method removes the fields from the record if the access is false
        @param request  {dict}
        @param data     {dict or list}
        @returns {dict}
        """
        rbac_options = cls.get(request, "fields")
        options = cls.get_rbac_fields_from_service_contract(request, py_.clone_deep(rbac_options))

        def do_filter(record):
            return_record = {}
            if options.get("operator") == "deny":
                return_record = py_.clone(record)
                for denied in options.get("deny"):
                    utils.remove_object_from_path(return_record, denied)
            else:
                # fill the fields that are not in the contract
                for i in record:
                    if i not in options.get("contract"):
                        return_record[i] = py_.clone_deep(record[i])
                for allowed in options.get("allow"):
                    value = py_.get(record, allowed)
                    utils.build_object_from_path(return_record, allowed, py_.clone_deep(value))

            return return_record

        def is_field_rbac_configured():
            return options and options.get("operator") and options["operator"] in ["allow", "deny"] and \
                   options.get("list") and len(options["list"]) > 0

        if not is_field_rbac_configured():
            return data

        if data:
            if utils.is_array(data):
                for i in range(len(data)):
                    data[i] = do_filter(data[i])
            elif utils.is_dict(data):
                data = do_filter(data)

        return data


def instance():
    """Get the singleton instance of the rbac"""
    _logger.debug("calling instance, os.pid=%d", os.getpid())
    return Rbac.rbac_singleton()
