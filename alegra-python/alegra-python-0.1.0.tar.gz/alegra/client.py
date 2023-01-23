import base64
import json

import requests

from alegra.exceptions import UnauthorizedError, WrongFormatInputError, ContactsLimitExceededError


class Client(object):
    URL = "https://api.alegra.com/api/v1/"
    headers = {"Content-Type": "application/json", "Accept": "application/json"}

    def __init__(self, email, token):
        api_key = base64.b64encode(f"{email}:{token}".encode()).decode()
        self.headers.update(Authorization=f"Basic {api_key}")

    def get_company_info(self):
        return self.get("company")

    def get_current_user(self):
        return self.get("users/self")

    def list_contacts(self, order_field=None, order="ASC", limit=None, start=None):
        params = {"order_direction": order, "order_field": order_field, "limit": limit, "start": start}
        return self.get("contacts", params=params)

    def create_contact(self, contact):
        """
        Contact must be a dict object, check README for an example.
        """
        return self.post("contacts", data=json.dumps(contact))

    def list_items(self, order_field=None, order="ASC", limit=None, start=None):
        params = {"order_direction": order, "order_field": order_field, "limit": limit, "start": start}
        return self.get("items", params=params)

    def create_item(self, item):
        """
        Item must be a dict object, check README for an example.
        """
        return self.post("items", data=json.dumps(item))

    def list_item_categories(self):
        return self.get("item-categories")

    def list_warehouses(self):
        return self.get("warehouses")

    def list_item_custom_fields(self):
        return self.get("custom-fields")

    def list_variant_attributes(self):
        return self.get("variant-attributes")

    def list_sellers(self):
        return self.get("sellers")

    def list_price_lists(self):
        return self.get("price-lists")

    def list_terms(self):
        return self.get("terms")

    def list_accounts(self, format_acc="tree", type_acc=None):
        params = {"format": format_acc, "type": type_acc}
        return self.get("categories", params=params)

    def list_taxes(self):
        return self.get("taxes")

    def get(self, endpoint, **kwargs):
        response = self.request("GET", endpoint, **kwargs)
        return self.parse(response)

    def post(self, endpoint, **kwargs):
        response = self.request("POST", endpoint, **kwargs)
        return self.parse(response)

    def delete(self, endpoint, **kwargs):
        response = self.request("DELETE", endpoint, **kwargs)
        return self.parse(response)

    def put(self, endpoint, **kwargs):
        response = self.request("PUT", endpoint, **kwargs)
        return self.parse(response)

    def patch(self, endpoint, **kwargs):
        response = self.request("PATCH", endpoint, **kwargs)
        return self.parse(response)

    def request(self, method, endpoint, headers=None, **kwargs):

        if headers:
            self.headers.update(headers)

        return requests.request(method, self.URL + endpoint, headers=self.headers, **kwargs)

    def parse(self, response):
        status_code = response.status_code
        if "Content-Type" in response.headers and "application/json" in response.headers["Content-Type"]:
            try:
                r = response.json()
            except ValueError:
                r = response.text
        else:
            r = response.text
        if status_code == 200:
            return r
        if status_code == 204:
            return None
        if status_code == 400:
            raise WrongFormatInputError(r)
        if status_code == 401:
            raise UnauthorizedError(r)
        if status_code == 406:
            raise ContactsLimitExceededError(r)
        if status_code == 500:
            raise Exception
        return r
