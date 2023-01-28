from ..base import BaseCategory
from typing import TYPE_CHECKING, Any

from dataclasses import dataclass, field
from datetime import datetime, time, date, timedelta

if TYPE_CHECKING:
    from ..api import AbstractAPI

    
@dataclass
class Lead:
    Id: int | None
    Created: datetime | None = None
    Updated: datetime | None = None
    FirstName: str | None = None
    LastName: str | None = None
    MiddleName: str | None = None
    AddressDate: datetime | None = None
    AdSource: str | None = None
    StatusId: str | None = None
    Status: str | None = None
    Birthday: datetime | None = None
    Phone: str | None = None
    Mobile: str | None = None
    UseMobileBySystem: bool | None = None
    EMail: str | None = None
    UseEMailBySystem: bool | None = None
    Maturity: str | None = None
    LearningType: str | None = None
    Discipline: str | None = None
    Level: str | None = None
    Agents: list | None = None
    OfficesAndCompanies: list | None = None
    Assignees: list | None = None
    ExtraFields: list | None = None
    StudentClientId: int | None = None
    Name: str = field(init=False)
    
    def __post_init__(self):
        self.Name = self.LastName + ' ' + self.FirstName + ' ' + self.MiddleName 


@dataclass 
class Leads:
    Leads: None | list[Lead] = field(default_factory=list)
    Now: None | datetime = None


class LeadsCategory(BaseCategory):

    def __init__(self, api: 'AbstractAPI'):
        self.api = api

    def get_leads(
            self,
            id: None | int = None,
            attached: None | bool = None,
            studentClientId: None | int = None
            ) -> list[Lead]:
        data = self.handle_parameters(locals())

        response = self.api.request(
                method='GetLeads',
                http_method='GET',
                data=data
                )

        raw_leads = [Lead(**_) for _ in Leads(**response).Leads]
        
        return raw_leads
    
    def get_all_leads_id(self, **kwargs) -> list[int]:
        leads = self.get_leads(**kwargs)
        return [lead.StudentClientId for lead in leads]


__all__ = ['LeadsCategory']
        
