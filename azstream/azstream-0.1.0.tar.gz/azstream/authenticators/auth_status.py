from dataclasses import dataclass
from datetime import timedelta
from typing import Union
from enum import Enum
from ..utils.formatting import timedelta_to_hh_mm


class SessionStatus(Enum):
    HEALTY = 1
    EXPIRING = 2
    EXPIRED = 3
    ERROR = 4


@dataclass
class AuthStatus():
    session_status: SessionStatus
    expires_in: Union[timedelta, None]
    can_refresh: bool
    failed_refreshes: int
    failed_authentications: int

    def __str__(self):
        status = ''
        expires_in = ''
        if self.session_status == SessionStatus.ERROR:
            status = 'Error'
            expires_in = 'N/A'
        elif self.session_status == SessionStatus.EXPIRED:
            status = 'Expired'
            expires_in = 'N/A'
        elif self.session_status == SessionStatus.EXPIRING:
            status = 'Expiring'
            expires_in = timedelta_to_hh_mm(self.expires_in)
        elif self.session_status == SessionStatus.HEALTY:
            status = 'Healty'
            expires_in = timedelta_to_hh_mm(self.expires_in)
        return f'Session status: {status}. Expires in: {expires_in}.'