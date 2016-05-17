from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
import os
import shelve
import sqlite3
import unittest

from data.data_manager import DataManager
from model.amity_model import Amity
from model.office import Office
from model.living import Living
from cStringIO import StringIO


class TestDatabase(unittest.TestCase):
    """Test cases for Amity"""
    @classmethod
    def setUpClass(cls):
        # Clear entry in the database
        database_name = 'tests/test_data_files/test_amity_database.db'
        db_conn = sqlite3.connect(database_name)
        db_cursor = db_conn.cursor()
        db_cursor.execute('DROP TABLE if exists rooms')
        db_cursor.execute('DROP TABLE if exists persons')
        db_conn.commit()
        db_conn.close()

    def setUp(self):
        # Set up the class with room file, person file and database file
        self.held = sys.stdout
        sys.stdout = StringIO()
        self.database_name = 'tests/test_data_files/test_amity_database.db'
        self.db_conn = sqlite3.connect(self.database_name)
        self.db_cursor = self.db_conn.cursor()
        self.test_rooms_file = 'tests/test_data_files/test_rooms'
        self.test_persons_file = 'tests/test_data_files/test_persons'

        self.rooms_data = shelve.open(self.test_rooms_file)
        self.persons_data = shelve.open(self.test_persons_file)
        self.amity = Amity(self.test_rooms_file, self.test_persons_file)
        room_dict = {'saturn': 'office', 'cedar':'living'}
        person_dict = {"fellow": ['ADEOLA', 'ADEDOYIN', 'Y'], "staff": ['NADAYAR', 'ENGESI','N'] }
        self.amity.create_room('saturn','office')
        
        self.rooms_data = shelve.open(self.test_rooms_file)
        self.amity = Amity(self.test_rooms_file, self.test_persons_file)
        self.amity.create_room('cedar','living')
        self.rooms_data = shelve.open(self.test_rooms_file)
        self.amity = Amity(self.test_rooms_file, self.test_persons_file)
        
        for person_type, person_info in person_dict.items():
            self.rooms_data = shelve.open(self.test_rooms_file)
            self.persons_data = shelve.open(self.test_persons_file)
            self.amity.add_person(person_info[0],person_info[1],person_type, person_info[2])
            self.amity = Amity(self.test_rooms_file, self.test_persons_file)
        self.amity.save_state(self.database_name)
        self.amity = Amity(self.test_rooms_file, self.test_persons_file)
        self.amity.load_state(self.database_name)
        self.rooms_data = shelve.open(self.test_rooms_file)
        self.persons_data = shelve.open(self.test_persons_file)
        


    def tearDown(self):
        self.rooms_data.close()
        self.persons_data.close()

    def test_save_state(self):
        officequery = "SELECT * FROM rooms"
        self.db_cursor.execute(officequery)
        results = self.db_cursor.fetchall()
        all_rooms = [str(row[1]) for row in results]
        self.assertTrue('saturn' in all_rooms)

        livingquery = "SELECT * FROM rooms"
        self.db_cursor.execute(livingquery)
        results = self.db_cursor.fetchall()
        all_rooms = [str(row[1]) for row in results]
        self.assertTrue('cedar' in all_rooms)

        fellowquery = "SELECT * FROM persons"
        self.db_cursor.execute(fellowquery)
        results = self.db_cursor.fetchall()
        all_fellows = [str(row[2]) for row in results]
        self.assertTrue('ADEOLA ADEDOYIN' in all_fellows)

        staffquery = "SELECT * FROM persons"
        self.db_cursor.execute(staffquery)
        results = self.db_cursor.fetchall()
        all_staff = [str(row[2]) for row in results]
        self.assertTrue('NADAYAR ENGESI' in all_staff)

    def test_load_state(self):
        self.assertTrue('saturn' in self.rooms_data)
        self.assertTrue('cedar' in self.rooms_data)
        self.assertTrue('ADEOLA ADEDOYIN' in self.rooms_data['saturn'].members.values())
        self.assertTrue('ADEOLA ADEDOYIN' in self.rooms_data['cedar'].members.values())
        self.assertTrue('NADAYAR ENGESI' in self.rooms_data['saturn'].members.values())

if __name__ == '__main__':
    unittest.main()
