"""
@author Victor Valenzuela M
@since 28-12-22
"""

import json
import sys
from pathlib import Path
from inspect import currentframe, getframeinfo
from datetime import datetime
from enum import Enum


DATE_FORMAT = "%d/%m/%Y %H:%M:%S"
LOG_PATH = 'logs/log.ev'

class RType(Enum):
    ERR = 'error'
    WARN = 'warning'
    #INFO = 3

class Registry():
    """
    Clase Base para errores, warnings, info, etc
    """
    r_type:RType
    description:str
    timestamp:datetime
    ex:Exception

    def __init__(
            self,
            r_type:RType,
            description:str='',
            timestamp:datetime=datetime.now(),
            ex:Exception=None
            ) -> None:
        self.r_type = r_type
        self.description = description
        self.timestamp = timestamp
        self.ex = ex
    
    def get_json(self) -> dict:
        frame = currentframe().f_back.f_back.f_back
        tb = getframeinfo(frame)

        information = {}
        information['type'] = self.r_type.value
        information['description'] = self.description
        information['timestamp'] = self.timestamp.strftime(DATE_FORMAT)
        information['line'] = tb.lineno
        information['filename'] = tb.filename.split('\\')[-1]
        information['context'] = frame.f_code.co_qualname
        information['positions'] = tb.positions

        if self.ex is not None:
            information['ex_name'] = self.ex.__class__.__name__
            information['ex_args'] = str(self.ex.args)

        return information

class Priority(Enum):
    LOW = 'low'
    MID = 'mid'
    HIGH = 'high'

class Error(Registry):
    priority:Priority

    def __init__(
            self,
            description:str='',
            timestamp:datetime=datetime.now(),
            ex:Exception=None,
            priority:Priority=Priority.MID
            ) -> None:
        """
        For actions that cause problems, every time!

        Args:
            description (str, optional): A short description for the warning. Defaults to ''.
            timestamp (datetime, optional): date and time what ocurred. Defaults to datetime.now().
            ex (Exception, optional): Exception for more details. Defaults to None.
            priority (Priority, optional): When we have more than one error, we need to classify that. Defaults to False.
        """
        self.priority = priority
        super(Error, self).__init__(
            r_type=RType.ERR,
            description=description,
            timestamp=timestamp,
            ex=ex
        )
    
    def get_json(self) -> dict:
        information = super(Error, self).get_json()
        information['priority'] = self.priority.value
        return information
    
    def __repr__(self) -> str:
        return f"""Error(
                        description={self.description},
                        timestamp={self.timestamp},
                        ex={self.ex},
                        priority={self.priority}
                    )
                    """

class Warning(Registry):
    follow_me:bool

    def __init__(
            self,
            description:str='',
            timestamp:datetime=datetime.now(),
            ex:Exception=None,
            follow_me:bool=False
            ) -> None:
        """
        For actions that would cause problems, but work

        Args:
            description (str, optional): A short description for the warning. Defaults to ''.
            timestamp (datetime, optional): date and time what ocurred. Defaults to datetime.now().
            ex (Exception, optional): Exception for more details. Defaults to None.
            follow_me (bool, optional): If this warning needs to followed. Defaults to False.
        """
        self.follow_me = follow_me
        super(Warning, self).__init__(
            r_type=RType.WARN,
            description=description,
            timestamp=timestamp,
            ex=ex
        )
    
    def get_json(self) -> dict:
        information = super(Warning, self).get_json()
        information['follow_me'] = self.follow_me
        return information
    
    def __repr__(self) -> str:
        return f"""Warning(
                        description={self.description},
                        timestamp={self.timestamp},
                        ex={self.ex},
                        follow_me={self.follow_me}
                    )
                    """

#TODO Add an Info Class to the logger

def create_logfile() -> None:
    try:
        path = Path(LOG_PATH)
        path.parent.mkdir(parents=True)
        path.write_text('[]')
    except FileExistsError as ex:
        if not path.exists():
            with open(LOG_PATH, 'w') as new_file:
                return new_file.write('[]')

def get_previous_logs() -> list:
    with open(f'{LOG_PATH}', 'r') as file:
        return json.load(file)

def save_log_to_file(obj:dict) -> bool:
    lista = get_previous_logs()
    lista.append(obj)

    with open('logs/log.ev', 'w') as file:
        return bool(file.write(json.dumps(lista)))
    
#TODO Make a file length detector to backup the file and initialize a new one
def add_log(obj:dict) -> bool:
    create_logfile()
    return save_log_to_file(obj)

def log(obj:Error | Warning, printable:bool=False) -> bool:
    status = add_log(obj.get_json())
    if printable:
        print(f'Saved log status: {"Correcto" if status else "Fallido"}', file=sys.stderr)
    return status