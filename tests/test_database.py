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
      db_cursor.execute('DROP TABLE IF EXISTS office')
      db_cursor.execute('DROP TABLE IF EXISTS living')        
      db_cursor.execute('DROP TABLE IF EXISTS fellow')
      db_cursor.execute('DROP TABLE IF EXISTS staff')        
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
      
    def tearDown(self):
      self.office_data.close()
      self.living_data.close()
      self.fellow_data.close()
      self.staff_data.close()

    #def test_00_add_fellow_raises_error_no_room(self):
    #    self.amity.save_state(self.database_name)

    #def test_02_office_saved_in_data(self):
    #  self.amity.create_room('neptune','office')  # Create a sample office
    
    #def test_03_test_office_saved_in_data(self):
    #  self.assertTrue('neptune' in self.office_data)

    #def test_04_office_object_created(self):
    #  self.assertTrue(type(self.office_data['neptune']), Office)
    
    #if __name__ == '__main__':
    #unittest.main(verbosity=2)
    

