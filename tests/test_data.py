from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import shelve
import unittest

from remove import Remove
from data.data_manager import DataManager
from model.amity_model import Amity
from model.office import Office
from model.living import Living
from cStringIO import StringIO # or from StringIO ...
import sys, os

Remove()
class TestCreateRoom(unittest.TestCase):
    @classmethod
    def setUpClass(TestCreateRoom):
      if os.path.isfile(os.path.realpath('tests/test_data_files/test_persons_ids.db')):
        os.remove(os.path.realpath('tests/test_data_files/test_persons_ids.db'))
      if os.path.isfile(os.path.realpath('tests/test_data_files/test_offices.db')):
        os.remove(os.path.realpath('tests/test_data_files/test_offices.db'))
      if os.path.isfile(os.path.realpath('tests/test_data_files/test_living.db')):
        os.remove(os.path.realpath("tests/test_data_files/test_living.db"))
      if os.path.isfile(os.path.realpath('tests/test_data_files/test_fellows.db')):
        os.remove(os.path.realpath("tests/test_data_files/test_fellows.db"))
      if os.path.isfile(os.path.realpath('test/test_data_files/test_staff.db')):
        os.remove(os.path.realpath("tests/test_data_files/test_staff.db"))
    
    def setUp(self):
      self.held, sys.stdout = sys.stdout, StringIO()
      self.test_office_file = 'tests/test_data_files/test_offices'
      self.test_living_file = 'tests/test_data_files/test_living'
      self.test_fellow_file = 'tests/test_data_files/test_fellows'
      self.test_staff_file = 'tests/test_data_files/test_staff'
      
      #self.clear_files()
      self.amity = Amity(self.test_office_file, self.test_living_file, self.test_fellow_file, self.test_staff_file)
      
      self.office_data = shelve.open(self.test_office_file)
      self.living_data = shelve.open(self.test_living_file)
      self.fellow_data = shelve.open(self.test_fellow_file)
      self.staff_data = shelve.open(self.test_staff_file)
    
    @classmethod
    def tearDownClass(cls):
      pass

      
    def tearDown(self):
      self.office_data.close()
      self.living_data.close()
      self.fellow_data.close()
      self.staff_data.close()
    def test_00_office_saved_in_data(self):
      self.amity.create_room('neptune','office')  # Create a sample office
    def test_01_test_office_saved_in_data(self):
      self.assertTrue('neptune' in self.office_data)

    def test_02_office_object_created(self):
      self.assertTrue(type(self.office_data['neptune']), Office)
    
    def test_03_office_creation(self):
      self.assertEqual(1,len(self.office_data))
    
    def test_04_office_name(self):
      self.assertEqual('neptune',self.office_data['neptune'].name.lower())

    def test_05_office_members_is_empty(self):
      self.assertEqual(self.office_data['neptune'].members,{})
    
    def test_06_office_no_of_occupants(self):
      self.assertEqual(self.office_data['neptune'].no_of_occupants, 0)

    def test_07_office_max_occupants(self):
      self.assertEqual(self.office_data['neptune'].max_occupants, 6)

    #def test_create_same_office(self):
    #  self.amity.create_room('neptune','office')
    #  self.assertEqual(sys.stdout.getvalue(), 'Room NEPTUNE already exist\n')

    def test_08_create_office_raises_error(self):
      self.assertRaises(Exception, self.amity.create_room, [2,4,5],'office')

    def test_09_create_room_wrong_type_raises_error(self):
      self.assertRaises(Exception, self.amity.create_room, 'Cafeteria','refresh')

    def test_10_print_office_room(self):
      self.amity.print_room('neptune')
      displayline = '..............................................................................'
      self.assertEqual(sys.stdout.getvalue(), 'Loading NEPTUNE (OFFICE) members...\nNEPTUNE(OFFICE) - 0 of 6\n%s\nEMPTY\n\n\n'%(displayline))

    #def test_remove_office(self):
    #  self.amity.remove_room('mars')
    #def test_new_office_creation(self):
    #  self.amity.create_room('saturn','office')
    #  self.assertTrue('saturn' in self.office_data)

    #def test_new_office_creation(self):
    #  self.assertEqual(2,len(self.office_data))
    

    #def test_office_removal(self):
    #  self.amity.remove_room('saturn')
    #  self.assertTrue('saturn' not in self.office_data)
  
    def test_11_living_creation(self):
      self.amity.create_room('iroko','living')
      self.assertEqual(1,len(self.living_data))
      
    def test_12_living_saved_in_data(self):
      self.amity.create_room('iroko','living')  # Create a sample office
      self.assertTrue('iroko' in self.living_data)

    def test_13_created_living_object(self):
      self.assertEqual(type(self.living_data['iroko']), Living)
    
    #def test_office_object_created(self):
    #  neptune = Office('neptune')
    #  self.assertEqual(neptune, self.office_data['neptune'])

    def test_14_living_creation(self):
      self.assertEqual(1,len(self.living_data))
    
    def test_15_living_name(self):
      self.assertEqual('iroko', self.living_data['iroko'].name.lower())

    def test_16_living_members_is_empty(self):
      self.assertEqual(self.living_data['iroko'].members, {})
    
    def test_17_living_no_of_occupants(self):
      self.assertEqual(self.living_data['iroko'].no_of_occupants, 0)

    def test_18_living_max_occupants(self):
      self.assertEqual(self.living_data['iroko'].max_occupants, 4)

    #def test_create_same_living(self):
    #  self.amity.create_room('Iroko','living')
    #  self.assertEqual(sys.stdout.getvalue(), 'Room IROKO already exist\n')

    def test_19_create_living_wrong_type_raises_error(self):
      self.assertRaises(Exception, self.amity.create_room, ['Mahogany'],'living')

    def test_20_print_living_room(self):
      self.amity.print_room('iroko')
      displayline = '..............................................................................'
      self.assertEqual(sys.stdout.getvalue(), 'Loading IROKO (LIVING) members...\nIROKO(LIVING) - 0 of 4\n%s\nEMPTY\n\n\n'%(displayline))

    def test_21_reallocate_wrong_id_raises_error(self):
      self.assertRaises(Exception, self.amity.reallocate_person, 'ABDCQ','iroko')

    def test_22_allocate_fellow(self):
      self.amity.add_person('Adeola','Adedoyin','fellow','y')
    
    def test_23_test_allocate_fellow(self):
      self.amity.print_room('iroko')
      displayline = '..............................................................................'
      self.assertEqual(sys.stdout.getvalue(), 'Loading IROKO (LIVING) members...\nIROKO(LIVING) - 1 of 4\n%s\nADEOLA ADEDOYIN\n\n\n'%(displayline))

    def test_24_unallocated(self):
      self.amity.add_person('Adedoyin', 'Israel', 'fellow')      
      
    def test_25_print_unallocated(self):
      self.amity.print_unallocated()
      self.assertEqual(sys.stdout.getvalue(), 'Loading all unallocated people...\nADEDOYIN ISRAEL (FELLOW)\n\n')

    def test_26_allocate_staff(self):
      self.amity.add_person('Bukola','Makinwa','staff')
    
    def test_27_test_allocate_fellow(self):
      self.amity.print_room('neptune')
      displayline = '..............................................................................'
      self.assertEqual(sys.stdout.getvalue(), 'Loading NEPTUNE (OFFICE) members...\nNEPTUNE(OFFICE) - 1 of 6\n%s\nBUKOLA MAKINWA\n\n\n'%(displayline))
    

    '''
    class TestAllocations(TestCreateRoom):
    if os.path.isfile(os.path.realpath('test_data_files/test_persons_ids.db')):
      os.remove(os.path.realpath('test_data_files/test_persons_ids.db')) 
    if os.path.isfile(os.path.realpath('test_data_files/test_offices.db')):
      os.remove(os.path.realpath("test_data_files/test_offices.db"))
    if os.path.isfile(os.path.realpath('test_data_files/test_living.db')):
      os.remove(os.path.realpath("test_data_files/test_living.db"))
    if os.path.isfile(os.path.realpath('test_data_files/test_fellows.db')):
      os.remove(os.path.realpath("test_data_files/test_fellows.db"))
    if os.path.isfile(os.path.realpath('test_data_files/test_staff.db')):
      os.remove(os.path.realpath("test_data_files/test_staff.db"))

    def setUp(self):
      self.held, sys.stdout = sys.stdout, StringIO()
      self.test_office_file = 'tests/test_data_files/test_offices'
      self.test_living_file = 'tests/test_data_files/test_living'
      self.test_fellow_file = 'tests/test_data_files/test_fellows'
      self.test_staff_file = 'tests/test_data_files/test_staff'
      
      #self.clear_files()
      self.amity = Amity(self.test_office_file, self.test_living_file, self.test_fellow_file, self.test_staff_file)
      
      self.office_data = shelve.open(self.test_office_file)
      self.living_data = shelve.open(self.test_living_file)
      self.fellow_data = shelve.open(self.test_fellow_file)
      self.staff_data = shelve.open(self.test_staff_file)

    def tearDown(self):
      self.office_data.close()
      self.living_data.close()
      self.fellow_data.close()
      self.staff_data.close()

    def test_allocate_person(self):
      self.amity.add_person('Adeola','Adedoyin','fellow','y')
      
      def tearDown(self):
        self.office_data.close()
        self.living_data.close()
        self.fellow_data.close()
        self.staff_data.close() 

      
      def test_living_removal(self):
        self.myid = shelve.open(self.test_living_data)
        self.amity.remove_room('iroko')
        self.assertEqual(0,len(self.myid))

      def test_living_removed_from_data(self):
        self.myid = shelve.open(self.test_living_data)
        self.assertNotIn('iroko',self.myid)
      """
      #def test_print_living_room_after_allocation(self):
      #  self.amity.print_room('iroko')
      #  displayline = '..............................................................................'
      #  self.assertEqual(sys.stdout.getvalue(), 'Loading IROKO (LIVING) members...\nIROKO(LIVING) - 1 of 4\n%s\nADEOLA ADEDOYIN\n\n\n'%(displayline))

      #def test_print_all_room(self):
      #  self.amity.print_allocations()
      #  displayline = '..............................................................................'
      #  finaldisp = 'Loading All Offices...\nNEPTUNE(OFFICE) - 0 of 6\n%s\nEMPTY\n\n\n'%(displayline)
      #  finaldisp += 'Loading All Living Rooms...\nIROKO(LIVING) - 1 of 4\n%s\nADEOLA ADEDOYIN\n\n\n'%(displayline)
      #  self.assertEqual(sys.stdout.getvalue(), finaldisp)

      def test_close_file(self):
        
          os.remove(os.path.realpath("tests/test_data_files/test_offices.db"))
          os.remove(os.path.realpath("tests/test_data_files/test_living.db"))
          os.remove(os.path.realpath("tests/test_data_files/test_fellows.db"))
          os.remove(os.path.realpath("tests/test_data_files/test_staff.db"))

      
      '''
if __name__ == '__main__':
    unittest.main(verbosity=2)
    

