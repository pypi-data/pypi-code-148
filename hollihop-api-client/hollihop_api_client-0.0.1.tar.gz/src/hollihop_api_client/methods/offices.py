from ..base import BaseCategory
from typing import TYPE_CHECKING, Any

from dataclasses import dataclass, field
from datetime import timezone

if TYPE_CHECKING:
    from ..api import AbstractAPI


@dataclass
class Office:
    Id: None | int = None
    Name: None | str = None
    Location: None | str = None
    Address: None | str = None
    EMail: None | str = None
    Phone: None | str = None
    NoClassrooms: None | bool = None
    TimeZone: None | timezone = None
    License: None | str = None


@dataclass 
class Offices:
    Offices: list[Office] = field(default_factory=list)


class OfficesCategory(BaseCategory):

    def __init__(self, api: 'AbstractAPI'):
        self.api = api

    def get_offices(
            self,
            id: None | int = None,
            location_id: None | int = None,
            name: None | str = None,
            license: None | str = None
            ) -> list[Office]:
        data = self.handle_parameters(locals())

        response = self.api.request(
                method='GetOffices',
                http_method='GET',
                data=data
                )

        return [Office(**_) for _ in Offices(**response).Offices]
    
    def get_all_offices_name(self) -> list[str]:
        offices = self.get_offices()
        return [office.Name for office in offices]

    def get_all_offices_id(self) -> list[int]:
        offices = self.get_offices()
        return [office.Id for office in offices]


__all__ = ['OfficesCategory']
        
