from ..base import BaseCategory
from typing import TYPE_CHECKING, Any

from dataclasses import dataclass, field
from functools import lru_cache

if TYPE_CHECKING:
    from ..api import AbstractAPI


@dataclass
class Location:
    Id: None | int
    Name: None | str


@dataclass 
class Locations:
    Locations: list[Location] = field(default_factory=list)


class LocationsCategory(BaseCategory):

    def __init__(self, api: 'AbstractAPI'):
        self.api = api

    def get_locations(
            self,
            id: None | int = None,
            name: None | str = None
            ) -> list[Location]:
        data = self.handle_parameters(locals())

        response = self.api.request(
                method='GetLocations',
                http_method='GET',
                data=data
                )

        return [Location(**_) for _ in Locations(**response).Locations]
    
    def get_all_locations_name(self) -> list[str]:
        locations = self.get_locations()
        return [location.Name for location in locations]

    def get_all_locations_id(self) -> list[int]:
        locations = self.get_locations()
        return [location.Id for location in locations]


__all__ = ['LocationsCategory']
        
