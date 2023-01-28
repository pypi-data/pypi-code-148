from ..base import BaseCategory
from typing import TYPE_CHECKING, Any

from dataclasses import dataclass, field
from datetime import datetime, time

if TYPE_CHECKING:
    from ..api import AbstractAPI


@dataclass
class EdUnit:
    Id: int | None = None
    Type: str | None = None
    Name: str | None = None
    Corporative: bool = False
    OfficeOrCompanyId: int | None = None
    OfficeOrCompanyName: str | None = None
    OfficeOrCompanyAddress: str | None = None
    OfficeTimeZone: time | None = None
    Discipline: str | None = None
    Level: str | None = None
    Maturity: str | None = None
    LearningType: str | None = None
    ExtraFields: list | None = None
    StudentsCount: int | None = None
    Vacancies: int | None = None
    StudyUnitsInRange: str | None = None
    Description: str | None = None
    CompanyContractNumber: str | None = None
    CompanyContractDate: datetime | None = None
    ScheduleItems: list | None = None
    Days: list | None = None
    FiscalInfo: None | list = None
    TeacherPrices: None |list = None
    PriceValues: None | list = None
    Assignee: None | dict = None


@dataclass(frozen=True)
class Statuses:
    Reserve = 'Reserve'
    Forming = 'Forming'
    Working = 'Working'
    Stopped = 'Stopped'
    Finished = 'Finished' 


@dataclass 
class EdUnits:
    EdUnits: list[EdUnit] = field(default_factory=list)


class EdUnitsCategory(BaseCategory):

    def __init__(self, api: 'AbstractAPI'):
        self.api = api

    def get_ed_units(
            self,
            id: None | int = None,
            types: None | str = None,
            dateFrom: None | datetime = None,
            dateTo: None | datetime = None,
            statuses: None | str = None,
            officeOrCompanyId: None | int = None,
            locationId: None | int = None,
            disciplines: None | str = None,
            levels: None | str = None,
            maturities: None | str = None,
            corporative: None | bool = None,
            learningTypes: None | str = None
            ) -> list[EdUnit]:
        data = self.handle_parameters(locals())

        response = self.api.request(
                method='GetEdUnits',
                http_method='GET',
                data=data
                )

        return [EdUnit(**_) for _ in EdUnits(**response).EdUnits]
    
    def get_all_ed_units_name(self, **kwargs) -> list[str]:
        ed_units = self.get_ed_units(**kwargs)
        return [ed_unit.Name for ed_unit in ed_units]

    def get_all_ed_units_id(self, **kwargs) -> list[int]:
        ed_units = self.get_ed_units(**kwargs)
        return [ed_unit.Id for ed_unit in ed_units]


__all__ = ['EdUnitsCategory']
        
