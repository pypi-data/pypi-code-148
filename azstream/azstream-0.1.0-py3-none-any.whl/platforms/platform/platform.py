import pathlib, json, logging
from datetime import timedelta
from typing import Dict, Any, List, Union
from abc import ABC
from ...authenticators import SessionStatus
from ...authenticators import Authenticator, UnauthenticatedAuthenticator
from ..authentication_method import AuthenticationMethod
from ...types import SearchResult, Title


class Platform(ABC):

    def __init__(self, 
        id: str, 
        cache_location: pathlib.Path,
        keep_authenticated: bool,
        refresh_authentication_when_expiring_in: timedelta,
        authentication_method: AuthenticationMethod,
        authentication_data: dict[str, any],
        platform_options: dict[str, any]
    ):
        """
        Initializes a new Platform object.

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
            platform_options (Dict[str, Any]): All authentication parameters.
        """

        # Arguments
        self.id = id
        self.tag = 'unknown'
        self.cache_location = cache_location
        self.logger = logging.getLogger(id)
        self.keep_authenticated = keep_authenticated
        self.refresh_authentication_when_expiring_in = refresh_authentication_when_expiring_in
        self.authentication_method = authentication_method
        self.authentication_data = authentication_data
        self.platform_options = platform_options

        self.authenticator = UnauthenticatedAuthenticator(self.id, self.refresh_authentication_when_expiring_in)

        # Cache initialization (prior to authenticator since some cache data may be useful)
        if self.cache_location:
            if not self.cache_location.is_dir():
                self.logger.debug('Cache directory does not exist, creating it')
                self.cache_location.mkdir(parents=True)
            else:
                try:
                    self.load_cache_data()
                except Exception as e:
                    self.logger.warn(f'Unable to load session from cache: {str(e)}')


    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    # Getters/setters                                                             #
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #


    def get_authenticator(self) -> Authenticator:
        return self.authenticator

    
    def get_available_channels(self) -> List[str]:
        return self.authenticator.get_available_channels()


    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    # System methods                                                              #
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #


    def tick(self) -> bool:
        """
        The tick function. Should be called often to ensure that the platform
        stay consistant over time.

        Returns:
            bool: Wether the session is valid after the execution.
        """

        self.logger.debug('Running automated jobs')

        # Run an authenticator tick to ensure that the session stay valid.
        if self.authenticator and self.keep_authenticated:
            return self.authenticator.tick()


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

        return []

    
    def search(self, id: str) -> List[SearchResult]:
        """
        Returns the titles matching the best with the given query in order from
        the most relevant to the less relevant.
        This will return a maximum of 25 results.

        Args:
            query (str): The search query.

        Returns:
            List[SearchResult]: The search results
        """

        return []

    def describe_title(self, id: str) -> Union[Title, None]:
        """
        Returns the detailed title.

        Args:
            id (str): The title ID.

        Returns:
            Title: The detailed title
            None: If the system is unable to get the title details
        """

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

        return {
            'id': self.id,
            'authenticator': self.authenticator.generate_cache_data()
        }

    def save_cache_data(self) -> bool:
        """
        Saves the cache data to the cache file
        """

        if self.cache_location:
            self.logger.debug('Saving session data to cache file')
            cache_data = self.generate_cache_data()
            cache_file = self.cache_location / 'cache.json'
            with open(cache_file, 'w') as f:
                json.dump(cache_data, f, indent=4, default=str)
            

    def load_cache_data(self):
        """
        Loads the data from the cache file.
        """

        self.logger.debug('Loading session data from the cache file')
        cache_file = self.cache_location / 'cache.json'
        if not cache_file.is_file():
            raise Exception('Unable to find the cache file.')
        try:
            # Read cache data from the file
            with open(cache_file, 'r') as f:
                cache_data = json.load(f)
        except:
            raise Exception('An error occured while parsing the cache file.')
        
        if not self.verify_cache_data(cache_data):
            self.logger.warn('Cannot load cache data. New cache data will override the previous ones.')
            return
        
        # Cached authentication data
        self.authentication_data['cache'] = cache_data.get('authenticator', {})


    def verify_cache_data(self, cache_data: Dict[str, Any]) -> bool:
        """
        Verifies if the cache data can be loaded.
        """

        if not 'authenticator' in cache_data:
            return False

        return True