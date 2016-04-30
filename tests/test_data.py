import shelve
import unittest

from data.data_manager import DataManager
from model.amity_model import Amity
from cStringIO import StringIO # or from StringIO ...
import sys

class TestCreateRoom(unittest.TestCase):
    def setUp(self):
      self.held, sys.stdout = sys.stdout, StringIO()
      self.test_id_list = 'tests/test_data_files/test_persons_ids'
      self.test_office_data = 'tests/test_data_files/test_offices'
      self.test_living_data = 'tests/test_data_files/test_living'
      #self.clear_files()
      self.amity = Amity(self.test_office_data, self.test_living_data)
      
      self.office_file = shelve.open(self.test_office_data)
      self.living_file = shelve.open(self.test_living_data)

    def test_office_creation(self):
      self.amity.create_room('neptune','office')
      self.assertEqual(1,len(self.office_file))

    # def test_office_saved_in_data(self):
    # self.assertIn('neptune',self.office_file)

    def test_create_same_office(self):
      self.amity.create_room('Neptune','office')
      self.assertEqual(sys.stdout.getvalue(), 'Room NEPTUNE already exist\n')

    def test_create_same_office(self):
      self.amity.create_room('Neptune','office')
      self.assertEqual(sys.stdout.getvalue(), 'Room NEPTUNE already exist\n')


      def test_create_same_office(self):
      self.amity.create_room('Neptune','office')
      self.assertEqual(sys.stdout.getvalue(), 'Room NEPTUNE already exist\n')

    def test_print_office_room(self):
      self.amity.print_room('neptune')
      displayline = '..............................................................................'
      self.assertEqual(sys.stdout.getvalue(), 'Loading NEPTUNE (OFFICE) members...\nNEPTUNE(OFFICE) - 0 of 6\n%s\nEMPTY\n\n\n'%(displayline))
      
    def clear_files(self):
      del self.test_office_data
      del self.test_living_data

    """
    def test_office_removal(self):
      self.myid = shelve.open(self.test_office_data)
      self.amity.remove_room('neptune')
      self.assertEqual(0,len(self.myid))
    
    def test_office_removed_from_data(self):
      self.myid = shelve.open(self.test_office_data)
      self.assertNotIn('neptune',self.myid)
     
    def close_file(self):
      self.myid.close()
    """

    def test_living_creation(self):
      self.amity.create_room('iroko','living')
      self.assertEqual(1,len(self.living_file))
      
    # def test_living_saved_in_data(self):
    #  self.assertIn('iroko',self.living_file)

    def test_create_same_living(self):
      self.amity.create_room('iroko','living')
      self.assertEqual(sys.stdout.getvalue(), 'Room IROKO already exist\n')
      self.clear_files()

    def test_print_living_room(self):
      self.amity.print_room('iroko')
      displayline = '..............................................................................'
      self.assertEqual(sys.stdout.getvalue(), 'Loading IROKO (LIVING) members...\nIROKO(LIVING) - 0 of 4\n%s\nEMPTY\n\n\n'%(displayline))
    
    """
    def test_living_removal(self):
      self.myid = shelve.open(self.test_living_data)
      self.amity.remove_room('iroko')
      self.assertEqual(0,len(self.myid))

    def test_living_removed_from_data(self):
      self.myid = shelve.open(self.test_living_data)
      self.assertNotIn('iroko',self.myid)
    """
      
    def close_file(self):
      self.myid.close()
    
    def clear_files(self):
      del self.test_office_data
      del self.test_living_data

    def test_print_all_room(self):
      self.amity.print_allocations()
      displayline = '..............................................................................'
      finaldisp = 'Loading All Offices...\nNEPTUNE(OFFICE) - 0 of 6\n%s\nEMPTY\n\n\n'%(displayline)
      finaldisp += 'Loading All Living Rooms...\nIROKO(LIVING) - 0 of 4\n%s\nEMPTY\n\n\n'%(displayline)
      self.assertEqual(sys.stdout.getvalue(), finaldisp)


if __name__ == '__main__':
    unittest.main(verbosity=2)
    

