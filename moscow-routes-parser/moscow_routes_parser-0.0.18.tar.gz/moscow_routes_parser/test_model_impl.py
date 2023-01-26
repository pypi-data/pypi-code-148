from datetime import time, date
from unittest import TestCase

from moscow_routes_parser.model_impl import Stop_impl, Stop_builder_impl, Timetable_stop_time_t_mos_ru, \
    Timetable_t_mos_ru, Timetable_stop_builder_t_mos_ru, Timetable_builder_t_mos_ru


class TestStop_impl(TestCase):
    def test_stop(self):
        name = "Stop"
        coords = (10.2, 13.3)
        stop = Stop_impl(name, coords)

        self.assertEqual(stop.get_name(), name)
        self.assertEqual(stop.get_coords(), coords)

    def test_eq(self):
        name = "Stop"
        coords = (37.574604,55.499970)
        name2 = "Stop"
        coords2 = (37.5746041,55.4999701)
        name3 = "Stop"
        coords3 = (37.574605,55.499971)
        stop = Stop_impl(name,coords)
        stop2 = Stop_impl(name2,coords2)
        stop3 = Stop_impl(name3,coords3)
        self.assertTrue(stop==stop2)
        self.assertFalse(stop==stop3)

class TestStop_builder_impl(TestCase):
    def test_builder(self):
        name = "Stop"
        stop = Stop_builder_impl().set_name(name).set_coords((10, 20)).build()

        self.assertEqual(stop.get_name(), name)
        self.assertEqual(stop.get_coords(), (10, 20))

    def test_builder_reverse(self):
        name = "StopStop"
        stop = Stop_builder_impl().set_coords((10, 20)).set_name(name).build()

        self.assertEqual(stop.get_name(), name)
        self.assertEqual(stop.get_coords(), (10, 20))


class TestTimetable_stop_time_t_mos_ru(TestCase):
    def test_timetable_stop_time(self):
        t = time(10, 15)
        color = "Red"
        timetable_stop_time = Timetable_stop_time_t_mos_ru(t, color)

        self.assertEqual(timetable_stop_time.get_time(), t)
        self.assertEqual(timetable_stop_time.get_color_special_flight(), color)

    def test_timetable_stop_time_none_color(self):
        t = time(10, 15)
        color = None
        timetable_stop_time = Timetable_stop_time_t_mos_ru(t, color)

        self.assertEqual(timetable_stop_time.get_time(), t)
        self.assertEqual(timetable_stop_time.get_color_special_flight(), color)

    def test_timetable_stop_time_equal_true(self):
        t = time(10, 15)
        color = "Red"
        timetable_stop_time = Timetable_stop_time_t_mos_ru(t, color)
        t2 = time(10, 15)
        color2 = "Red"
        timetable_stop_time2 = Timetable_stop_time_t_mos_ru(t2, color2)
        self.assertTrue(timetable_stop_time == timetable_stop_time2)
        self.assertFalse(timetable_stop_time != timetable_stop_time2)

    def test_timetable_stop_time_equal_false_color(self):
        t = time(10, 15)
        color = "Blue"
        timetable_stop_time = Timetable_stop_time_t_mos_ru(t, color)
        t2 = time(10, 15)
        color2 = "Red"
        timetable_stop_time2 = Timetable_stop_time_t_mos_ru(t2, color2)
        self.assertFalse(timetable_stop_time == timetable_stop_time2)
        self.assertTrue(timetable_stop_time != timetable_stop_time2)

    def test_timetable_stop_time_equal_false_time(self):
        t = time(10, 16)
        color = "Red"
        timetable_stop_time = Timetable_stop_time_t_mos_ru(t, color)
        t2 = time(10, 15)
        color2 = "Red"
        timetable_stop_time2 = Timetable_stop_time_t_mos_ru(t2, color2)
        self.assertFalse(timetable_stop_time == timetable_stop_time2)
        self.assertTrue(timetable_stop_time != timetable_stop_time2)

    def test_timetable_stop_time_equal_false_time_color(self):
        t = time(10, 16)
        color = "Blue"
        timetable_stop_time = Timetable_stop_time_t_mos_ru(t, color)
        t2 = time(10, 15)
        color2 = "Red"
        timetable_stop_time2 = Timetable_stop_time_t_mos_ru(t2, color2)
        self.assertFalse(timetable_stop_time == timetable_stop_time2)
        self.assertTrue(timetable_stop_time != timetable_stop_time2)

    def test_timetable_stop_time_str_without_color(self):
        t = time(23, 59)
        color = None
        timetable_stop_time = Timetable_stop_time_t_mos_ru(t, color)
        self.assertEqual(str(timetable_stop_time), "23:59")
        self.assertEqual(repr(timetable_stop_time), "23:59")

    def test_timetable_stop_time_str_with_color(self):
        t = time(1, 1)
        color = "Red"
        timetable_stop_time = Timetable_stop_time_t_mos_ru(t, color)
        self.assertEqual(str(timetable_stop_time), "01:01 (Red)")
        self.assertEqual(repr(timetable_stop_time), "01:01 (Red)")


# Timetable_stop don't use without builder

# class TestTimetable_stop_t_mos_ru(TestCase):
#     def test_timetable_stop(self):
#         name = "Улица Иванова"
#         times = [
#             Timetable_stop_time_t_mos_ru(time(10, 12), "Red"),
#             Timetable_stop_time_t_mos_ru(time(20, 30), None),
#         ]
#         stop = Timetable_stop_t_mos_ru(name, [10, 20], times)
#         self.assertEqual(stop.get_name(), name)
#         self.assertEqual(list(stop.get_times()), times)
#         self.assertEqual(stop.get_coords(), [10, 20])
#
#     def test_eq(self):
#         name = "Улица Иванова"
#         times = [
#             Timetable_stop_time_t_mos_ru(time(10, 12), "Red"),
#             Timetable_stop_time_t_mos_ru(time(20, 30), None),
#         ]
#         stop = Timetable_stop_t_mos_ru(name, [10, 20], times)
#         name2 = "Улица Иванова"
#         times2 = [
#             Timetable_stop_time_t_mos_ru(time(10, 12), "Red"),
#             Timetable_stop_time_t_mos_ru(time(20, 30), None),
#         ]
#         stop2 = Timetable_stop_t_mos_ru(name2, [10, 20], times2)
#         self.assertTrue(stop == stop2)
#         self.assertFalse(stop != stop2)
#
#     def test_eq_false_name(self):
#         name = "Улица Иванова"
#         times = [
#             Timetable_stop_time_t_mos_ru(time(10, 12), "Red"),
#             Timetable_stop_time_t_mos_ru(time(20, 30), None),
#         ]
#         stop = Timetable_stop_t_mos_ru(name, [10, 20], times)
#         name2 = "Улица Ивановаа"
#         times2 = [
#             Timetable_stop_time_t_mos_ru(time(10, 12), "Red"),
#             Timetable_stop_time_t_mos_ru(time(20, 30), None),
#         ]
#         stop2 = Timetable_stop_t_mos_ru(name2, [10, 20], times2)
#         self.assertFalse(stop == stop2)
#         self.assertTrue(stop != stop2)
#
#     def test_eq_false_time(self):
#         name = "Улица Иванова"
#         times = [
#             Timetable_stop_time_t_mos_ru(time(10, 12), "Red"),
#             Timetable_stop_time_t_mos_ru(time(20, 30), None),
#         ]
#         stop = Timetable_stop_t_mos_ru(name, [10, 20], times)
#         name2 = "Улица Иванова"
#         times2 = [
#             Timetable_stop_time_t_mos_ru(time(10, 13), "Red"),
#             Timetable_stop_time_t_mos_ru(time(20, 30), None),
#         ]
#         stop2 = Timetable_stop_t_mos_ru(name2, [10, 20], times2)
#         self.assertFalse(stop == stop2)
#         self.assertTrue(stop != stop2)
#
#     def test_eq_false_coords(self):
#         name = "Улица Иванова"
#         times = [
#             Timetable_stop_time_t_mos_ru(time(10, 12), "Red"),
#             Timetable_stop_time_t_mos_ru(time(20, 30), None),
#         ]
#         stop = Timetable_stop_t_mos_ru(name, [10, 20], times)
#         name2 = "Улица Иванова"
#         times2 = [
#             Timetable_stop_time_t_mos_ru(time(10, 12), "Red"),
#             Timetable_stop_time_t_mos_ru(time(20, 30), None),
#         ]
#         stop2 = Timetable_stop_t_mos_ru(name2, [10, 21], times2)
#         self.assertFalse(stop == stop2)
#         self.assertTrue(stop != stop2)
#
#     def test_eq_shake(self):
#         name = "Улица Иванова"
#         times = [
#             Timetable_stop_time_t_mos_ru(time(10, 12), "Red"),
#             Timetable_stop_time_t_mos_ru(time(20, 30), None),
#         ]
#         stop = Timetable_stop_t_mos_ru(name, [10, 20], times)
#         name2 = "Улица Иванова"
#         times2 = [
#             Timetable_stop_time_t_mos_ru(time(20, 30), None),
#             Timetable_stop_time_t_mos_ru(time(10, 12), "Red"),
#         ]
#         stop2 = Timetable_stop_t_mos_ru(name2, [10, 20], times2)
#         self.assertTrue(stop == stop2)
#         self.assertFalse(stop != stop2)


class TestTimetable_t_mos_ru(TestCase):

    def test_timetable_t_mos_ru(self):
        id_route_t_mos_ru = '393'
        direction = 1
        current_date = date(2022, 2, 20)
        times = [
            Timetable_stop_time_t_mos_ru(time(10, 12), "Red"),
            Timetable_stop_time_t_mos_ru(time(20, 30), None),
        ]
        stop = Timetable_stop_builder_t_mos_ru().set_name('ул. Иванова').set_coords([20, 30]). \
            add_item_timetable(times[0].get_time(), times[0].get_color_special_flight()). \
            add_item_timetable(times[1].get_time()).build()

        stops = [
            stop
        ]

        timetable = Timetable_t_mos_ru(id_route_t_mos_ru, direction, current_date, stops)
        self.assertEqual(timetable.get_id_route_t_mos_ru(), id_route_t_mos_ru)
        self.assertEqual(timetable.get_date(), current_date)
        self.assertEqual(timetable.get_stops(), stops)
        self.assertEqual(timetable.get_direction(), direction)
        for stop_current in timetable:
            self.assertEqual(stop_current, stop)


class TestTimetable_stop_builder_t_mos_ru(TestCase):
    def test_timetable_stop(self):
        name = "Улица Иванова"
        times = [
            Timetable_stop_time_t_mos_ru(time(10, 12), "Red"),
            Timetable_stop_time_t_mos_ru(time(20, 30), None),
        ]
        stop = Timetable_stop_builder_t_mos_ru().set_name(name). \
            add_item_timetable(times[0].get_time(), times[0].get_color_special_flight()). \
            add_item_timetable(times[1].get_time()). \
            set_coords([10, 20]).build()
        self.assertEqual(stop.get_name(), name)
        self.assertEqual(list(stop.get_times()), times)
        self.assertEqual(stop.get_coords(), [10, 20])

    pass


class TestTimetable_builder_t_mos_ru(TestCase):
    def test_timetable_builder_t_mos_ru(self):
        id_route_t_mos_ru = '393'
        direction = 1
        current_date = date(2022, 2, 20)
        times = [
            Timetable_stop_time_t_mos_ru(time(10, 12), "Red"),
            Timetable_stop_time_t_mos_ru(time(20, 30), None),
        ]
        stop = Timetable_stop_builder_t_mos_ru().set_name('ул. Иванова').set_coords([20, 30]). \
            add_item_timetable(times[0].get_time(), times[0].get_color_special_flight()). \
            add_item_timetable(times[1].get_time()).build()
        stops = [
            stop
        ]

        builder = Timetable_builder_t_mos_ru(). \
            set_date(current_date).set_direction(direction). \
            set_id_route_t_mos_ru(id_route_t_mos_ru)
        builder.add_stop().set_name('ул. Иванова').set_coords([20, 30]). \
            add_item_timetable(times[0].get_time(), times[0].get_color_special_flight()). \
            add_item_timetable(times[1].get_time())
        timetable = builder.build()
        self.assertEqual(timetable.get_id_route_t_mos_ru(), id_route_t_mos_ru)
        self.assertEqual(timetable.get_date(), current_date)
        self.assertEqual(timetable.get_stops(), stops)
        self.assertEqual(timetable.get_direction(), direction)
        for stop_current in timetable:
            self.assertEqual(stop_current, stop)

    pass
