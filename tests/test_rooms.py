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
    """Test cases for Room class"""
    room = Room('Orion')

    def test_new_room_class(self):
        self.assertEqual(type(self.room), Room)

    def test_new_room_name(self):
        self.assertEqual(self.room.name, 'Orion')

    def test_new_room_members(self):
        self.assertEqual(self.room.members, {})

    def test_new_room_occupants(self):
        self.assertEqual(self.room.no_of_occupants, 0)

    def test_create_room_raises_error(self):
        self.assertRaises(Exception, Room, [1, 3, 4])


class TestOffice(unittest.TestCase):
    """Test cases for Office class"""
    office = Office('Neptune')

    def test_new_office_class(self):
        self.assertEqual(type(self.office), Office)

    def test_new_office_name(self):
        self.assertEqual(self.office.name, 'Neptune')

    def test_new_office_members(self):
        self.assertEqual(self.office.members, {})

    def test_new_office_occupants(self):
        self.assertEqual(self.office.no_of_occupants, 0)

    def test_new_office_max_occupants(self):
        self.assertEqual(self.office.max_occupants, 6)

    def test_create_office_raises_error(self):
        self.assertRaises(Exception, Office, 5)


class TestLiving(unittest.TestCase):
    """Test cases for Living class"""
    living = Living('Iroko')

    def test_new_living_class(self):
        self.assertEqual(type(self.living), Living)

    def test_new_living_name(self):
        self.assertEqual(self.living.name, 'Iroko')

    def test_new_living_members(self):
        self.assertEqual(self.living.members, {})

    def test_new_living_occupants(self):
        self.assertEqual(self.living.no_of_occupants, 0)

    def test_new_living_max_occupants(self):
        self.assertEqual(self.living.max_occupants, 4)

    def test_create_living_raises_error(self):
        self.assertRaises(Exception, Living, {'obeche': 'living'})

if __name__ == '__main__':
    unittest.main()
