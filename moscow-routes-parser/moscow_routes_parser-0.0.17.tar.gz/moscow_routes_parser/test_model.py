from unittest import TestCase

from moscow_routes_parser.model import Equipment, Route


class TestEquipment(TestCase):
    def test_equipment_tramway(self):
        equipment = Equipment.tramway()
        self.assertEqual(equipment.to_number(), Equipment.tramway().to_number())
        self.assertEqual(Equipment.by_number(equipment.to_number()), equipment)
        self.assertEqual(equipment, Equipment.tramway())

    def test_equipment_bus(self):
        equipment = Equipment.bus()
        self.assertEqual(equipment.to_number(), Equipment.bus().to_number())
        self.assertEqual(Equipment.by_number(equipment.to_number()), equipment)
        self.assertEqual(equipment, Equipment.bus())

    def test_equipment_trolleybus(self):
        equipment = Equipment.trolleybus()
        self.assertEqual(equipment.to_number(), Equipment.trolleybus().to_number())
        self.assertEqual(Equipment.by_number(equipment.to_number()), equipment)
        self.assertEqual(equipment, Equipment.trolleybus())


    def test_str(self):
        self.assertEqual(Equipment.tramway().to_str(), "tramway")
        self.assertEqual(Equipment.trolleybus().to_str(), "trolleybus")
        self.assertEqual(Equipment.bus().to_str(), "bus")

    def test_ne(self):
        self.assertTrue(Equipment.tramway() != Equipment.bus())
        self.assertTrue(Equipment.tramway() != Equipment.trolleybus())
        self.assertTrue(Equipment.bus() != Equipment.trolleybus())

    def test_hash(self):
        self.assertTrue(hash(Equipment.tramway()) != hash(Equipment.bus()))
        self.assertTrue(hash(Equipment.tramway()) != hash(Equipment.trolleybus()))
        self.assertTrue(hash(Equipment.bus()) != hash(Equipment.trolleybus()))
        self.assertTrue(hash(Equipment.tramway()) == hash(Equipment.tramway()))
        self.assertTrue(hash(Equipment.trolleybus()) == hash(Equipment.trolleybus()))
        self.assertTrue(hash(Equipment.bus()) == hash(Equipment.bus()))



class TestRoute(TestCase):
    def test_route(self):
        route = Route('937', Equipment.tramway(), 'A')
        self.assertEqual(route.get_equipment(), Equipment.tramway())
        self.assertEqual(route.get_name(), "A")
        self.assertEqual(route.get_id_mgt(), "937")

    def test_eq(self):
        route = Route('937', Equipment.tramway(), 'A')
        route2 = Route('937', Equipment.tramway(), 'A')
        self.assertTrue(route == route2)
        route3 = Route('936', Equipment.tramway(), 'A')
        route4 = Route('937', Equipment.bus(), 'A')
        route5 = Route('937', Equipment.tramway(), 'A2')
        self.assertFalse(route == route3)
        self.assertFalse(route == route4)
        self.assertFalse(route == route5)

    def test_ne(self):
        route = Route('937', Equipment.tramway(), 'A')
        route2 = Route('937', Equipment.tramway(), 'A')
        self.assertFalse(route != route2)
        route3 = Route('936', Equipment.tramway(), 'A')
        route4 = Route('937', Equipment.bus(), 'A')
        route5 = Route('937', Equipment.tramway(), 'A2')
        self.assertTrue(route != route3)
        self.assertTrue(route != route4)
        self.assertTrue(route != route5)

    def test_list(self):
        route = Route('937', Equipment.tramway(), 'A')
        route2 = Route('937', Equipment.tramway(), 'A')
        self.assertTrue(route in [route2])
        route3 = Route('936', Equipment.tramway(), 'A')
        self.assertFalse(route in [route3])
