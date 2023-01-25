import logging, pathlib
from datetime import timedelta
from abc import ABC, abstractmethod
from typing import Any, Dict, List
from ..auth_status import AuthStatus, SessionStatus
from ...utils.formatting import timedelta_to_hh_mm


MAX_REFRESH_ATTEMPTS = 3
MAX_AUTHENTICATE_ATTEMPTS = 3


class Authenticator(ABC):

    def __init__(self, 
        platform_id: str,
        refresh_authentication_when_expiring_in: timedelta
    ):
        """
        Initializes a new Authenticator object.

        Args:
            platform_id (str): the platform ID
            refresh_authentication_when_expiring_in (timedelta): The expires in
                trigger value to refresh the session automatically.
        """

        self.logger = logging.getLogger(f'{platform_id}-auth')
        self.refresh_authentication_when_expiring_in = refresh_authentication_when_expiring_in
        self.failed_refreshes = 0
        self.failed_authentications = 0
        self.available_channels: List[str] = []


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

        return self.available_channels


    def get_token(self) -> Any:
        """
        This method will return the updated token from the authenticator.
        If the UnauthenticatedAuthenticator is used, this will return None.
        If the user session is not valid, this will return None.

        Returns:
            Any: The token or any form of authentication needed.
        """

        return None


    def get_status(self, silent: bool = False) -> AuthStatus:
        """
        Returns the authentication status.

        Returns:
            AuthStatus: The authentication status
        """
        session_status = SessionStatus.HEALTY
        if self.failed_authentications >= MAX_AUTHENTICATE_ATTEMPTS:
            session_status = SessionStatus.ERROR
        return AuthStatus(
            session_status=session_status,
            expires_in=None,
            can_refresh=False,
            failed_refreshes=self.failed_refreshes,
            failed_authentications=self.failed_authentications
        )


    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    # Authentication actions                                                      #
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #


    def authenticate(self) -> bool:
        """
        Authenticates the user based on the authenticator method.

        Returns:
            bool: Wether the authentication has succeed or not
        """
        return True


    def refresh(self) -> bool:
        """
        Refreshes the session.

        Returns:
            bool: Wether the refresh has succeed or not
        """
        return True


    def reset_error(self):
        """
        This method will reset the error state, allowing the authenticator to
        try to authenticate again after reaching the maximum failures amount.
        """
        self.failed_refreshes = 0
        self.failed_authentications = 0
        self.tick()


    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    # System methods                                                              #
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #


    def tick(self, init_tick: bool = False) -> bool:
        """
        The tick function. Should be called often to ensure the authentication
        stay valid over time. Depending on the refresh trigger value choosed, 
        this function will refresh the token if necessary.

        Returns:
            bool: Wether the session is valid after the execution.
        """

        status = self.get_status(init_tick)

        # 1. Session in an error state, simply write an error in the log
        if status.session_status == SessionStatus.ERROR:
            self.logger.error('Session is in an error state. This is most likely due to invalid authentication options.')
            return False

        # 2. Session is healty, do nothing
        elif status.session_status == SessionStatus.HEALTY:
            if init_tick:
                self.logger.info(str(status))
            return True

        # 3. Session is expired or about to expired, renew it
        elif status.session_status in (SessionStatus.EXPIRING, SessionStatus.EXPIRED):
            if status.session_status == SessionStatus.EXPIRING:
                self.logger.warn(f'Session is expiring in {timedelta_to_hh_mm(status.expires_in)}.')
            elif not init_tick:
                self.logger.warn('Session is expired.')
            # If refreshing is possible and haven't failed before
            if status.can_refresh and self.failed_refreshes < MAX_REFRESH_ATTEMPTS:
                self.logger.warn(f'Refreshing session... (attempt {self.failed_refreshes+1}/{MAX_REFRESH_ATTEMPTS})')
                if not self.refresh():
                    self.failed_refreshes += 1
                    return status.session_status == SessionStatus.EXPIRING # An expiring session can still do requests
                else:
                    self.failed_refreshes = 0
                    self.failed_authentications = 0
                    return True
            # If refreshing isn't possible or have failed before
            elif self.failed_authentications < MAX_AUTHENTICATE_ATTEMPTS:
                self.logger.warn(f'Authenticating session... (attempt {self.failed_authentications+1}/{MAX_AUTHENTICATE_ATTEMPTS})')
                if not self.authenticate():
                    self.failed_authentications += 1
                    return status.session_status == SessionStatus.EXPIRING # An expiring session can still do requests
                else:
                    self.failed_refreshes = 0
                    self.failed_authentications = 0
                    return True
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

        return {
            'type': ''
        }
