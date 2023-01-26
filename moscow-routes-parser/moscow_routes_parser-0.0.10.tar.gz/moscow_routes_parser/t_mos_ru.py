import html
import json
import logging
import re
from abc import abstractmethod
from datetime import datetime, time
from typing import Optional

import requests

from moscow_routes_parser.model import Route, Timetable, Equipment, Timetable_builder
from moscow_routes_parser.model_impl import Timetable_builder_t_mos_ru


class parser_timetable:
    """"Interface for parser"""

    @abstractmethod
    def parse(self, text: str) -> Timetable_builder:
        pass


class parser_timetable_t_mos_ru(parser_timetable):
    """"Parser for timetable from t.mos.ru implementation"""

    def __init__(self, builder: Timetable_builder):
        """"Initialize parser
        :param builder: Builder for Timetable for route
        """
        self.builder = lambda: builder

    def parse(self, text: str) -> Timetable_builder:
        """Parse text from https://transport.mos.ru/ru/ajax/App/ScheduleController/getRoute (for format using
        2022-Jan-11)

        Since 12.01.2022 t.mos.ru drop data-services from results

        @param text: text for parse
        @return Timetable for route
        """
        result_stops = type(self.builder())()
        # stops = re.finditer(r'data-stop="([^"]*?)".*?data-services="([^"]*?)".*?d-inline.*?>(.*?)<(.*?)</li>', text,
        #                     re.M + re.S
        #                     )
        stops = re.finditer(r'data-stop="(.*?)".*?d-inline.*?>(.*?)<(.*?)</li>', text,
                            re.M + re.S
                            )
        data_coords_iter = re.finditer(r'data-coords="(.*?)"', text,
                                       re.M + re.S
                                       )
        data_coords_list = list(data_coords_iter)
        # если есть расписание
        if len(data_coords_list) > 0:
            data_coords = data_coords_list[0].group(1)
            data_coords = html.unescape(data_coords)
            data_coords = json.loads(data_coords)['features']
            data_coords = iter(map(lambda feature: feature['geometry']['coordinates'], data_coords))
        else:
            data_coords = []

        for stop in stops:
            name_stop = stop.group(2)
            coords_stop = next(data_coords)
            description = stop.group(3)
            logger = logging.getLogger(__name__)
            logger.info(name_stop)
            hours = re.finditer(r'dt1.*?(\d\d):(.*?)</div>\s*</div>\s*</div>', description, re.M + re.S)
            timetable_stop = result_stops.add_stop()
            timetable_stop.set_name(name_stop)
            timetable_stop.set_coords(coords_stop)
            log_timetable = ""
            for hour in hours:
                num_hour = int(hour.group(1))
                minutes_text = hour.group(2)
                log_timetable += str(num_hour) + ": "
                minutes = re.finditer(r'div10([^>]*)>\s*(\d\d)', minutes_text, re.M + re.S)
                for minute in minutes:
                    num_minute = int(minute.group(2))
                    color_start = minute.group(1).find('color: ')
                    if color_start >= 0:
                        quote = minute.group(1).find('"', color_start)
                        min_color = minute.group(1)[color_start + 7:quote]
                    else:
                        min_color = None
                    if not (min_color is None):
                        log_timetable += "{}{}".format(num_minute, min_color) + " "
                        pass
                    else:
                        log_timetable += str(num_minute) + " "
                        pass
                    time_flight = time(num_hour, num_minute)
                    timetable_stop.add_item_timetable(time_flight, min_color)
                logger.info(log_timetable)
        return result_stops


class Parser_routes:

    @abstractmethod
    def parse(self, text: str) -> [Route]:
        pass


class Parser_routes_t_mos_ru(Parser_routes):

    def __init__(self):
        self.count = None

    def parse(self, text: str) -> [Route]:
        """"Parses route info from transport.mos.ru (name, id, type)
        :param text: text for parsing from t.mos.ru
        :return list of Route
        """
        count_result = re.finditer(r'data-count-pages="(\d+)"', text, re.M + re.S)
        self.count = int(list(count_result)[0].group(1))

        result = re.finditer(r'<a.*?href=.*?route/(.+?)".*?<div.*?ic[ ]([a-z-]+).*?</i>\s*(\S+?)\s*</div>', text,
                             re.M + re.S)
        list_routes = []

        for route in result:
            num = route.group(1)
            type_route = route.group(2)
            if type_route.find('-bus') >= 0:
                type_route = Equipment.bus()
            elif type_route.find('tramway') >= 0:
                type_route = Equipment.tramway()
            elif type_route.find('trolleybus') >= 0:
                type_route = Equipment.trolleybus()
            else:
                logging.getLogger(__name__).error("Unknown type route: {}".format(type_route))
                type_route = None
            name = route.group(3)
            list_routes.append(Route(num, type_route, name))
        return list_routes


def get_route(date: datetime.date, id_route_t_mos_ru: str, direction: int,
              get_route_url: str = 'https://transport.mos.ru/ru/ajax/App/ScheduleController/getRoute',
              parser: parser_timetable = parser_timetable_t_mos_ru(builder=Timetable_builder_t_mos_ru())
              ) -> Timetable:
    """Get timetable for route by date and direction
        :param date: date of timetable for route
        :param id_route_t_mos_ru: id of route from t.mos.ru
        :param direction: direction for route (0 or 1)
        :param get_route_url URL for requesting timetable
        :param parser for timetable
        :return timetable for route by date and direction
    """
    logger = logging.getLogger(__name__)
    try:
        # strange problem with SSL Cert in package
        response = requests.get(get_route_url,
                                params={
                                    'mgt_schedule[isNight]': '',
                                    'mgt_schedule[date]': date.strftime("%d.%m.%Y"),
                                    'mgt_schedule[route]': id_route_t_mos_ru,
                                    'mgt_schedule[direction]': direction,
                                }
                                )
        if response.status_code == 200:
            logger.info("Get route #{}".format(id_route_t_mos_ru))
            route_info = parser.parse(response.text)
        else:
            logger.error("Error status: {}".format(response.status_code))
            route_info = None
    except requests.exceptions.RequestException as e:
        logger.error("Error " + str(e))
        route_info = None

    if not (route_info is None):
        result = route_info.set_id_route_t_mos_ru(id_route_t_mos_ru).set_direction(direction).set_date(date).build()
        if len(result.get_stops()) == 0:  # Error of loading timetable without exceptions
            result = None
    else:
        result = None
    return result


def get_list_routes(work_time: int, direction: int,
                    parser: Parser_routes = None,
                    get_routes_url: str = 'https://transport.mos.ru/ru/ajax/App/ScheduleController/getRoutesList'
                    ) -> Optional[list[Route]]:
    """get list routes by work_time and direction from transport.mos.ru
        :param parser: function to parse got string
        :param get_routes_url: url for requesting routes
        :param work_time: work day or not (1 or 0)
        :param direction: 0
        :return list of Route
    """
    if parser is None:
        parser = Parser_routes_t_mos_ru()
    page = 1
    result_routes = []
    finish = False
    count = None
    logger = logging.getLogger(__name__)
    while not finish:
        finish = False
        repeat = True
        while repeat:
            repeat = False
            try:
                # strange problem with SSL Cert in package
                response = requests.get(get_routes_url,
                                        params={
                                            'mgt_schedule[search]': '',
                                            'mgt_schedule[isNight]': '',
                                            'mgt_schedule[filters]': '',
                                            'mgt_schedule[work_time]': work_time,
                                            'page': page,
                                            'mgt_schedule[direction]': direction,
                                        }
                                        # , headers={'Cookie': "_ym_d=1637468102; _ym_uid=1637468102592825648; mos_id=rBEAAmGaFNawBwAOHRgWAgA=; _ga=GA1.2.1733238845.1637487830; uxs_uid=147e2110-500d-11ec-a7cb-8bb8b12c3186; KFP_DID=ee285837-cd1f-0a9b-c8a2-9cef6a4ee333; _ym_isad=2; _ym_visorc=w"}
                                        )
                if response.status_code == 200:
                    logger.info("Get page #{}".format(page))
                    routes = parser.parse(response.text)
                    result_routes += routes
                    if count is None:
                        count = parser.count
                    if not routes:
                        finish = True
                else:
                    logger.error("Error status: {}".format(response.status_code))
                    finish = True
                page = page + 1
                if page > count:
                    finish = True
            except requests.exceptions.RequestException as e:
                logger.error("Error " + str(e))
                repeat = True

    return result_routes
