from datetime import datetime
from itertools import groupby
from typing import Optional, Tuple

from moscow_routes_parser.model import Stop, Stop_builder, Timetable_stop_time, Timetable_stop, Timetable, \
    Timetable_stop_builder, Timetable_builder


class Stop_impl(Stop):

    def get_coords(self) -> Tuple[float, float]:
        return self.coords

    def get_name(self) -> str:
        return self.name

    def __str__(self):
        return self.get_name()

    def __repr__(self):
        return self.get_name()

    def __hash__(self):
        return hash((self.get_coords(),self.name))

    def __init__(self, name: str, coords: Tuple[float, float]):
        self.coords = coords
        self.name = name

    def __eq__(self, other):
        return not (self.get_coords()[0] is None) and \
               not (self.get_coords()[1] is None) and \
               not (other.get_coords()[0] is None) and \
               not (other.get_coords()[1] is None) and            \
               self.get_name() == other.get_name() and \
               abs(self.get_coords()[0] - other.get_coords()[0]) <= 0.0000005 and \
               abs(self.get_coords()[1] - other.get_coords()[1]) <= 0.0000005

    def __ne__(self, other):
        return not (self == other)


class Stop_builder_impl(Stop_builder):

    def set_coords(self, coords: (float, float)) -> Stop_builder:
        self.coords = coords
        return self

    def __init__(self):
        self.coords = None
        self.name = None

    def set_name(self, name: str) -> Stop_builder:
        self.name = name
        return self

    def build(self) -> Stop:
        return Stop_impl(self.name, self.coords)


class Timetable_stop_time_t_mos_ru(Timetable_stop_time):

    def __init__(self, time_flight: datetime.time, color_special_flight: Optional[str]):
        self.time_flight = time_flight
        self.color_special_flight = color_special_flight

    def get_time(self) -> datetime.time:
        return self.time_flight

    def get_color_special_flight(self) -> Optional[str]:
        return self.color_special_flight

    def __eq__(self, other):
        return self.get_time() == other.get_time() and \
               self.get_color_special_flight() == other.get_color_special_flight()

    def __ne__(self, other):
        return not (self == other)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        str_time = self.get_time().strftime("%H:%M")
        color = self.get_color_special_flight()
        if not (color is None):
            str_time += " ({})".format(color)
        return str_time


class Timetable_stop_t_mos_ru(Timetable_stop):

    def __init__(self, stop: Stop, times: list[Timetable_stop_time_t_mos_ru]):
        self.stop = stop
        self.times = times

    def get_times(self) -> iter:
        return iter(self.times)

    def get_stop(self) -> Stop:
        return self.stop

    def __eq__(self, other):
        return self.get_stop() == other.get_stop() and \
               list(sorted(self.get_times(), key=lambda x: x.get_time())) == list(
            sorted(other.get_times(), key=lambda x: x.get_time()))

    def __ne__(self, other):
        return not (self == other)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        result = "{} ({},{}):\n".format(self.get_name(), self.get_coords()[0], self.get_coords()[1])
        time_by_hours = groupby(sorted(self.get_times(), key=lambda t: t.get_time()), key=lambda t: t.get_time().hour)
        for h in time_by_hours:
            result += str(h[0]) + ': ' + \
                      ' '.join(map(lambda t: str(t.get_time().minute) + ("" if t.get_color_special_flight() is None
                                                                         else " ({})".format(
                          t.get_color_special_flight())), h[1])) + "\n"
        return result


class Timetable_t_mos_ru(Timetable):

    def has_another_direction(self):
        return self.flag_has_another_direction

    def get_stops(self) -> list[Timetable_stop]:
        return self.stops

    def __init__(self, id_route_t_mos_ru: str, direction: int, date: datetime.date,
                 stops: list[Timetable_stop],flag_has_another_direction=False):
        self.flag_has_another_direction = flag_has_another_direction
        self.id_route_t_mos_ru = id_route_t_mos_ru
        self.direction = direction
        self.stops = stops
        self.date = date

    def get_direction(self) -> int:
        return self.direction

    def get_id_route_t_mos_ru(self) -> str:
        return self.id_route_t_mos_ru

    def get_date(self) -> datetime.date:
        return self.date

    def __iter__(self):
        return iter(self.get_stops())

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        result = "Route with id={}, direction = {}, date={}: ".format(self.get_id_route_t_mos_ru(),
                                                                      self.get_direction(), self.get_date()) + "\n"
        result += ''.join(str(self.get_stops()))
        return result


class Timetable_stop_builder_t_mos_ru(Timetable_stop_builder):

    def add_item_timetable(self, time_flight: datetime.time,
                           special_flight: Optional[str] = None) -> Timetable_stop_builder:
        self.time_flights.append(Timetable_stop_time_t_mos_ru(time_flight, special_flight))
        return self

    def set_name(self, name: str) -> Timetable_stop_builder:
        self.name = name
        return self

    def set_coords(self, coords: (float, float)) -> Timetable_stop_builder:
        self.coords = coords
        return self

    def __init__(self):
        self.coords = None
        self.name = None
        self.time_flights = []

    def build(self) -> Timetable_stop:
        stop = Stop_impl(self.name, self.coords)
        return Timetable_stop_t_mos_ru(stop, self.time_flights)


class Timetable_builder_t_mos_ru(Timetable_builder):

    def __init__(self):
        #Default True for backward compatilibity
        self.flag_has_another_direction = True
        self.date = None
        self.direction = None
        self.id_route_t_mos_ru = None
        self.stops = []

    def set_date(self, date: datetime.date) -> Timetable_builder:
        self.date = date
        return self

    def add_stop(self) -> Timetable_stop_builder:
        stop_builder = Timetable_stop_builder_t_mos_ru()
        self.stops.append(stop_builder)
        return stop_builder

    def build(self) -> Timetable:
        return Timetable_t_mos_ru(
            self.id_route_t_mos_ru,
            self.direction,
            self.date,
            list(map(lambda stop_builder: stop_builder.build(),
                     self.stops)),
            self.flag_has_another_direction
        )

    def set_id_route_t_mos_ru(self, id_route_t_mos_ru: str) -> Timetable_builder:
        self.id_route_t_mos_ru = id_route_t_mos_ru
        return self

    def set_direction(self, direction: int) -> Timetable_builder:
        self.direction = direction
        return self

    def set_has_another_direction(self,flag_has_another_direction=True):
        self.flag_has_another_direction=flag_has_another_direction


