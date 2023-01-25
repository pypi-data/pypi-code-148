from enum import Enum
from typing import List
from .search_result import TitleType
from dataclasses import dataclass, field


@dataclass
class Title():

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

    # People
    actors: List[str] = field(default_factory=list) 
    directors: List[str] = field(default_factory=list) 
    authors: List[str] = field(default_factory=list) 
    producers: List[str] = field(default_factory=list) 

    # Other metadata
    genres: List[str] = field(default_factory=list) 
    synopsis: str = None
