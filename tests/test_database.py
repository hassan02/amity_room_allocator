from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import os

import shelve
import unittest
import sqlite3

from data.data_manager import DataManager
from model.amity_model import Amity
from model.office import Office
from model.living import Living
from cStringIO import StringIO

class TestDatabase(unittest.TestCase):
    
    @classmethod
    def setUpClass(TestDatabase):
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
        sys.stdout =  StringIO()
        self.database_name = 'tests/test_data_files/test_amity_database.db'
        self.db_conn = sqlite3.connect(self.database_name)
        self.db_cursor = self.db_conn.cursor()
        self.test_rooms_file = 'tests/test_data_files/test_rooms'
        self.test_persons_file = 'tests/test_data_files/test_persons'
        
        self.amity = Amity(self.test_rooms_file, self.test_persons_file)
        
        self.rooms_data = shelve.open(self.test_rooms_file)
        self.persons_data = shelve.open(self.test_persons_file)
      
    @classmethod
    def tearDownClass(TestDatabase):
        pass
      
    def tearDown(self):
        self.rooms_data.close()
        self.persons_data.close()
    
    def test_01_save_state(self):
        self.amity.save_state(self.database_name)

    def test_02_check_office_in_database(self):
        officequery = "SELECT * FROM rooms"
        self.db_cursor.execute(officequery)
        results = self.db_cursor.fetchall()
        all_rooms = [ str(row[1]) for row in results]
        self.assertTrue('neptune' in all_rooms)

    def test_03_check_living_in_database(self):
        livingquery = "SELECT * FROM rooms"
        self.db_cursor.execute(livingquery)
        results = self.db_cursor.fetchall()
        all_rooms = [ str(row[1]) for row in results]
        self.assertTrue('iroko' in all_rooms)

    def test_04_check_fellow_in_database(self):
        fellowquery = "SELECT * FROM persons"
        self.db_cursor.execute(fellowquery)
        results = self.db_cursor.fetchall()
        all_fellows = [ str(row[2]) for row in results]
        self.assertTrue('ADEOLA ADEDOYIN' in all_fellows)

    def test_05_check_staff_in_database(self):
        staffquery = "SELECT * FROM persons"
        self.db_cursor.execute(staffquery)
        results = self.db_cursor.fetchall()
        all_staff = [ str(row[2]) for row in results]
        self.assertTrue('NADAYAR ENGESI' in all_staff)

    def test_06_load_state(self):
        self.amity.load_state(self.database_name)

    def test_07_check_if_office_loaded(self):
        self.assertTrue('neptune' in self.rooms_data)

    def test_08_check_if_office_loaded(self):
        self.assertTrue('saturn' in self.rooms_data)

    def test_09_check_if_living_loaded(self):
        self.assertTrue('iroko' in self.rooms_data)
    
    def test_10_check_if_living_loaded(self):
        self.assertTrue('cedar' in self.rooms_data)

    def test_11_check_if_fellow_in_living(self):
        self.assertTrue('ADEOLA ADEDOYIN' in \
            self.rooms_data['iroko'].members.values())

    def test_12_check_if_staff_in_office(self):
        self.assertTrue('BUKOLA MAKINWA' in \
            self.rooms_data['neptune'].members.values())
    
if __name__ == '__main__':
    unittest.main()