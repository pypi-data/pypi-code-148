from typing import Any, Dict
import requests
from datetime import timedelta
from pypasser import reCaptchaV3
from ..jwt_authenticator import JwtAuthenticator
from .requests import get_captcha_request_data,        get_login_request_data,\
                      get_magic_generate_request_data, get_magic_login_request_data,\
                      get_profile_request_data,        get_refresh_request_data


DEFAULT_WEB_CREDENTIALS = ('usermgt', 'default')
DEFAULT_WEB_USER_AGENT = 'Mozilla/5.0 (Linux; Android 13; SM-S906U Build/TP1A.220624.014; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/109.0.5414.44 Mobile Safari/537.36'


class BellMediaExternalAuthenticator(JwtAuthenticator):

    def __init__(self, 
        platform_id: str,
        refresh_authentication_when_expiring_in: timedelta,
        authentication_data: Dict[str, Any],
        app_headers_tag: str,
        app_credentials: str,
        web_credentials: tuple[str, str] = DEFAULT_WEB_CREDENTIALS,
        web_user_agent: str = DEFAULT_WEB_USER_AGENT
    ):
        super(JwtAuthenticator, self).__init__(platform_id, refresh_authentication_when_expiring_in)

        # Authentication parameters
        self.app_credentials = app_credentials
        self.web_credentials = web_credentials
        self.web_user_agent  = web_user_agent if web_user_agent else DEFAULT_WEB_USER_AGENT,
        self.app_headers_tag = app_headers_tag

        # Account authentication
        self.username = authentication_data['username']
        self.password = authentication_data['password']
        self.access_token = ''
        self.refresh_token = ''
        self.profile_infos = ''
        self.load_from_cache(authentication_data.get('cache'))


    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    # Authentication actions                                                      #
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #


    def authenticate(self) -> bool:
        '''
        This method will authenticate the user in.
        '''

        try:

            # 1. Captcha
            self.logger.debug('  Bypassing Captcha')
            url = get_captcha_request_data()
            try:
                captcha = reCaptchaV3(url)
            except:
                raise Exception('Unable to bypass the Captcha. Anchor URL might have changes.')

            # 2. Username/Password Login
            self.logger.debug('  Authenticating using username and password')
            url, body, headers = get_login_request_data(self.username, 
                                self.password, captcha, self.web_credentials,
                                self.app_headers_tag, self.web_user_agent)
            resp = requests.post(url, headers=headers, data=body)
            if resp.status_code != 200:
                if 'Bad credentials' in resp.text:
                    raise Exception('Username/password combination is not valid.')
                else:
                    raise Exception('An error occured while authenticating using the username and password: ' + resp.text)
            login_token = resp.json()['access_token']
            
            # 3. Generate magic token
            self.logger.debug('  Generating a magic token')
            url, headers = get_magic_generate_request_data(login_token, 
                                    self.app_headers_tag, self.web_user_agent)
            resp = requests.post(url, headers=headers)
            if resp.status_code != 201:
                raise Exception('An error occured while generating the magic token: ' + resp.text)
            magic_token = resp.text.replace('==', '')

            # 4. Login using magic token
            self.logger.debug('  Authenticating using the magic token')
            url, body, headers = get_magic_login_request_data(magic_token, 
                                                            self.app_credentials)
            resp = requests.post(url, headers=headers, data=body)
            if resp.status_code != 200:
                raise Exception('An error occured while authenticating using the magic token: ' + resp.text)
            parsed_resp = resp.json()
            self.access_token  = parsed_resp['access_token']
            self.refresh_token = parsed_resp['refresh_token']

            # 5. Get profile infos
            self.logger.debug('  Fetching profile infos')
            url, headers = get_profile_request_data(self.access_token)
            resp = requests.get(url, headers=headers)
            if resp.status_code != 200:
                raise Exception('An error occured while getting user profile infos: ' + resp.text)
            self.profile_infos = resp.json()[0]

            # 6. Print session infos
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
            url, body, headers = get_refresh_request_data(self.refresh_token, 
                                    self.profile_infos['id'], self.app_credentials)
            resp = requests.post(url, headers=headers, data=body)
            if resp.status_code != 200:
                raise Exception('An error occured while refreshing tokens: ' + resp.text)
            parsed_resp = resp.json()
            self.access_token  = parsed_resp['access_token']
            self.refresh_token = parsed_resp['refresh_token']

            # 2. Fetch profile infos
            self.logger.debug('  Fetching profile infos...')
            url, headers = get_profile_request_data(self.access_token)
            resp = requests.get(url, headers=headers)
            if resp.status_code != 200:
                raise Exception('An error occured while getting user profile infos: ' + resp.text)
            self.profile_infos = resp.json()[0]

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
        cache_data['type'] = 'bellmedia_external'
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
           cache_data.get('type') == 'bellmedia_external' and \
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




    

    


