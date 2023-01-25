from enum import Enum
from dataclasses import dataclass

class TitleType(Enum):
    MOVIE  = 1
    SERIES = 2
    UNKNOWN = 9


@dataclass
class SearchResult():

    # Title infos
    id: str
    title: str

    # Platform infos
    platform_tag: str   # i.e. 'toutv'
    platform_id: str    # i.e. 'toutv-0'

    # Title infos
    title_type: TitleType = TitleType.UNKNOWN

    # Accessibility infos
    has_access: bool = True

    # Images
    poster_url: str = None
    backdrop_url: str = None
