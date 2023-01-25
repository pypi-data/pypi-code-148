from typing import Any, Dict, List, Union
import requests, thefuzz.fuzz
from .parsers import parse_search_results, parse_title
from ..platform import Platform
from ..authentication_method import AuthenticationMethod
from ...authenticators import TOUTVAuthenticator
from ...types import SearchResult, Title
from .requests import get_settings_request_data, get_db_request_data,\
                      get_search_request_data,   get_title_request_data


PLATFORM_NAME = 'toutv'

DEFAULT_DEVICE_TYPE = 'phone'
SETTINGS = {
    'phone': {
        'default_app_version': '4.15.2.151',
        'default_android_version': '13', # '8.0.0', '9.0.0', '10', '11', '12', '13'
        'default_client_id': 'd6f8e3b1-1f48-45d7-9e28-a25c4c514c60',
        'user_agent_format': 'ICI Tou.TV-v{app_version}-Android-{android_version}',
        'login_client_id': '6b47a0fc-dd20-4e2e-974f-366a25dcadc0',
        'login_client_secret': '509wUPw4XCv5W~92v~DYq5pK_dRY893.h~'
    },
    'tv': {
        'default_app_version': '4.9.0',
        'default_android_version': '11', # '8.0.0', '9.0.0', '10', '11', '12', '13'
        'default_client_id': '1ba43628-12ee-4dca-88a0-78d37679063f',
        'user_agent_format': 'Tou.TV-v{app_version}-android-{android_version}',
        'login_client_id': '65824cc0-e69f-4298-afc8-1dad7edec765',
        'login_client_secret': None
    }
}


class TOUTV(Platform):


    def __init__(self, *args, **kwargs):
        """
        Initializes a new TOU.TV Platform object.

        Args:
            id (str): The platform ID
            cache_location (pathlib.Path): The location where to store cache.
                Can be None if no cache should be kept.
            keep_authenticated (bool): Wether the system should automatically
                refresh the session before it expires.
            refresh_authentication_when_expiring_in (timedelta): The expires in
                trigger value to refresh the session automatically.
            authentication_method (AuthenticationMethod): The authentication
                method to use. If the method requires parameterers, these
                should be provided in the authentication_data dictionary.
            authentication_data (Dict[str, Any]): All authentication parameters.
        """

        super(TOUTV, self).__init__(*args, **kwargs)

        self.tag = PLATFORM_NAME

        # Parse platform options
        self.device_type = self.platform_options.get('device_type', DEFAULT_DEVICE_TYPE)
        self.app_version = self.platform_options.get('app_version', SETTINGS[self.device_type]['default_app_version'])
        self.android_version = self.platform_options.get('android_version', SETTINGS[self.device_type]['default_android_version'])
        self.login_client_id = self.platform_options.get('login_client_id', SETTINGS[self.device_type]['login_client_id'])
        self.login_client_secret = self.platform_options.get('login_client_secret', SETTINGS[self.device_type]['login_client_secret'])
        self.client_id = SETTINGS[self.device_type]['default_client_id']
        self.app_user_agent = SETTINGS[self.device_type]['user_agent_format'].format(app_version=self.app_version, android_version=self.android_version)

        # Do the settings request
        if not self.update_settings():
            raise Exception('Unable to get client settings.')

        # Initialize the authenticator
        if self.authentication_method == AuthenticationMethod.USER_PASS:

            # Verify authentication data integrity
            provider = self.authentication_data.get('provider')
            if not provider:
                raise Exception('The "USER_PASS" authentication method requires a "provider" argument.')
            elif not self.authentication_data.get('username'):
                raise Exception('The "USER_PASS" authentication method requires a "username" argument.')
            elif not self.authentication_data.get('password'):
                raise Exception('The "USER_PASS" authentication method requires a "password" argument.')

            # Initialize the right authenticator
            if provider == 'direct':
                self.authenticator = TOUTVAuthenticator(
                    platform_id=self.id, 
                    refresh_authentication_when_expiring_in=self.refresh_authentication_when_expiring_in,
                    authentication_data=self.authentication_data,
                    app_user_agent=self.authentication_data.get('app_user_agent', self.app_user_agent),
                    client_id=self.login_client_id,
                    client_secret=self.login_client_secret,
                    device_type=self.device_type,
                    ropc_url = self.ropc_url,
                    ropc_scopes = self.ropc_scopes,
                    ropc_app_id = self.ropc_app_id

                )
            else:
                raise Exception(f'The provider "{provider}" is not supported.')

        # Do the first db update
        self.update_db()
        
        # Cache
        self.save_cache_data()


    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    # System methods                                                              #
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #


    def tick(self):
        """
        The tick function. TOU.TV needs to keep an updated titles table locally
        to allow searches. After every tick, this table should get updated.

        Returns:
            bool: Wether the session is valid after the execution.
        """

        # If parent tick fails, that means that the we cannot update the table
        if not super().tick():
            return False
        return self.update_db()


    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    # Update methods                                                              #
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

    def update_settings(self) -> bool:
        try:
            self.logger.debug('Getting client infos...')
            url, headers = get_settings_request_data(
                device_type=self.device_type, 
                client_id=self.client_id, 
                app_user_agent=self.app_user_agent
            )
            resp = requests.get(url, headers=headers)
            if resp.status_code != 200:
                return False
            parsed_resp = resp.json()
            if self.device_type == 'phone':
                self.client_id = parsed_resp['LoginClientIdAndroid']
                self.user_info_url = parsed_resp['EndpointUserInfoAndroid']
            elif self.device_type == 'tv':
                self.client_id = parsed_resp['LoginClientIdAndroidTv']
                self.user_info_url = parsed_resp['EndpointUserInfoTV']
            self.ropc_app_id = parsed_resp['IdentityManagement']['ROPC']['AppId']
            self.ropc_scopes = parsed_resp['IdentityManagement']['ROPC']['Scopes']
            self.ropc_url    = parsed_resp['IdentityManagement']['ROPC']['Url']
            return True
        except:
            return False

    def update_db(self) -> bool:
        try:
            if self.device_type != 'phone':
                return True
            self.logger.debug('Updating the titles database...')
            url, headers = get_db_request_data(
                device_type=self.device_type,
                client_id=self.client_id,
                app_user_agent=self.app_user_agent
            )
            resp = requests.get(url, headers=headers)
            if resp.status_code != 200:
                return False
            self.db = resp.json()
            return True
        except:
            return False


    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    # Main functions                                                              #
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #


    def search(self, query: str) -> List[SearchResult]:
        """
        Returns the titles matching the best with the given query in order from
        the most relevant to the less relevant.
        This will return a maximum of 25 results.

        Args:
            query (str): The search query.

        Returns:
            List[SearchResult]: The search results
        """
        
        tmp_list = []

        if self.device_type == 'tv':
            '''
            TV Client makes a request every time a search is done.
            '''
            # Make the search request
            url, headers = get_search_request_data(
                device_type=self.device_type,
                client_id=self.client_id,
                app_user_agent=self.app_user_agent,
                query=query
            )
            resp = requests.get(url, headers=headers)
            if resp.status_code != 200:
                return []
            # Rate each result
            for title in resp.json():
                tmp_list.append({'ratio': thefuzz.fuzz.ratio(title['SearchableText'], query), 'title': title})
            
        elif self.device_type == 'phone':
            '''
            Phone Client makes a search locally inside its updated database
            '''
            tmp_list = []
            for title in self.db:
                ratio = thefuzz.fuzz.ratio(title['SearchableText'], query)
                if ratio > 30:
                    tmp_list.append({'ratio': ratio, 'title': title})
        
        tmp_list.sort(reverse=True, key=lambda x: x['ratio'])
        title_list = [x['title'] for x in tmp_list][:25]
        return parse_search_results(self, title_list)


    def describe_title(self, id: str) -> Union[Title, None]:
        """
        Returns the detailed title.

        Args:
            id (str): The title ID.

        Returns:
            Title: The detailed title
            None: If the system is unable to get the title details
        """

        # Get details from the API
        url, headers = get_title_request_data(
                title_id=id,
                device_type=self.device_type,
                client_id=self.client_id,
                app_user_agent=self.app_user_agent
            )
        resp = requests.get(url, headers=headers)
        if resp.status_code != 200:
            self.logger.error(f'Unable to get title details: {resp.text}')
            return None

        # Parse the response
        try:
            return parse_title(self, resp.json())
        except:
            self.logger.error('Unable to parse the title details.')
            return None




    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    # Cache                                                                       #
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #


    def generate_cache_data(self) -> Dict[str, Any]:
        """
        This method will generate the data to be stored in the cache

        Returns:
            Dict[str, Any]: The data to be stored in the cache.
        """

        cache_data = super().generate_cache_data()
        cache_data['device_type'] = self.device_type
        return cache_data
            

    def verify_cache_data(self, cache_data: Dict[str, Any]) -> bool:
        """
        Verifies if the cache data can be loaded.
        """

        if not super().verify_cache_data(cache_data):
            return False

        if not 'device_type' in cache_data:
            return False
        
        if cache_data['device_type'] != self.platform_options.get('device_type', 'none'):
            self.logger.warn('Device type has changed, previous cache data is invalid.')
            return False
        
        return True