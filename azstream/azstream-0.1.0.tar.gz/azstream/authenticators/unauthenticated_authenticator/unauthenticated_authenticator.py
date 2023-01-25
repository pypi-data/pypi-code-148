from datetime import timedelta
from typing import Any, Dict, List
from ..authenticator import Authenticator


class UnauthenticatedAuthenticator(Authenticator):

    def __init__(self,
        platform_id: str,
        refresh_authentication_when_expiring_in: timedelta,
        available_channels: List[str] = []
    ):
        """
        Initializes a new UnauthenticatedAuthenticator object.
        The UnauthenticatedAuthenticator can be used on Platform that requires
        no authentication or gives a limited access to unauthenticated users.

        Args:
            platform_id (str): the platform ID
            refresh_authentication_when_expiring_in (timedelta): The expires in
            trigger value to refresh the session automatically.
            available_channels (timedelta): If an unauthenticated user has
            access to a limited set of channels, they have to be provided.
        """ 
        
        super().__init__(platform_id, refresh_authentication_when_expiring_in)
        self.available_channels = available_channels


    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    # Getters/Setters                                                             #
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #


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
            'type': 'unauthenticated'
        }
