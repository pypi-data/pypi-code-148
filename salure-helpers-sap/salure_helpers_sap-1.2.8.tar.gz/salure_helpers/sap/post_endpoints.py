from salure_helpers.sap.base_functions import BaseFunctions
import requests
import warnings
import json
from typing import Union, List


class PostEndpoints:
    def __init__(self, label: str, data_dir: str, certificate_file: str = None, key_file: str = None, debug: bool = False):
        self.base_class = BaseFunctions(label=label, data_dir=data_dir, certificate_file=certificate_file, key_file=key_file, debug=debug)
        self.data_dir = data_dir
        self.debug = debug

    @staticmethod
    def __check_fields(data: Union[dict, List], required_fields: List, allowed_fields: List):
        if isinstance(data, dict):
            data = data.keys()

        for field in data:
            if field not in allowed_fields and field not in required_fields:
                warnings.warn('Field {field} is not implemented. Optional fields are: {allowed_fields}'.format(field=field, allowed_fields=tuple(allowed_fields)))

        for field in required_fields:
            if field not in data:
                raise ValueError('Field {field} is required. Required fields are: {required_fields}'.format(field=field, required_fields=tuple(required_fields)))

    def post_master_action(self, data: dict, overload_fields: dict = None):
        """
        Upload the new employee to SAP through MasterAction
        :param data: Fields that are allowed are listed in allowed fields array. Update this whenever necessary
        :return: status code for request and optional error message
        """
        allowed_fields = ['cost_carrier', 'org_unit_id', 'cost_center', 'salutation', 'last_name', 'first_name', 'name_prefix', 'second_name_prefix',
                          'middle_name', 'initials', 'second_title', 'date_of_birth', 'language', 'nationality', 'title', 'gender']
        required_fields = ['employment_status', 'afas_employee_id', 'employee_start_date', 'end_date', 'action', 'reason', 'position_id', 'employee_group',
                           'personal_area', 'personal_subarea', 'employee_subgroup']

        self.__check_fields(data=data, required_fields=required_fields, allowed_fields=allowed_fields)

        base_body = {
            "Afasemployeenumber": data['afas_employee_id'],
            "Employeenumber": "00000000",
            "Startdate": data['employee_start_date'],
            "Enddate": "9999-12-31",
            "Actiontype": data['action'],
            "Reasonforaction": data['reason'],
            "Employmentstatus": data['employment_status'],
            "Personnelarea": data['personal_area'],
            "Personnelsubarea": data['personal_subarea'],
            "Employeegroup": data['employee_group'],
            "Employeesubgroup": data['employee_subgroup'],
            "PositionID": data['position_id']
        }
        fields_to_update = {}

        # Add fields that you want to update a dict (adding to body itself is too much text)
        fields_to_update.update({"Companycode": data['cost_carrier']}) if 'cost_carrier' in data else fields_to_update
        fields_to_update.update({"OrgunitID": data['org_unit_id']}) if 'org_unit_id' in data else fields_to_update
        fields_to_update.update({"Costcenter": data['cost_center']}) if 'cost_center' in data else fields_to_update
        fields_to_update.update({"Salutation": data['salutation']}) if 'salutation' in data else fields_to_update
        fields_to_update.update({"Lastname": data['last_name']}) if 'last_name' in data else fields_to_update
        fields_to_update.update({"Firstname": data['first_name']}) if 'first_name' in data else fields_to_update
        fields_to_update.update({"Nameprefix": data['name_prefix']}) if 'name_prefix' in data else fields_to_update
        fields_to_update.update({"Secondnameprefix": data['second_name_prefix']}) if 'second_name_prefix' in data else fields_to_update
        fields_to_update.update({"Middlename": data['middle_name']}) if 'middle_name' in data else fields_to_update
        fields_to_update.update({"Initials": data['initials']}) if 'initials' in data else fields_to_update
        fields_to_update.update({"Othertitle": data['second_title']}) if 'second_title' in data else fields_to_update
        fields_to_update.update({"Dateofbirth": data['date_of_birth']}) if 'date_of_birth' in data else fields_to_update
        fields_to_update.update({"Communicationlanguage": data['language']}) if 'language' in data else fields_to_update
        fields_to_update.update({"Nationality": data['nationality']}) if 'nationality' in data else fields_to_update
        fields_to_update.update({"Title": data['title']}) if 'title' in data else fields_to_update
        fields_to_update.update({"Gender": data['gender']}) if 'gender' in data else fields_to_update

        fields_to_update.update(overload_fields) if overload_fields is not None else ''

        # Update the request body with update fields
        base_body.update(fields_to_update)
        response = self.base_class.post_data(uri='MasterActionPost/*', data=base_body, return_key='Employeenumber')
        return response

    def post_personal_data(self, data: dict, overload_fields: dict = None):
        """
        Upload the employee personal data
        :param data: Fields that are allowed are listed in allowed fields array. Update this whenever necessary
        :return: status code for request and optional error message
        """
        allowed_fields = ['last_name', 'first_name', 'name_prefix', 'second_name_prefix', 'middle_name', 'middle_name', 'initials', 'second_title',
                          'date_of_birth', 'language', 'nationality', 'title', 'gender']
        required_fields = ['afas_employee_id', 'sap_employee_id', 'start_date', 'end_date']

        self.__check_fields(data=data, required_fields=required_fields, allowed_fields=allowed_fields)

        base_body = {
            'PersonalData': {
                "Afasemployeenumber": data["afas_employee_id"],
                "Employeenumber": data["sap_employee_id"],
                "Startdate": data["start_date"],
                "Enddate": data["end_date"]
            }
        }
        fields_to_update = {}

        # Add fields that you want to update a dict (adding to body itself is too much text)
        fields_to_update.update({"Lastname": data['last_name']}) if 'last_name' in data else fields_to_update
        fields_to_update.update({"Firstname": data['first_name']}) if 'first_name' in data else fields_to_update
        fields_to_update.update({"Nameprefix": data['name_prefix']}) if 'name_prefix' in data else fields_to_update
        fields_to_update.update({"Secondnameprefix": data['second_name_prefix']}) if 'second_name_prefix' in data else fields_to_update
        fields_to_update.update({"Middlename": data['middle_name']}) if 'middle_name' in data else fields_to_update
        fields_to_update.update({"Initials": data['initials']}) if 'initials' in data else fields_to_update
        fields_to_update.update({"Salutation": data['salutation']}) if 'salutation' in data else fields_to_update
        fields_to_update.update({"Othertitle": data['second_title']}) if 'second_title' in data else fields_to_update
        fields_to_update.update({"Dateofbirth": data['date_of_birth']}) if 'date_of_birth' in data else fields_to_update
        fields_to_update.update({"Communicationlanguage": data['language']}) if 'language' in data else fields_to_update
        fields_to_update.update({"Nationality": data['nationality']}) if 'nationality' in data else fields_to_update
        fields_to_update.update({"Title": data['title']}) if 'title' in data else fields_to_update
        fields_to_update.update({"Gender": data['gender']}) if 'gender' in data else fields_to_update

        fields_to_update.update(overload_fields) if overload_fields is not None else ''

        # Update the request body with update fields
        base_body.update(fields_to_update)
        response = self.base_class.post_data(uri='PersonalDataPost/*', data=base_body, return_key=None)
        return response

    def post_communication(self, data: dict, overload_fields: dict = None):
        """
        Post communication data to SAP like email or KID
        :param data: Fields that are allowed are listed in allowed fields array. Update this whenever necessary
        :param overload_fields: Give the guid and value from a free field if wanted
        :return: status code for request and optional error message
        """

        allowed_fields = ['user_id', 'user_id_long']
        required_fields = ['afas_employee_id', 'sap_employee_id', 'start_date', 'end_date', 'user_type']

        self.__check_fields(data=data, required_fields=required_fields, allowed_fields=allowed_fields)

        base_body = {
            "Afasemployeenumber": data["afas_employee_id"],
            "Employeenumber": data["sap_employee_id"],
            "Startdate": data["start_date"],
            "Enddate": data["end_date"],
            "Usertype": data["user_type"]
        }
        fields_to_update = {}

        # Add fields that you want to update a dict (adding to body itself is too much text)
        fields_to_update.update({"UserId": data['user_id']}) if 'user_id' in data else fields_to_update
        fields_to_update.update({"UserIdLong": data['user_id_long']}) if 'user_id_long' in data else fields_to_update

        fields_to_update.update(overload_fields) if overload_fields is not None else ''

        # Update the request body with update fields
        base_body.update(fields_to_update)

        response = self.base_class.post_data(uri='CommunicationsPost/*', data=base_body, return_key='UserId')
        return response

    def post_organisational_unit(self, data: dict, overload_fields: dict = None):
        """
        Post OrgUnits to SAP
        :param data: Fields that are allowed are listed in allowed fields array. Update this whenever necessary
        :param overload_fields: Give the guid and value from a free field if wanted
        :return: status code for request and optional error message
        """
        allowed_fields = ['sap_organisational_unit_id', 'language']
        required_fields = ['start_date', 'end_date', 'organisational_unit_id', 'organisational_unit', 'parent_organisational_unit_id']

        self.__check_fields(data=data, required_fields=required_fields, allowed_fields=allowed_fields)

        base_body = {
            "OrgUnitID": "00000000" if data['sap_organisational_unit_id'] is None else data['sap_organisational_unit_id'],  # New organisational unit will have 00000000 as the OrgUnitID to indicate Creating new ones
            "Startdate": data["start_date"],
            "Enddate": data["end_date"],
            "Shorttext": data["organisational_unit_id"],
            "Longtext": data["organisational_unit"],
            "OrgunitIDassigend": data["parent_organisational_unit_id"]
        }
        fields_to_update = {}

        # Add fields that you want to update a dict (adding to body itself is too much text)
        fields_to_update.update({"Langu": data['language']}) if 'language' in data else fields_to_update

        fields_to_update.update(overload_fields) if overload_fields is not None else ''

        # Update the request body with update fields
        base_body.update(fields_to_update)

        response = self.base_class.post_data(uri='OrgUnitPost/*', data=base_body, return_key='OrgUnitID')
        return response

    def post_position(self, data: dict, overload_fields: dict = None):
        """
        Post Position to SAP
        :param data: Fields that are allowed are listed in allowed fields array. Update this whenever necessary
        :param overload_fields: Give the guid and value from a free field if wanted
        :return: status code for request and optional error message
        """
        allowed_fields = ['sap_position_id', 'language', 'cost_center', 'is_manager']
        required_fields = ['start_date', 'end_date', 'job_code', 'job', 'sap_organisational_unit_id']

        self.__check_fields(data=data, required_fields=required_fields, allowed_fields=allowed_fields)

        base_body = {
            "PositionID": "00000000" if data['sap_position_id'] is None or data['sap_position_id'] == '' else data['sap_position_id'],
            "Startdate": data['start_date'],
            "Enddate": data['end_date'],
            "Shorttext": data['job_code'],
            "Longtext": data['job'],
            "Omleader": False if data['is_manager'] is None or data['is_manager'] == '' else True,
            "OrgunitIDassigend": data['sap_organisational_unit_id']
        }

        # Add fields that you want to update a dict (adding to body itself is too much text)
        fields_to_update = {}
        fields_to_update.update({"Langu": data['language']}) if 'language' in data else fields_to_update
        fields_to_update.update({"Costcenter": data['cost_center']}) if 'cost_center' in data else fields_to_update
        fields_to_update.update(overload_fields) if overload_fields is not None else ''

        # Update the request body with update fields
        base_body.update(fields_to_update)

        response = self.base_class.post_data(uri='PositionPost/*', data=base_body, return_key='PositionID')
        return response

    def post_workcenter(self, data: dict, overload_fields: dict = None):
        """
        Post Workcenters to SAP, assign to an existing position
        :param data: Fields that are allowed are listed in allowed fields array. Update this whenever necessary
        :param overload_fields: Give the guid and value from a free field if wanted
        :return: status code for request and optional error message
        """
        allowed_fields = []
        required_fields = ['workcenter_id', 'start_date', 'end_date', 'sap_position_id']

        self.__check_fields(data=data, required_fields=required_fields, allowed_fields=allowed_fields)

        base_body = {
            "WorkcenterID": data['workcenter_id'],
            "Startdate": data['start_date'],
            "Enddate": data['end_date'],
            "PositionID": data['sap_position_id'],
        }
        # Add fields that you want to update a dict (adding to body itself is too much text)
        fields_to_update = {}
        fields_to_update.update(overload_fields) if overload_fields is not None else ''

        # Update the request body with update fields
        base_body.update(fields_to_update)

        response = self.base_class.post_data(uri='WorkcenterPost/*', data=data, return_key=None)
        return response

