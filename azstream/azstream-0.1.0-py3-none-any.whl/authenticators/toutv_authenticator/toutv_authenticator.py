from typing import Any, Dict
import requests, uuid
from datetime import timedelta
from ..jwt_authenticator import JwtAuthenticator
from .requests import get_login_request_data, get_refresh_request_data,\
                      get_profile_request_data


DEFAULT_DEVICE_ID     = '61bvnYAaEoCnwRTwVqibYd'

class TOUTVAuthenticator(JwtAuthenticator):

    def __init__(self, 
        platform_id: str,
        refresh_authentication_when_expiring_in: timedelta,
        authentication_data: Dict[str, Any],
        app_user_agent: str,
        ropc_url: str,
        ropc_scopes: str,
        ropc_app_id: str,
        device_type: str,
        client_id: str,
        client_secret: str,
        device_id: str = DEFAULT_DEVICE_ID,
    ):
        super(JwtAuthenticator, self).__init__(platform_id, refresh_authentication_when_expiring_in)

        # Authentication parameters
        self.app_user_agent = app_user_agent
        self.device_type = device_type
        self.device_id      = device_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.ropc_url = ropc_url
        self.ropc_scopes = ropc_scopes
        self.ropc_app_id = ropc_app_id

        # Account authentication
        self.username = authentication_data['username']
        self.password = authentication_data['password']
        self.access_token = ''
        self.refresh_token = ''
        self.profile_infos = ''
        self.available_channels = ['extra']
        self.unauthenticated_channels = []
        self.load_from_cache(authentication_data.get('cache'))


    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    # Authentication actions                                                      #
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #


    def authenticate(self) -> bool:
        '''
        This method will authenticate the user in.
        '''

        try:

            # 1. Username/Password Login
            self.logger.debug('  Authenticating using username and password')
            body, headers = get_login_request_data(
                username=self.username,
                password=self.password,
                scopes=self.ropc_scopes,
                client_id=self.client_id,
                client_secret=self.client_secret,
                device_type=self.device_type,
                app_user_agent=self.app_user_agent
            )
            resp = requests.post(self.ropc_url, headers=headers, data=body)
            if resp.status_code != 200:
                if 'Check your email and password' in resp.text:
                    raise Exception('Username/password combination is not valid.')
                else:
                    raise Exception('An error occured while authenticating using the username and password: ' + resp.text)
            parsed_resp = resp.json()
            self.access_token  = parsed_resp['access_token']
            self.refresh_token = parsed_resp['refresh_token']

           # 2. Get profile infos
            self.logger.debug('  Fetching profile infos')
            url, headers = get_profile_request_data(self.access_token, self.device_id)
            resp = requests.get(url, headers=headers)
            if resp.status_code != 200:
                raise Exception('An error occured while getting user profile infos: ' + resp.text)
            self.profile_infos = resp.json()

            # 3. Print session infos
            self.logger.info('Session established.')
            self.logger.debug(str(self.get_status()))

            return True

        except Exception as e:
            self.logger.error(str(e))
            return False
    

    def refresh(self):
        '''
        This method will refresh the authtication tokens.
        '''

        try:

            # 1. Access token refresh
            self.logger.debug('  Refreshing access token...')
            body, headers = get_refresh_request_data(
                refresh_token=self.refresh_token,
                app_user_agent=self.app_user_agent,
                device_type=self.device_type
            )
            resp = requests.post(self.ropc_url, headers=headers, data=body)
            if resp.status_code != 200:
                raise Exception('An error occured while refreshing tokens: ' + resp.text)
            parsed_resp = resp.json()
            self.access_token  = parsed_resp['access_token']
            self.refresh_token = parsed_resp['refresh_token']

            # 2. Fetch profile infos
            self.logger.debug('  Fetching profile infos...')
            url, headers = get_profile_request_data(self.access_token, self.device_id)
            resp = requests.get(url, headers=headers)
            if resp.status_code != 200:
                raise Exception('An error occured while getting user profile infos: ' + resp.text)
            self.profile_infos = resp.json()

            # 3. Print session infos
            self.logger.info('Session refreshed.')
            self.logger.debug(str(self.get_status()))
            return True

        except Exception as e:
            self.logger.error(str(e))
            return False


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
        cache_data['type'] = 'toutv'
        cache_data['profile_infos'] = self.profile_infos
        return cache_data


    def load_from_cache(self, cache_data: Dict[str, Any] = None) -> bool:
        """
        Try to load session from the provided cache data.

        Args:
            cache_data (Dict[str, Any], optional): Data fetched from the cache
            to be used to retrieve the session.
        """        

        # If a cache data is provided and the cache type is valid with the
        # current authenticator, load the data from it
        if cache_data and \
           cache_data.get('type') == 'toutv' and \
           cache_data.get('access_token') and \
           cache_data.get('refresh_token') and \
           cache_data.get('profile_infos'):

            # Set the data fetched from the cache
            self.access_token  = cache_data.get('access_token')
            self.refresh_token = cache_data.get('refresh_token')
            self.profile_infos = cache_data.get('profile_infos')
            self.logger.info('Session infos fetched from cache.')

        # Run a tick to ensure run needed authentication
        return self.tick(True)




    

    


