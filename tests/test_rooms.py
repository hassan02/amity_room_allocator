from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from model.person import Person
from model.fellow import Fellow
from model.staff import Staff
from model.room import Room
from model.office import Office
from model.living import Living
import unittest

class TestRoom(unittest.TestCase):
    room = Room('Orion')
    def test_new_room_class(self):
        self.assertIsInstance(self.room, Room)
    def test_new_room_name(self):
        self.assertEqual(self.room.room_name, 'Orion')
    def test_new_room_members(self):
        self.assertEqual(self.room.members, {})
    def test_new_room_occupants(self):
        self.assertEqual(self.room.no_of_occupants, 0)

class TestOffice(unittest.TestCase):
    office = Office('Neptune')
    def test_new_office_class(self):
        self.assertIsInstance(self.office, Office)
    def test_new_office_name(self):
        self.assertEqual(self.office.room_name, 'Neptune')
    def test_new_office_members(self):
        self.assertEqual(self.office.members, {})
    def test_new_office_occupants(self):
        self.assertEqual(self.office.no_of_occupants, 0)

class TestLiving(unittest.TestCase):
    living = Living('Iroko')
    def test_new_living_class(self):
        self.assertIsInstance(self.living, Living)
    def test_new_living_name(self):
        self.assertEqual(self.living.room_name, 'Iroko')
    def test_new_living_members(self):
        self.assertEqual(self.living.members, {})
    def test_new_living_occupants(self):
        self.assertEqual(self.living.no_of_occupants, 0)
if __name__ == '__main__':
    unittest.main()