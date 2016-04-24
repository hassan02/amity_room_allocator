import shelve
import unittest
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from data.data_manager import DataManager
from model.amity_model import Amity

class TestCreateOffice(unittest.TestCase):
    test_id_list = 'tests/test_data_files/test_persons_ids'
    test_office_data = 'tests/test_data_files/test_offices'
    test_living_data = 'tests/test_data_files/test_living'
    new_amity = Amity(test_office_data, test_living_data)
    
    myid = shelve.open(test_office_data)

    def test_office_creation(self):
      self.new_amity.create_office('neptune')
      self.assertEqual(1,len(self.myid))
      
    def test_office_saved_in_data(self):
      self.assertIn('neptune',self.myid)
      self.close_file()
      
    def test_office_removal(self):
      self.myid = shelve.open(self.test_office_data)
      self.new_amity.remove_room('neptune')
      self.assertEqual(0,len(self.myid))
      
    def close_file(self):
      self.myid.close()

class TestCreateLiving(unittest.TestCase):
    test_id_list = 'tests/test_data_files/test_persons_ids'
    test_office_data = 'tests/test_data_files/test_offices'
    test_living_data = 'tests/test_data_files/test_living'
    new_amity = Amity(test_office_data, test_living_data)
    
    myid = shelve.open(test_living_data)

    def test_living_creation(self):
      self.new_amity.create_living('iroko')
      self.assertEqual(1,len(self.myid))
      
    def test_living_saved_in_data(self):
      self.assertIn('iroko',self.myid)
      self.close_file()
      
    def test_living_removal(self):
      self.myid = shelve.open(self.test_living_data)
      self.new_amity.remove_room('iroko')
      self.assertEqual(0,len(self.myid))
      
    def close_file(self):
      self.myid.close()


if __name__ == '__main__':
    unittest.main()

