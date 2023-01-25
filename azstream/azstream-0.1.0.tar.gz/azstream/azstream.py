import pathlib, logging, schedule, threading, time
from datetime import timedelta
from typing import Any, Dict, Union
from .utils import get_appdir
from .platforms import Platform, Noovo, Crave, TOUTV, AuthenticationMethod


logging.getLogger('requests').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)
logging.getLogger('schedule').setLevel(logging.WARNING)
logging.getLogger('charset_normalizer').setLevel(logging.WARNING)


APP_NAME = 'PyStream'
DEFAULT_CACHE_DIR = 'Cache'


class AZStream():

    def __init__(
        self, 
        cache: bool = True,
        cache_location: str = None,
        tick_rate: int = 300
    ):
        # Cache options
        self.cache = cache
        if self.cache:
            if cache_location is None: 
                self.cache_location = get_appdir(APP_NAME) / DEFAULT_CACHE_DIR
            else:
                self.cache_location = pathlib.Path(cache_location)
        else:
            self.cache_location = None
        
        # Platforms options
        self.platforms: Dict[str, Platform] = {}

        # Other attributes
        self.logger = logging.getLogger('pystream')

        # Timer
        self.schedule = schedule.every(tick_rate).seconds.do(self.tick)
        self.schedule_flag = None
        self.run_schedule()


    def run_schedule(self):
        if self.schedule_flag is not None:
            return

        self.schedule_flag = True

        class ScheduleThread(threading.Thread):
            @classmethod
            def run(cls):
                while self and self.schedule_flag:
                    schedule.run_pending()
                    time.sleep(1)


        self.schedule_thread = ScheduleThread()
        self.schedule_thread.start()


    def __del__(self):
        self.schedule_flag = False
        schedule.cancel_job(self.schedule)


    def tick(self):
        ''''''
        for platform in self.platforms.values():
            try:
                platform.tick()
            except Exception as e:
                self.logger.error(f'An error occured running automated job on platform "{platform.id}"')
                self.logger.error(str(e))



    def add_platform(self, 
        platform: str, 
        id: str = None,
        authentication_method: AuthenticationMethod = AuthenticationMethod.NONE,
        authentication_data: Dict[str, Any] = {},
        keep_authenticated: bool = True,
        refresh_authentication_when_expiring_in: timedelta = timedelta(minutes=30),
        platform_options: Dict[str, Any] = {}
    ) -> Platform:
        # Verify that no other platform uses the same ID
        if id is None:
            id = platform.lower()
        if self.platforms.get(id) is not None:
            raise Exception(f'Another platform uses the ID {id}, please choose another ID.')
        
        # Generate the object
        platform_obj = None
        args = ()
        kwargs = {
            'id': id,
            'cache_location': self.cache_location / 'platforms' / id if self.cache else None,
            'keep_authenticated': keep_authenticated,
            'refresh_authentication_when_expiring_in': refresh_authentication_when_expiring_in,
            'authentication_method': authentication_method,
            'authentication_data': authentication_data,
            'platform_options': platform_options
        }
        if platform.lower() == 'noovo':
            platform_obj = Noovo(*args, **kwargs)
        elif platform.lower() == 'crave':
            platform_obj = Crave(*args, **kwargs)
        elif platform.lower() == 'toutv':
            platform_obj = TOUTV(*args, **kwargs)
        else:
            raise Exception(f'The platform {platform} is not supported yet.')
        
        # Assign the object to the ID
        self.platforms[id] = platform_obj
        return self.platforms[id]

        
    def get_platform(self, id: str) -> Union[Platform, None]:
        return self.platforms.get(id)


    def remove_platform(self, id: str):
        if id in self.platforms:
            del self.platforms[id]