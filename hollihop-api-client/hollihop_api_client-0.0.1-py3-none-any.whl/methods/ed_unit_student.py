from ..base import BaseCategory
from typing import TYPE_CHECKING, Any
import phonenumbers

from dataclasses import dataclass, field
from datetime import datetime, time, date, timedelta

if TYPE_CHECKING:
    from ..api import AbstractAPI

@dataclass
class StudentAgent:
    FirstName: None | str = None
    LastName: None | str = None
    MiddleName: None | str = None
    WhoIs: None | str = None
    Mobile: None | str = None
    UseMobileBySystem: None | str = None
    Phone: None | str = None
    EMail: None | str = None
    UseEMailBySystem: None | bool = None
    Skype: None | str = None
    JobOrStudyPlace: None | str = None
    Position: None | str = None
    IsCustomer: None | bool = None
    Birthday: None | datetime = None




@dataclass
class Payer:
    ClientId: int | None = None
    IsCompany: bool | None = None
    Name: str | None = None
    Actual: bool | None = None
    TerminatedContracts: list = None
    PriceId: int | None = None
    PriceName: str | None = None
    Discounts: list | None = None
    Surcharges: list | None = None
    PayableMinutes: int | None = None
    PayableUnits: str | None = None
    PayableMinutesRanged: int | None = None
    PayableUnitsRanged: str | None = None
    Value: str | None = None
    ValueRanged: str | None = None
    ValuePaidRanged: str | None = None
    ContractValue: str | None = None
    ContractValueRestored: str | None = None
    ContractValueRanged: str | None = None
    ContractValueRangedRestored: str | None = None
    DebtDate: datetime | None = None
    EdUnitPayments: list | None = None


@dataclass 
class Student:
    EdUnitId: int | None = None
    EdUnitType: str | None = None
    EdUnitName: str | None = None
    EdUnitCorporative: bool | None = None
    EdUnitOfficeOrCompanyId: int | None = None
    EdUnitOfficeOrCompanyName: str | None = None
    EdUnitDiscipline: str | None = None
    EdUnitLevel: str | None = None
    EdUnitMaturity: str | None = None
    EdUnitLearningType: str | None = None
    StudentClientId: int | None = None
    StudentName: str | None = None
    StudentMobile: str | None = None
    StudentPhone: str | None = None
    StudentEMail: str | None = None
    StudentAgents: list[StudentAgent] | None = None
    StudentExtraFields: list | None = None
    BeginDate: datetime | None = None
    EndDate: datetime | None = None
    BeginTime: time | None = None
    EndTime: time | None = None
    Weekdays: int | None = None
    Status: str | None = None
    StudyMinutes: int | None = None
    StudyUnits: str | None = None
    Days: list | None = None
    Payers: list[Payer] | None = None
    Phones: list[str] = field(init=False) 

    def __post_init__(self):
        self.Phones = []
        if not self.Payers is None:
            self.Payers = [Payer(**_) for _ in self.Payers]
        if not self.StudentAgents is None:
            self.StudentAgents = [StudentAgent(**_) for _ in self.StudentAgents]
            for agent in self.StudentAgents:
                if not agent.Mobile is None:
                    self.Phones.append(self.format_phone(agent.Mobile).replace('+', ''))
        if not self.StudentMobile is None:
            self.Phones.append(self.format_phone(self.StudentMobile).replace('+', ''))
        if not self.StudentPhone is None:
            self.Phones.append(self.format_phone(self.StudentPhone).replace('+', ''))

    def format_phone(self, number) -> str:
        return phonenumbers.format_number(
                phonenumbers.parse(number, 'RU'),
                phonenumbers.PhoneNumberFormat.E164
                )

    def __repr__(self) -> str:
        return self.StudentName



@dataclass 
class Students:
    EdUnitStudents: list[Student] = field(default_factory=list)


class StudentsCategory(BaseCategory):

    def __init__(self, api: 'AbstractAPI'):
        self.api = api

    def get_students(
            self,
            edUnitId: None | int = None,
            edUnitTypes: None | str = None,
            edUnitOfficeOrCompanyId: None | int = None,
            edUnitOfficeOrCompany: None | str = None,
            studentClientId: None | int = None,
            dateFrom: None | datetime = None,
            dateTo: None | datetime = None,
            statuses: None | str = None,
            queryPayers: None | bool = None
            ) -> list[Student]:
        data = self.handle_parameters(locals())

        response = self.api.request(
                method='GetEdUnitStudents',
                http_method='GET',
                data=data
                )

        return [Student(**_) for _ in Students(**response).EdUnitStudents]
    
    def get_all_students_name(self, **kwargs) -> list[str]:
        students = self.get_students(**kwargs)
        return [student.StudentName for student in students]

    def get_all_students_id(self, **kwargs) -> list[int]:
        students = self.get_students(**kwargs)
        return [student.StudentClientId for student in students]

    def get_students_with_debt(
            self,
            in_a_week: bool = False,
            not_newbies: bool = True,
            **kwargs):
        students = self.get_students(**kwargs)
        if not_newbies:
            students = [student 
                    for student in students
                    if not student.Payers[0].EdUnitPayments is None
                    and
                    len(student.Payers[0].EdUnitPayments) > 1
                    ]
        students = [student 
                for student in students
                if not student.Payers[0].DebtDate is None 
                and 
                datetime.strptime(
                    student.Payers[0].DebtDate, 
                    '%Y-%m-%d'
                    ) <= datetime.now()
                ]
        if in_a_week:
            today_debtors_ids = [
                    student.StudentClientId for student in students
                    ] 
            students = [student
                    for student in students 
                    if not student.Payers[0].DebtDate is None 
                    and
                    datetime.strptime(
                        student.Payers[0].DebtDate,
                        '%Y-%m-%d'
                        ) <= datetime.now() + timedelta(days=7) and 
                    student.StudentClientId not in today_debtors_ids
                    ]

        return students



__all__ = ['StudentsCategory']
        
