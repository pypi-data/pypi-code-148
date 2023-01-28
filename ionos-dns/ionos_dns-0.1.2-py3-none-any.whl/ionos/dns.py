"""
Python module to interact with the IONOS DNS Beta API
"""

from typing import Any, Dict, List, Optional

import requests


class APIError(Exception):
    """ IONOS API Error """

    def __init__(self, msg, details=None):
        super().__init__(msg)
        self.details = details


def _handle_error(response: requests.Response,
                  ok_result: Any = None,
                  success_code: int = 200):
    if response.status_code == success_code:
        if response.text == "":
            return ok_result
        return response.json()
    error = response.json()[0]
    raise APIError(error['code'], error)


class DNS:
    """ Class to interact with the IONOS DNS Beta API """

    def __init__(self, api_key: str):
        self._api_key = api_key
        self._url = 'https://api.hosting.ionos.com'
        self._headers = {'X-API-Key': self._api_key}
        self._timeout = 30

    def _get(self, api: str, params: Dict[str, Any] = None):
        return requests.get(f'{self._url}/{api}',
                            params=params,
                            headers=self._headers,
                            timeout=self._timeout)

    def _delete(self, api: str):
        return requests.delete(f'{self._url}/{api}',
                               headers=self._headers,
                               timeout=self._timeout)

    def _patch(self, api: str, body: str):
        return requests.patch(f'{self._url}/{api}',
                              json=body,
                              headers=self._headers,
                              timeout=self._timeout)

    def _put(self, api: str, body):
        return requests.put(f'{self._url}/{api}',
                            json=body,
                            headers=self._headers,
                            timeout=self._timeout)

    def _post(self, api: str, body):
        return requests.post(f'{self._url}/{api}',
                             json=body,
                             headers=self._headers,
                             timeout=self._timeout)

    def list_zones(self) -> List[Dict[str, Any]]:
        """ Returns list of customer zones. """
        return _handle_error(self._get('dns/v1/zones'))

    def get_zone(self,
                 zone_id: str,
                 suffix: Optional[str] = None,
                 record_name: Optional[str] = None,
                 record_type: Optional[str] = None) -> Dict[str, Any]:
        """ Returns a customer zone. """
        params = {}
        if suffix is not None:
            params['suffix'] = suffix
        if record_name is not None:
            params['recordName'] = record_name
        if record_type is not None:
            params['recordType'] = record_type
        result = self._get(f'dns/v1/zones/{zone_id}', params=params)
        return _handle_error(result)

    def batch_update_records(self, zone_id: str,
                             record_list: List[Dict[str, Any]]) -> None:
        """
        Replaces all records of the same name and type with the ones provided.
        """
        result = self._patch(f'dns/v1/zones/{zone_id}', body=record_list)
        return _handle_error(result)

    def batch_replace_records(self, zone_id: str,
                              record_list: List[Dict[str, Any]]) -> None:
        """ Replaces all records in the zone with the ones provided """
        result = self._put(f'dns/v1/zones/{zone_id}', body=record_list)
        return _handle_error(result)

    def create_records(self, zone_id: str,
                       record_list: List[Dict[str, Any]]) -> None:
        """ Creates records for a customer zone. """
        result = self._post(f'dns/v1/zones/{zone_id}/records', record_list)
        return _handle_error(result, success_code=201)

    def get_record(self, zone_id: str, record_id: str) -> Dict[str, Any]:
        """
        Returns the record from the customer zone with the mentioned id.
        """
        result = self._get(f'dns/v1/zones/{zone_id}/records/{record_id}')
        return _handle_error(result, {})

    def delete_record(self, zone_id: str, record_id: str) -> None:
        """ Delete a record from the customer zone. """
        result = self._delete(f'dns/v1/zones/{zone_id}/records/{record_id}')
        return _handle_error(result)

    def update_record(self, zone_id: str, record_id: str,
                      record_update: Dict[str, Any]) -> None:
        """ Update a record from the customer zone. """
        result = self._put(f'dns/v1/zones/{zone_id}/records/{record_id}',
                           record_update)
        return _handle_error(result)

    def enable_dyndns(self, domain_list: List[str],
                      description: str) -> Dict[str, Any]:
        """
        Activate Dynamic Dns for a bundle of (sub)domains. The url from
        response will be used to update the ips of the (sub)domains.
        """
        args = {
            'domains': domain_list,
            'description': description,
        }
        result = self._post('dns/v1/dyndns', args)
        return _handle_error(result)

    def disable_dyndns(self) -> None:
        """ Disable Dynamic Dns """
        result = self._delete('dns/v1/dyndns')
        return _handle_error(result)

    def update_dyndns_entry(self, bulk_id: str, domain_list: List[str],
                            description: str) -> None:
        """ Update Dynamic Dns for bulk id """
        args = {
            'domains': domain_list,
            'description': description,
        }
        result = self._put(f'dns/v1/dyndns/{bulk_id}', args)
        return _handle_error(result)

    def delete_dyndns_entry(self, bulk_id: str) -> None:
        """ Disable Dynamic Dns for bulk id """
        result = self._delete(f'dns/v1/dyndns/{bulk_id}')
        return _handle_error(result)

    @staticmethod
    def _sort_by_name_len(domain_info: Dict[str, Any]) -> int:
        return -len(domain_info['name'])

    def get_zone_id(self, domain_name: str) -> Optional[str]:
        """ Returns the zone id for the given domain """
        domain_info_list = self.list_zones()
        domain_info_list.sort(key=self._sort_by_name_len)
        for domain_info in domain_info_list:
            if domain_name.endswith(domain_info['name']):
                return domain_info['id']
        return None
