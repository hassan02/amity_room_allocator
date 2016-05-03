import os,sys

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
      
      database_name = 'tests/test_data_files/test_amity_data.db'
      db_conn = sqlite3.connect(database_name)
      db_cursor = db_conn.cursor()
      db_cursor.execute('DROP TABLE if exists office')
      db_cursor.execute('DROP TABLE if exists living')        
      db_cursor.execute('DROP TABLE if exists fellow')
      db_cursor.execute('DROP TABLE if exists staff')    
      db_conn.commit()
      db_conn.close()
      # Set up a connection and cursor
        
    
    def setUp(self):
      self.held = sys.stdout
      sys.stdout =  StringIO()
      self.database_name = 'tests/test_data_files/test_amity_data.db'
      self.db_conn = sqlite3.connect(self.database_name)
      self.db_cursor = self.db_conn.cursor()
      self.test_office_file = 'tests/test_data_files/test_offices'
      self.test_living_file = 'tests/test_data_files/test_living'
      self.test_fellow_file = 'tests/test_data_files/test_fellows'
      self.test_staff_file = 'tests/test_data_files/test_staff'
      
      self.amity = Amity(self.test_office_file, self.test_living_file, self.test_fellow_file, self.test_staff_file, )
      
      self.office_data = shelve.open(self.test_office_file)
      self.living_data = shelve.open(self.test_living_file)
      self.fellow_data = shelve.open(self.test_fellow_file)
      self.staff_data = shelve.open(self.test_staff_file)
    
    @classmethod
    def tearDownClass(TestDatabase):
      pass
      '''
      database_name = 'tests/test_data_files/test_amity_data.db'
      db_conn = sqlite3.connect(database_name)
      db_cursor = db_conn.cursor()
      db_cursor.execute('DROP TABLE if exists office')
      db_cursor.execute('DROP TABLE if exists living')        
      db_cursor.execute('DROP TABLE if exists fellow')
      db_cursor.execute('DROP TABLE if exists staff')        
      db_conn.commit()
      db_conn.close()
      '''
      
    def tearDown(self):
        self.office_data.close()
        self.living_data.close()
        self.fellow_data.close()
        self.staff_data.close()
    
    def test_00_save_state(self):
        self.amity.save_state(self.database_name)

    def test_01_check_office_in_database(self):
        officequery = "SELECT * FROM office"
        self.db_cursor.execute(officequery)
        results = self.db_cursor.fetchall()
        all_rooms = [ str(row[1]) for row in results]
        self.assertTrue('neptune' in all_rooms)

    def test_02_check_living_in_database(self):
        livingquery = "SELECT * FROM living"
        self.db_cursor.execute(livingquery)
        results = self.db_cursor.fetchall()
        all_rooms = [ str(row[1]) for row in results]
        self.assertTrue('iroko' in all_rooms)

    def test_03_check_fellow_in_database(self):
        fellowquery = "SELECT * FROM fellow"
        self.db_cursor.execute(fellowquery)
        results = self.db_cursor.fetchall()
        all_fellows = [ str(row[2]) for row in results]
        self.assertTrue('ADEOLA ADEDOYIN' in all_fellows)

    def test_04_check_staff_in_database(self):
        staffquery = "SELECT * FROM staff"
        self.db_cursor.execute(staffquery)
        results = self.db_cursor.fetchall()
        all_staff = [ str(row[2]) for row in results]
        self.assertTrue('NADAYAR ENGESI' in all_staff)

    def test_05_load_state(self):
        self.amity.load_state(self.database_name)

    def test_06_check_if_office_loaded(self):
        self.assertTrue('neptune' in self.office_data)

    def test_07_check_if_office_loaded(self):
        self.assertTrue('saturn' in self.office_data)

    def test_08_check_if_living_loaded(self):
        self.assertTrue('iroko' in self.living_data)
    
    def test_09_check_if_living_loaded(self):
        self.assertTrue('cedar' in self.living_data)

    def test_10_check_if_fellow_in_living(self):
        self.assertTrue('ADEOLA ADEDOYIN' in self.living_data['iroko'].members.values())

    def test_12_check_if_staff_in_office(self):
        self.assertTrue('GODSON UKPERE' in self.office_data['neptune'].members.values())


    
if __name__ == '__main__':
    unittest.main()