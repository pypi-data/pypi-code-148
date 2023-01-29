import datetime
from typing import List

import requests

from .models import TypeMessage, StatusMessage, Response, Scope, Gender


class SigmaSMS:
    __debug: bool
    __token: str
    __sender: str
    __base_url: str = 'https://online.sigmasms.ru/api/'

    def __init__(self, debug: bool, sender: str, api_token: str):
        self.__debug = debug
        self.__sender = sender
        self.__token = api_token
        self.__headers: dict = {
            'Content-Type': 'application/json',
            'Authorization': self.__token
        }

    def _get_params(self, order: str = None, scope: Scope = None, offset: int = None, limit: int = None):
        params = {}
        if order:
            params['$order'] = order
        if scope:
            params['$scope'] = scope.value
        if offset:
            params['$offset'] = offset
        if limit:
            params['$limit'] = limit
        return params

    def send_sms(self, recipient: str | List[str], text: str) -> Response:
        """
        Send SMS message
        :param recipient: recipient's number or list of recipient numbers
        :param text: message text
        """
        if not self.__debug:
            url = f'{self.__base_url}sendings'
            message = {
                "recipient": recipient,
                "type": TypeMessage.SMS.value,
                "payload": {
                    "sender": self.__sender,
                    "text": text
                }
            }
            response = requests.post(url, json=message, headers=self.__headers)
            return Response(response.status_code, response.json())
        else:
            return Response(
                200,
                {'id': '', 'recipient': recipient, 'status': StatusMessage.SENT}
            )

    def send_viber(self, recipient: str | List[str], text: str) -> Response:
        """
        Send Viber message
        :param recipient: recipient's number or list of recipient numbers
        :param text: message text
        """
        if not self.__debug:
            url = f'{self.__base_url}sendings'
            message = {
                "recipient": recipient,
                "type": TypeMessage.VIBER.value,
                "payload": {
                    "sender": self.__sender,
                    "text": text,
                }
            }
            response = requests.post(url, json=message, headers=self.__headers)
            return Response(response.status_code, response.json())
        else:
            return Response(200, {'id': '', 'recipient': recipient, 'status': StatusMessage.SENT})

    def send_vk(self, recipient: str | List[str], text: str) -> Response:
        """
        Send VK message
        :param recipient: recipient's number or list of recipient numbers
        :param text: message text
        """
        if not self.__debug:
            url = f'{self.__base_url}sendings'
            message = {
                "recipient": recipient,
                "type": TypeMessage.VK.value,
                "payload": {
                    "sender": self.__sender,
                    "text": text
                }
            }
            response = requests.post(url, json=message, headers=self.__headers)
            return Response(response.status_code, response.json())
        else:
            return Response(200, {'id': '', 'recipient': recipient, 'status': StatusMessage.SENT})

    def get_message(self, id: str) -> Response:
        """Get message by message's id"""
        url = f'{self.__base_url}sendings/{id}'
        response = requests.get(url, headers=self.__headers)
        return Response(response.status_code, response.json())

    def get_messages(self, order: str = None, scope: Scope = None, offset: int = None, limit: int = None) -> Response:
        """
        Get all messages
        :param offset: from 0
        :param limit: from 1 to 500
        """
        url = f'{self.__base_url}sendings'
        params = self._get_params(order=order, scope=scope, offset=offset, limit=limit)
        response = requests.get(url, params=params, headers=self.__headers)
        return Response(response.status_code, response.json())

    def get_user(self, user_id: str) -> Response:
        """Get user by user's id"""
        url = f'{self.__base_url}users/{user_id}'
        response = requests.get(url, headers=self.__headers)
        return Response(response.status_code, response.json())

    def get_contact_lists(self, order: str = None, scope: Scope = None, offset: int = None,
                          limit: int = None) -> Response:
        """Get all contact lists"""
        url = f'{self.__base_url}contactLists'
        params = self._get_params(order=order, scope=scope, offset=offset, limit=limit)
        response = requests.get(url, params=params, headers=self.__headers)
        return Response(response.status_code, response.json())

    def get_contact_list(self, id: str, scope: Scope = None) -> Response:
        """Get contact list by contact list's id"""
        url = f'{self.__base_url}contactLists/{id}'
        params = self._get_params(scope=scope)
        response = requests.get(url, params=params, headers=self.__headers)
        return Response(response.status_code, response.json())

    def create_contact(self, phone: str, contact_list_id: str,
                       email: str = None, firstName: str = None,
                       lastName: str = None, middleName: str = None,
                       date: datetime.date = None, gender: Gender = None,
                       **other) -> Response:
        """Create contact"""
        if gender:
            gender = gender.value
        contact = {
            'phone': phone,
            'email': email,
            'firstName': firstName,
            'lastName': lastName,
            'middleName': middleName,
            'date': date.isoformat() if date else None,
            'gender': gender,
            'ListId': contact_list_id,
        }
        contact.update(other)

        if not self.__debug:
            url = f'{self.__base_url}contacts'
            response = requests.post(url, json=contact, headers=self.__headers)
            return Response(response.status_code, response.json())
        else:
            contact['id'] = ''
            return Response(200, contact)

    def get_contacts(self, contact_list_id: str) -> Response:
        """Get all contacts in contact list"""
        url = f'{self.__base_url}contacts'
        response = requests.get(url, params={'ListId': contact_list_id}, headers=self.__headers)
        return Response(response.status_code, response.json())

    def delete_contact(self, contact_id: str):
        """Get contact by contact's id"""
        if not self.__debug:
            url = f'{self.__base_url}contacts/{contact_id}'
            response = requests.delete(url, headers=self.__headers)
            return Response(response.status_code, response.json())
        else:
            return Response(200, {'id': contact_id})
