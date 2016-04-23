import shelve
import unittest
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from data.data_manager import DataManager

class TestCreateOffice(unittest.TestCase):
    test_id_list = 'test_persons_ids'
    test_office_data = 'test_offices'
    test_living_data = 'test_living'
    newdata = DataManager(test_id_list,test_office_data,test_living_data)
    
    myid = shelve.open(test_office_data)

    def test_office_creation(self):
      self.newdata.save_office('neptune')
      self.assertEqual(1,len(self.myid))

    def test_office_in_data(self):
      self.assertIn('neptune',self.myid)
      self.myid.close()

class TestCreateLiving(unittest.TestCase):
    test_id_list = 'test_persons_ids'
    test_office_data = 'test_offices'
    test_living_data = 'test_living'
    newdata = DataManager(test_id_list,test_office_data,test_living_data)
    
    myid = shelve.open(test_living_data)

    def test_living_creation(self):
      self.newdata.save_living('mahogany')
      self.assertEqual(1,len(self.myid))
    
    def test_living_saved_in_data(self):
      self.assertIn('mahogany',self.myid)
      self.myid.close()

class TestOfficeRemoval(unittest.TestCase):
    test_id_list = 'test_persons_ids'
    test_office_data = 'test_offices'
    test_living_data = 'test_living'
    newdata = DataManager(test_id_list,test_office_data,test_living_data)
    
    myid = shelve.open(test_office_data)

    def test_office_removal(self):
      myid = shelve.open(self.test_office_data)
      self.newdata.remove_room('neptune')
      self.assertEqual(0,len(self.myid))
      self.myid.close()

class TestLivingRemoval(unittest.TestCase):
    test_id_list = 'test_persons_ids'
    test_office_data = 'test_offices'
    test_living_data = 'test_living'
    newdata = DataManager(test_id_list,test_office_data,test_living_data)
    
    myid = shelve.open(test_living_data)

    def test_living_removal(self):
      myid = shelve.open(self.test_living_data)
      self.newdata.remove_room('mahogany')
      self.assertEqual(0,len(self.myid))
      self.myid.close()

if __name__ == '__main__':
    unittest.main()