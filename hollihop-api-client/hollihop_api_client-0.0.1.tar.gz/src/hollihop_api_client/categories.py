from .methods import (
        locations,
        offices,
        ed_units,
        ed_unit_students,
        leads,
        )
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .api import AbstractAPI


class APICategories:
    def __init__(self, api: 'AbstractAPI'):
        self.api = api

    @property
    def locations(self) -> locations.LocationsCategory:
        return locations.LocationsCategory(self.api)

    @property
    def offices(self) -> offices.OfficesCategory:
        return offices.OfficesCategory(self.api)

    @property
    def ed_units(self) -> ed_units.EdUnitsCategory:
        return ed_units.EdUnitsCategory(self.api)

    @property
    def ed_unit_students(self) -> ed_unit_students.StudentsCategory:
        return ed_unit_students.StudentsCategory(self.api)

    @property
    def leads(self) -> leads.LeadsCategory:
        return leads.LeadsCategory(self.api)


__all__ = ['APICategories']
