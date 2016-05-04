import os,sys

import shelve
import unittest
import sqlite3

from model.amity_model import Amity
from model.office import Office
from model.living import Living
from cStringIO import StringIO # or from StringIO ...

class TestAllocation(unittest.TestCase):
    
    @classmethod
    def setUpClass(TestAllocation):
      if os.path.isfile(os.path.realpath('tests/test_data_files/test_persons_ids.db')):
        os.remove(os.path.realpath('tests/test_data_files/test_persons_ids.db'))
      if os.path.isfile(os.path.realpath('tests/test_data_files/test_offices.db')):
        os.remove(os.path.realpath('tests/test_data_files/test_offices.db'))
      if os.path.isfile(os.path.realpath('tests/test_data_files/test_living.db')):
        os.remove(os.path.realpath("tests/test_data_files/test_living.db"))
      if os.path.isfile(os.path.realpath('tests/test_data_files/test_fellows.db')):
        os.remove(os.path.realpath("tests/test_data_files/test_fellows.db"))
      if os.path.isfile(os.path.realpath('tests/test_data_files/test_staff.db')):
        os.remove(os.path.realpath("tests/test_data_files/test_staff.db"))
    
    def setUp(self):
      self.held = sys.stdout
      sys.stdout = StringIO()
      self.test_office_file = 'tests/test_data_files/test_offices'
      self.test_living_file = 'tests/test_data_files/test_living'
      self.test_fellow_file = 'tests/test_data_files/test_fellows'
      self.test_staff_file = 'tests/test_data_files/test_staff'
      
      self.amity = Amity(self.test_office_file, self.test_living_file, self.test_fellow_file, self.test_staff_file)
      
      self.office_data = shelve.open(self.test_office_file)
      self.living_data = shelve.open(self.test_living_file)
      self.fellow_data = shelve.open(self.test_fellow_file)
      self.staff_data = shelve.open(self.test_staff_file)
    
    @classmethod
    def tearDownClass(TestCreateRoom):
      pass

      
    def tearDown(self):
      self.office_data.close()
      self.living_data.close()
      self.fellow_data.close()
      self.staff_data.close()

    def test_00_add_fellow_raises_error_no_room(self):
      self.amity.add_person('Bolade','Alawode','staff')

    def test_01_add_staff_raises_error_no_room(self):
      self.amity.add_person('Samuel','Akintola','fellow','y')

    def test_01_get_fellow_id(self):
        ids = [fellow_id for fellow_id, fellow_info in self.fellow_data.items() if fellow_info.fullname.upper() == 'SAMUEL AKINTOLA']
        return ids[0]

    def test_01_get_staff_id(self):
        ids = [staff_id for staff_id, staff_info in self.staff_data.items() if staff_info.fullname.upper() == 'BOLADE ALAWODE']
        return ids[0]
    
    def test_01_test_print_people(self):
        fellow_id = self.test_01_get_fellow_id()
        staff_id = self.test_01_get_staff_id()
        all_persons = 'Loading all persons...\n'
        all_persons += 'ID NO\t\tFULL NAME\t\tPERSON-TYPE\tALLOCATED\tROOM NAME\n'
        all_persons += '.................................................................................\n'
        all_persons +=  '%s\tSAMUEL AKINTOLA\t\tFELLOW\t\tFalse\t\t\n' % (fellow_id)
        all_persons +=  '%s\tBOLADE ALAWODE\t\tSTAFF\t\tFalse\t\t\n\n' % (staff_id)
        self.amity.print_people()
        self.assertEqual(sys.stdout.getvalue(), all_persons)
       
    def test_02_office_saved_in_data(self):
      self.amity.create_room('neptune','office')  # Create a sample office
    def test_03_test_office_saved_in_data(self):
      self.assertTrue('neptune' in self.office_data)

    def test_04_office_object_created(self):
      self.assertTrue(type(self.office_data['neptune']), Office)
    
    def test_05_office_creation(self):
      self.assertEqual(1,len(self.office_data))
    
    def test_06_office_name(self):
      self.assertEqual('neptune',self.office_data['neptune'].name.lower())

    def test_07_office_members_is_empty(self):
      self.assertEqual(self.office_data['neptune'].members,{})
    
    def test_08_office_no_of_occupants(self):
      self.assertEqual(self.office_data['neptune'].no_of_occupants, 0)

    def test_09_office_max_occupants(self):
      self.assertEqual(self.office_data['neptune'].max_occupants, 6)

    def test_10_create_office_raises_error(self):
      self.assertRaises(Exception, self.amity.create_room, [2,4,5],'office')

    def test_11_create_room_wrong_type_raises_error(self):
      self.assertRaises(Exception, self.amity.create_room, 'Cafeteria','refresh')

    def test_12_print_office_room(self):
      self.amity.print_room('neptune')
      displayline = '..............................................................................'
      self.assertEqual(sys.stdout.getvalue(), 'Loading NEPTUNE (OFFICE) members...\nNEPTUNE(OFFICE) - 0 of 6\n%s\nEMPTY\n\n\n'%(displayline))

    def test_13_living_creation(self):
      self.amity.create_room('iroko','living')
      self.assertEqual(1,len(self.living_data))
      
    def test_14_living_saved_in_data(self):
      self.amity.create_room('iroko','living')  # Create a sample office
      self.assertTrue('iroko' in self.living_data)

    def test_15_created_living_object(self):
      self.assertEqual(type(self.living_data['iroko']), Living)
    
    def test_16_living_creation(self):
      self.assertEqual(1,len(self.living_data))
    
    def test_17_living_name(self):
      self.assertEqual('iroko', self.living_data['iroko'].name.lower())

    def test_18_living_members_is_empty(self):
      self.assertEqual(self.living_data['iroko'].members, {})
    
    def test_19_living_no_of_occupants(self):
      self.assertEqual(self.living_data['iroko'].no_of_occupants, 0)

    def test_20_living_max_occupants(self):
      self.assertEqual(self.living_data['iroko'].max_occupants, 4)

    def test_21_create_living_wrong_type_raises_error(self):
      self.assertRaises(Exception, self.amity.create_room, ['Mahogany'],'living')

    def test_22_print_living_room(self):
      self.amity.print_room('iroko')
      displayline = '..............................................................................'
      self.assertEqual(sys.stdout.getvalue(), 'Loading IROKO (LIVING) members...\nIROKO(LIVING) - 0 of 4\n%s\nEMPTY\n\n\n'%(displayline))

    def test_23_print_all_room(self):
      self.amity.print_allocations()
      displayline = '..............................................................................'
      output = 'Loading All Offices...\nNEPTUNE(OFFICE) - 0 of 6\n%s\nEMPTY\n\n\n'%(displayline)
      output += 'Loading All Living Rooms...\nIROKO(LIVING) - 0 of 4\n%s\nEMPTY\n\n\n'%(displayline)
      self.assertEqual(sys.stdout.getvalue(), output)

    def test_24_reallocate_wrong_id_raises_error(self):
      self.assertRaises(Exception, self.amity.reallocate_person, 'ABDCQ','iroko')

    def test_25_add_fellow(self):
      self.amity.add_person('Adeola','Adedoyin','fellow','y')
    
    def test_26_allocate_fellow(self):
      self.amity.print_room('iroko')
      displayline = '..............................................................................'
      self.assertEqual(sys.stdout.getvalue(), 'Loading IROKO (LIVING) members...\nIROKO(LIVING) - 1 of 4\n%s\nADEOLA ADEDOYIN\n\n\n'%(displayline))

    def test_27_unallocated(self):
      self.amity.add_person('Adedoyin', 'Israel', 'fellow')      
      
    def test_28_print_unallocated(self):
      self.amity.print_unallocated()
      expectedoutput = 'Loading all unallocated people...\nADEDOYIN ISRAEL (FELLOW)\nBOLADE ALAWODE (STAFF)'
      expectedoutput += '\nSAMUEL AKINTOLA (FELLOW)\n\n'
      self.assertEqual(''.join(sorted(sys.stdout.getvalue())), ''.join(sorted(expectedoutput)))

    def test_29_add_staff(self):
      self.amity.add_person('Bukola','Makinwa','staff')
    
    def test_30_allocate_staff(self):
      self.amity.print_room('neptune')
      displayline = '..............................................................................'
      self.assertEqual(sys.stdout.getvalue(), 'Loading NEPTUNE (OFFICE) members...\nNEPTUNE(OFFICE) - 1 of 6\n%s\nBUKOLA MAKINWA\n\n\n'%(displayline))
    
    def test_31_allocate_another_staff(self):
      self.amity.add_person('Ikem','Okonkwo','staff')
    
    def test_32_allocate_another_staff(self):
      self.amity.add_person('Temilade','Ojuade','staff')
    
    def test_33_allocate_another_staff(self):
      self.amity.add_person('Nadayar','Engesi','staff')
    
    def test_34_allocate_another_staff(self):
      self.amity.add_person('Godson','Ukpere','staff')
    
    def test_35_allocate_another_staff(self):
      self.amity.add_person('Sayo','Alagbe','staff')
    
    def test_36_allocate_another_staff(self):
      self.amity.add_person('Derin','Otegbola','staff')
    
    def test_37_allocate_another_staff(self):
      self.amity.print_unallocated()
      expectedoutput = 'Loading all unallocated people...\nADEDOYIN ISRAEL (FELLOW)\nBOLADE ALAWODE (STAFF)'
      expectedoutput += '\nSAMUEL AKINTOLA (FELLOW)\nDERIN OTEGBOLA (STAFF)\n\n'
      self.assertEqual(''.join(sorted(sys.stdout.getvalue())), ''.join(sorted(expectedoutput)))
    
    def test_38_allocate_another_fellow(self):
      self.amity.add_person('Sunday','Nwuguru','fellow','y')
    
    def test_39_allocate_another_fellow(self):
      self.amity.add_person('Chukwuerika','Dike','fellow','y')
    
    def test_40_allocate_another_fellow(self):
      self.amity.add_person('Stephen','Oduntan','fellow','y')
    
    def test_41_allocate_another_fellow(self):
      self.amity.add_person('Lovelyn','Tijesunimi-Israel','fellow','y')
    
    def test_42_allocate_another_fellow(self):
      self.amity.print_unallocated()
    
    def test_43_allocate_person_raises_error(self):
      self.assertRaises(Exception, self.amity.add_person, 'Adeolu','Akinade','office')
        
    def test_44_create_new_office(self):
      self.amity.create_room('saturn','office')

    def test_45_add_new_staff(self):
      self.amity.add_person('Seni', 'Sulaimon', 'staff')

    def test_46_get_valid_staff_id(self):
      ids = [staff_id for staff_id, staff_info in self.staff_data.items() if staff_info.fullname.upper() == 'SENI SULAIMON']
      return ids[0]

    def test_47_test_reallocate_to_full_room(self):
      staff_id = self.test_46_get_valid_staff_id()
      self.amity.reallocate_person(staff_id, 'neptune')
      self.assertEqual(sys.stdout.getvalue(), 'Room NEPTUNE is full.\n')

    def test_48_test_reallocate_to_non_exiting_office(self):
      staff_id = self.test_46_get_valid_staff_id()
      self.amity.reallocate_person(staff_id, 'bombay')
      self.assertEqual(sys.stdout.getvalue(), 'Room BOMBAY does not exist as required space\n')

    def test_49_get_valid_staff_id(self):
      ids = [staff_id for staff_id, staff_info in self.staff_data.items() if staff_info.fullname.upper() == 'SAYO ALAGBE']
      return ids[0]
    
    def test_50_reallocate_staff(self):
      staff_id = self.test_49_get_valid_staff_id()
      self.amity.reallocate_person(staff_id, 'saturn')
      
    def test_51_test_reallocate_staff(self):
      staff_id = self.test_49_get_valid_staff_id()
      self.assertTrue(staff_id in self.office_data['saturn'].members)

    def test_52_test_reallocate_invalid_staff_id(self):
        self.assertRaises(Exception, self.amity.reallocate_person, 'S3242444', 'saturn' )
    
    def test_53_create_new_living(self):
        self.amity.create_room('cedar','living')

    def test_54_add_new_fellow(self):
        self.amity.add_person('Chiemeka','Alim','fellow','y')

    def test_55_get_valid_fellow_id(self):
        ids = [fellow_id for fellow_id, fellow_info in self.fellow_data.items() if fellow_info.fullname.upper() == 'CHIEMEKA ALIM']
        return ids[0]

    def test_56_test_reallocate_fellow_to_full_room(self):
        fellow_id = self.test_55_get_valid_fellow_id()
        self.amity.reallocate_person(fellow_id, 'iroko')
        self.assertEqual(sys.stdout.getvalue(), 'Room IROKO is full.\n')

    def test_57_test_reallocate_to_non_existing_living(self):
        fellow_id = self.test_55_get_valid_fellow_id()
        self.amity.reallocate_person(fellow_id, 'ojuelegba')
        self.assertEqual(sys.stdout.getvalue(), 'Room OJUELEGBA does not exist as required space\n')

    def test_58_test_reallocate_invalid_fellow_id(self):
        self.assertRaises(Exception, self.amity.reallocate_person, 'F32432232', 'iroko' )
    
    def test_59_get_valid_fellow_id(self):
        ids = [fellow_id for fellow_id, fellow_info in self.fellow_data.items() if fellow_info.fullname.upper() == 'CHUKWUERIKA DIKE']
        return ids[0]

    def test_60_test_reallocate_fellow_to_same_room(self):
        fellow_id = self.test_59_get_valid_fellow_id()
        self.amity.reallocate_person(fellow_id, 'iroko')
        self.assertEqual(sys.stdout.getvalue(), 'CHUKWUERIKA DIKE with ID: %s is already in IROKO\n' %(fellow_id))

    def test_62_get_valid_fellow_id(self):
      ids = [fellow_id for fellow_id, fellow_info in self.fellow_data.items() if fellow_info.fullname.upper() == 'SUNDAY NWUGURU']
      return ids[0]

    def test_64_reallocate_fellow(self):
      fellow_id = self.test_62_get_valid_fellow_id()
      self.amity.reallocate_person(fellow_id, 'cedar')
      
    def test_65_reallocate_person(self):
      fellow_id = self.test_62_get_valid_fellow_id()
      self.assertTrue(fellow_id in self.living_data['cedar'].members)

    def test_66_load_people(self):
      self.amity.load_people("tests/test_data_files/test_input.txt")
      self.assertTrue('EBUN OMONI' in self.office_data['neptune'].members.values() or 'EBUN OMONI' in self.office_data['saturn'].members.values())

    def test_67_load_people(self):
      self.amity.load_people("tests/test_data_files/test_input.txt")
      self.assertTrue('MAYOWA FALADE' in self.living_data['iroko'].members.values() or 'MAYOWA FALADE' in self.living_data['cedar'].members.values())

    def test_68_load_people_raises_error(self):
      self.assertRaises(Exception, self.amity.load_people, 'no_file.txt')
    
    def test_69_print_room_raises_error(self):
      self.assertRaises(Exception, self.amity.print_room, 'no_room')

    def test_70_load_rooms_raises_error(self):
      self.assertRaises(Exception, self.amity.print_allocations, 'no_file.txt')

if __name__ == '__main__':
    unittest.main()
    

