from abc import abstractmethod
from datetime import datetime
from typing import Optional


class Equipment:
    """"encapsulates equipment for routes (bus,tramway or trolleybus)"""

    def __init__(self, type_equipment: int):
        self.to_number = lambda: type_equipment

    @staticmethod
    def bus():
        return Equipment(0)

    @staticmethod
    def tramway():
        return Equipment(1)

    @staticmethod
    def trolleybus():
        return Equipment(2)

    def to_str(self):
        if self.to_number() == 0:
            return "bus"
        if self.to_number() == 1:
            return "tramway"
        if self.to_number() == 2:
            return "trolleybus"

    @classmethod
    def by_number(cls, num: int):
        if num == 0:
            return cls.bus()
        if num == 1:
            return cls.tramway()
        if num == 2:
            return cls.trolleybus()

    def __eq__(self, other):
        return self.to_number() == (other.to_number())

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        return hash(self.to_number())


class Route:
    """"encapsulates routes"""

    def __init__(self, id_mgt: str, equipment: Equipment, name: str):
        self.get_id_mgt = lambda: id_mgt
        self.get_equipment = lambda: equipment
        self.get_name = lambda: name

    def __eq__(self, other):
        return str(self.get_id_mgt()) == str(other.get_id_mgt()) and \
               self.get_equipment() == other.get_equipment() and \
               self.get_name() == other.get_name()
        # str() for old int type of field and changing format on t.mos.ru

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        return hash((self.get_id_mgt(), self.get_equipment(), self.get_name()))

    def __str__(self):
        return "{} ({}, id={})".format(self.get_name(), self.get_equipment().to_str(), self.get_id_mgt())

    def __repr__(self):
        return str(self)


class Stop:
    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get_coords(self) -> list[float]:
        pass

    @abstractmethod
    def get_id(self) -> int:
        pass


class Stop_builder:
    @abstractmethod
    def set_name(self, name: str) -> 'Stop_builder':
        pass

    @abstractmethod
    def set_id(self, id_stop: int) -> 'Stop_builder':
        pass

    @abstractmethod
    def set_coords(self, coords: list[float]) -> 'Stop_builder':
        pass

    @abstractmethod
    def build(self) -> Stop:
        pass


class Timetable_stop:
    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get_coords(self) -> list[float]:
        pass

    @abstractmethod
    def get_times(self) -> iter:
        pass


class Timetable:

    @abstractmethod
    def __iter__(self):
        """Iterator for stops"""
        pass

    @abstractmethod
    def get_direction(self) -> int:
        pass

    @abstractmethod
    def get_id_route_t_mos_ru(self) -> str:
        pass

    @abstractmethod
    def get_date(self) -> datetime.date:
        pass

    @abstractmethod
    def get_stops(self) -> list[Timetable_stop]:
        pass


class Timetable_stop_time:
    @abstractmethod
    def get_time(self) -> datetime.time:
        pass

    @abstractmethod
    def get_color_special_flight(self) -> Optional[str]:
        pass


class Timetable_stop_builder:
    @abstractmethod
    def add_item_timetable(self, time_flight: datetime.time,
                           special_flight: Optional[str] = None) -> 'Timetable_stop_builder':
        pass

    @abstractmethod
    def build(self) -> Timetable_stop:
        pass

    @abstractmethod
    def set_name(self, name: str) -> 'Timetable_stop_builder':
        pass

    @abstractmethod
    def set_coords(self, coords: list[float]) -> 'Timetable_stop_builder':
        pass


class Timetable_builder:
    @abstractmethod
    def add_stop(self) -> Timetable_stop_builder:
        pass

    @abstractmethod
    def build(self) -> Timetable:
        pass

    @abstractmethod
    def set_id_route_t_mos_ru(self, id_route_t_mos_ru: str) -> 'Timetable_builder':
        pass

    @abstractmethod
    def set_direction(self, direction: int) -> 'Timetable_builder':
        pass

    @abstractmethod
    def set_date(self, date: datetime.date) -> 'Timetable_builder':
        pass
