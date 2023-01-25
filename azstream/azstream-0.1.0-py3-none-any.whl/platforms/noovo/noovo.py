from ..platform import Platform
from ..authentication_method import AuthenticationMethod
from ...authenticators import BellMediaExternalAuthenticator


PLATFORM_NAME = 'noovo'


class Noovo(Platform):


    def __init__(self, *args, **kwargs):
        """
        Initializes a new Noovo Platform object.

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

        super(Noovo, self).__init__(*args, **kwargs)

        self.tag = PLATFORM_NAME

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
            if provider == 'bellmedia':
                self.authenticator = BellMediaExternalAuthenticator(
                    platform_id=self.id, 
                    refresh_authentication_when_expiring_in=self.refresh_authentication_when_expiring_in,
                    authentication_data=self.authentication_data,
                    app_headers_tag='com.vmediagroup.noovo',
                    app_credentials=('noovo-android', 'default'),
                    web_user_agent=self.authentication_data.get('web_user_agent', None)
                )
            else:
                raise Exception(f'The provider "{provider}" is not supported.')
        
        # Cache
        self.save_cache_data()