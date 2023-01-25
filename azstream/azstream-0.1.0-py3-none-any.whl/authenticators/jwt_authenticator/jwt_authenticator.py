from typing import Any, Dict, List
import jwt
from datetime import timedelta, datetime
from abc import ABC
from ..auth_status import AuthStatus, SessionStatus
from ..authenticator import Authenticator


class JwtAuthenticator(Authenticator, ABC):

    def __init__(self, 
        platform_id: str,
        refresh_authentication_when_expiring_in: timedelta
    ):
        """
        Initializes a new JwtAuthenticator object.
        The JwtAuthenticator can be used as a base to develop an authenticator
        that uses JWT tokens for authentication.

        Args:
            platform_id (str): the platform ID
            refresh_authentication_when_expiring_in (timedelta): The expires in
                trigger value to refresh the session automatically.
        """ 

        super(JwtAuthenticator, self).__init__(platform_id, refresh_authentication_when_expiring_in)
        self.access_token = ''
        self.refresh_token = ''
        self.unauthenticated_channels = []


    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    # Getters/setters                                                             #
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #


    def get_available_channels(self) -> List[str]:
        """
        Return the channels available to the user.
        By default, this list is empty.

        Returns:
            List[str]: The available channels
        """

        if self.get_status().session_status in (SessionStatus.HEALTY, SessionStatus.EXPIRING):
            return self.available_channels
        else:
            return self.unauthenticated_channels


    def get_token(self) -> Any:
        """
        This method will return the updated token from the authenticator.
        If the UnauthenticatedAuthenticator is used, this will return None.
        If the user session is not valid, this will return None.

        Returns:
            Any: The token or any form of authentication needed.
        """

        status = self.get_status()
        if status.session_status == SessionStatus.HEALTY:
            return self.access_token
        
        elif status.session_status in (SessionStatus.EXPIRING, SessionStatus.EXPIRED):
            if self.tick():
                return self.access_token
            else:
                return None
        
        else:
            return None



    def get_status(self, silent: bool = False) -> AuthStatus:
        """
        Returns the authentication status.

        Returns:
            AuthStatus: The authentication status
        """

        # If the parent detects an error state, don't try to do anything else
        auth_status = super().get_status(silent)
        if auth_status.session_status == SessionStatus.ERROR:
            return auth_status

        # Else, check the tokens validity
        now_dt = datetime.utcnow()
        try:
            access_token_data  = jwt.decode(self.access_token,  verify=False)
            access_token_expiry  = datetime.utcfromtimestamp(access_token_data['exp'])
        except:
            if not silent:
                self.logger.error('Unable to parse the access token, considering it as expired.')
            access_token_expiry = now_dt - timedelta(hours=1)
        # If no refresh token, consider it expired
        if not self.refresh_token:
            refresh_token_expiry = now_dt - timedelta(hours=1)
        else:
            try:
                refresh_token_data = jwt.decode(self.refresh_token, verify=False)
                refresh_token_expiry = datetime.utcfromtimestamp(refresh_token_data['exp'])
            except:
                # Being unable to parse the refresh token is usual and we can
                # consider them `always valid`
                refresh_token_expiry = datetime(year=2099, month=1, day=1)
        auth_status.expires_in = access_token_expiry - now_dt
        auth_status.can_refresh = True

        # Access token expired
        if access_token_expiry < now_dt:
            auth_status.session_status = SessionStatus.EXPIRED
            # Refresh token expired (refresh is impossible)
            if refresh_token_expiry < now_dt:
                auth_status.can_refresh = False
        # Access token not expired, but expires soon
        elif auth_status.expires_in < self.refresh_authentication_when_expiring_in:
            auth_status.session_status = SessionStatus.EXPIRING
            # Refresh token expired (refresh is impossible)
            if refresh_token_expiry < now_dt:
                auth_status.can_refresh = False
        
        return auth_status


    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    # Authentication actions                                                      #
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #


    def authenticate(self) -> bool:
        """
        Authenticates the user based on the authenticator method. Unlike the
        base authenticator, the JWT authenticator will return False by default
        unless an implementation is available.

        Returns:
            bool: Wether the authentication has succeed or not
        """
        return False


    def refresh(self) -> bool:
        """
        Refreshes the session. Unlike the base authenticator, the JWT
        authenticator will return False by default unless an implementation
        is available.

        Returns:
            bool: Wether the refresh has succeed or not
        """
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
        cache_data['access_token']  = self.access_token
        cache_data['refresh_token'] = self.refresh_token
        return cache_data
