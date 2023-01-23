import os
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient
from salure_helpers.salureconnect import SalureConnect
from lxml import etree
import pandas_read_xml as pdx
import pandas as ps
import requests
import json


class BaseFunctions(SalureConnect):
    def __init__(self, label: str, data_dir: str, certificate_file: str = None, key_file: str = None, debug: bool = False):
        """
        The SAP class is used to get the access token for the SAP connection.
        :param label: The label of the SAP connection in SalureConnect
        :param data_dir: The directory where the data will be stored. Needed for pandas to read the XML file
        :param certificate_file: The certificate file: open(file, 'rb')
        :param key_file: The key file in bytes format: open(file, 'rb')
        """
        super().__init__()
        credentials = self.get_system_credential(system='sap', label=label)
        self.base_url = credentials['base_url']
        self.headers = self.get_authorization_headers(credentials['client_id'], credentials['authorisation_url'], certificate_file, key_file)
        self.data_dir = data_dir
        self.debug = debug

    def get_authorization_headers(self, client_id, authorisation_url, certificate_file, key_file):
        """
        Get the access token from the endpoint
        1) Visit salureconnect to get the base_url, autorisation_url and client_id
        2) Get the access token from the endpoint using the client_id and certificate files
        :return: returns the retrieved access_token
        """
        client = BackendApplicationClient(client_id=client_id)
        oauth = OAuth2Session(client=client)
        token = oauth.fetch_token(token_url=authorisation_url,
                                  include_client_id=True,
                                  cert=(certificate_file, key_file))
        headers = {
            'Authorization': f'Bearer {token["access_token"]}',
            'Content-Type': 'application/json'
        }
        return headers

    def get_data(self, uri: str, filter: str = None, xml_root: str = None):
        """
        :param uri: The endpoint to call
        :param xml_root: the response from SAP comes within XML format. Give the root of the XML file from which you want to get the data
        :param filter: filter for the endpoint
        :return: a pandas dataframe with the content from the called endpoint
        i.e. fetch_data('OrgStructureSet', xml_root='OrgStructures', filter="Startdate eq '2022-01-01'")
        """
        url = f"{self.base_url}/{uri}?$filter={filter}" if filter is not None else f"{self.base_url}/{uri}"
        response = requests.request("GET", f"{url}", headers=self.headers, data={})
        response.raise_for_status()
        if self.debug:
            print(response.text)
        with open(f"{self.data_dir}/{uri}.xml", 'wb') as file:
            file.write(response.content)
        df = pdx.read_xml(f"{self.data_dir}/{uri}.xml", [xml_root], root_is_rows=False)
        df = df.pipe(pdx.fully_flatten).reset_index(drop=True)
        return df

    def get_batch_data(self, uri: str, filter: str, id_key: str, id_list: list, batch_size: int = 10, xml_root: str = None):
        """
        In some cases you want to get a lot of data from the endpoint. This function will combine a lot of calls for you into one dataframe
        SAP is not able to do this itself.
        :param uri: The URI you want to get the data from
        :param filter: The filter you want to use to filter the data on
        :param id_key: The key for all the ID's you want to get the data from. i.e. 'employee_id'
        :param id_list: A list of all the ID's you want to get the data from. i.e. ['123456', '654321']
        :param batch_size: the number of ID's you want to get the data from in one call. by default 10
        :param xml_root: the response from SAP comes within XML format. Give the root of the XML file from which you want to get the data
        :return: a Pandas dataframe with the data from the endpoint
        """
        # Put all the given ID's in one list
        id_batches = [id_list[i:i + batch_size] for i in range(0, len(id_list), batch_size)]
        df = pd.DataFrame()
        for i, id_batch in enumerate(id_batches):
            # Creat the filter for each batch
            temp_filter = ''
            for id in id_batch:
                temp_filter += f"{id_key} eq '{id}' or "
            final_filter = f"({temp_filter[:-4]}) and {filter}"

            # Now call the simple get_data endpoint
            df_tmp = self.get_data(uri=uri, xml_root=xml_root, filter=final_filter)
            df = pd.concat([df, df_tmp], axis=0)
        return df

    def post_data(self, uri: str, data: dict, filter: str = None, return_key: str = None):
        """
        Post data to the endpoint in SAP. For many endpoint, SAP returns an ID for the created object. This function will add the ID to the response so you can re-use it.
        :param uri: The endpoint to call
        :param data: The body of the request filled with the data you want to post
        :param filter: The filter you want to use to filter the data on
        :param return_key: The key of the ID you expect SAP to return after the POST. i.e. 'employee_id'
        :return: An ID if return_key is given, otherwise the response from SAP
        """
        url = f"{self.base_url}/{uri}?$filter={filter}" if filter is not None else f"{self.base_url}/{uri}"
        response = requests.request("POST", url, headers=self.headers, data=json.dumps(data))
        response.raise_for_status()
        if self.debug:
            return response
        # Don't use raise_for_status() here because the errors from SAP will come in XML format which can be parsed here
        if 200 <= response.status_code < 300:
            if len(response.text) == 0 or return_key is None:
                return response
            elif response.text.startswith('{'):
                response = json.loads(response.text)
                return_id = response[return_key]
                return return_id
            else:
                doc = etree.XML(response.content)
                return_id = doc.getchildren()[0].find(return_key).text
                return return_id
        else:
            # The error message is in XML format, follows the below steps to extract the error message
            if len(response.text) > 0:
                doc = etree.XML(response.content)
                error_code = doc.getchildren()[0].text
                error_message = doc.getchildren()[1].text
                raise ConnectionError(f'Error from SAP while calling endpoint {uri}. The message is \"{error_message}\" with code {error_code}')
            else:
                raise ConnectionError(f'Error from SAP while calling endpoint {uri}. There is no message with code {response.status_code}')

    def delete_data(self, uri: str, filter: str):
        """
        Delete data from the endpoint based on a filter. Be aware that for some endpoints you really delete the data but for others
        you will only delimit the selected dataset with an enddate but the data will still exist
        :param uri: The endpoint to call
        :param filter: The filter to delete the data on
        :return: the response from the call
        """
        url = f"{self.base_url}/{uri}?$filter={filter}" if filter is not None else f"{self.base_url}/{uri}"
        response = requests.request("DELETE", f"{url}", headers=self.headers)
        return response
