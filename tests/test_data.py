from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import os

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
        if os.path.isfile(os.path.realpath('tests/test_data_files/test_rooms.db')):
          os.remove(os.path.realpath("tests/test_data_files/test_rooms.db"))
        if os.path.isfile(os.path.realpath('tests/test_data_files/test_persons.db')):
          os.remove(os.path.realpath("tests/test_data_files/test_persons.db"))
      
    def setUp(self):
        self.held = sys.stdout
        sys.stdout = StringIO()
        self.test_rooms_file = 'tests/test_data_files/test_rooms'
        self.test_persons_file = 'tests/test_data_files/test_persons'
        self.amity = Amity(self.test_rooms_file, self.test_persons_file)
        self.rooms_data = shelve.open(self.test_rooms_file)
        self.persons_data = shelve.open(self.test_persons_file)
    
    @classmethod
    def tearDownClass(TestCreateRoom):
        pass

      
    def tearDown(self):
        self.rooms_data.close()
        self.persons_data.close()
      
    def test_01_add_fellow_raises_error_no_room(self):
        self.amity.add_person('Bolade','Alawode','staff')

    def test_02_add_staff_raises_error_no_room(self):
        self.amity.add_person('Samuel','Akintola','fellow','y')

    def test_03_get_fellow_id(self):
        ids = [fellow_id for fellow_id, fellow_info in self.persons_data.items() \
            if fellow_info.fullname.upper() == 'SAMUEL AKINTOLA']
        return ids[0]

    def test_04_get_staff_id(self):
        ids = [staff_id for staff_id, staff_info in self.persons_data.items()\
            if staff_info.fullname.upper() == 'BOLADE ALAWODE']
        return ids[0]
    
    def test_05_test_print_people(self):
        fellow_id = self.test_03_get_fellow_id()
        staff_id = self.test_04_get_staff_id()
        all_persons = 'Loading all persons...\n'
        all_persons += 'ID NO\t\tFULL NAME\t\tPERSON-TYPE\tLIVING_ALLOCATED'\
                       '\tLIVING_SPACE\tOFFICE_ALLOCATED\tOFFICE_SPACE\n'
        all_persons += '............................................................'\
                       '.........................................................................\n'
        all_persons +=  '%s\tSAMUEL AKINTOLA\t\tFELLOW\t\tFalse\t\t\t\t\tFalse\t\t\t\n' \
                        % (fellow_id)
        all_persons +=  '%s\tBOLADE ALAWODE\t\tSTAFF\t\tFalse\t\t\t\t\tFalse\t\t\t\n\n'\
                        % (staff_id)
        self.amity.print_people()
        self.assertEqual(''.join(sorted(sys.stdout.getvalue())),\
                         ''.join(sorted(all_persons)))
       
    def test_06_office_saved_in_data(self):
        self.amity.create_room('neptune','office')  # Create a sample office
    
    def test_07_test_office_saved_in_data(self):
        self.assertTrue('neptune' in self.rooms_data)

    def test_08_office_object_created(self):
        self.assertTrue(type(self.rooms_data['neptune']), Office)
    
    def test_09_office_creation(self):
        self.assertEqual(1,len(self.rooms_data))
    
    def test_10_office_name(self):
        self.assertEqual('neptune',self.rooms_data['neptune'].name.lower())

    def test_11_office_members_is_empty(self):
        self.assertEqual(self.rooms_data['neptune'].members,{})
    
    def test_12_office_no_of_occupants(self):
        self.assertEqual(self.rooms_data['neptune'].no_of_occupants, 0)

    def test_13_office_max_occupants(self):
        self.assertEqual(self.rooms_data['neptune'].max_occupants, 6)

    def test_14_create_office_raises_error(self):
        self.assertRaises(Exception, self.amity.create_room, [2,4,5],'office')

    def test_15_create_room_wrong_type_raises_error(self):
        self.assertRaises(Exception, self.amity.create_room, 'Cafeteria','refresh')

    def test_16_print_office_room(self):
        self.amity.print_room('neptune')
        displayline = '.............................................'\
                      '.................................'
        expectedoutput = 'Loading NEPTUNE (OFFICE) members...\nNEPTUNE(OFFICE) - 0 of 6' \
                         '\n%s\nEMPTY\n\n\n'%(displayline)
        self.assertEqual(''.join(sorted(sys.stdout.getvalue())), \
                         ''.join(sorted(expectedoutput)))

    def test_17_living_creation(self):
        self.amity.create_room('iroko', 'living')
        self.assertEqual(2,len(self.rooms_data))
      
    def test_18_living_saved_in_data(self):
        self.amity.create_room('iroko','living')  # Create a sample office
        self.assertTrue('iroko' in self.rooms_data)

    def test_19_created_living_object(self):
        self.assertEqual(type(self.rooms_data['iroko']), Living)
    
    def test_20_living_name(self):
        self.assertEqual('iroko', self.rooms_data['iroko'].name.lower())

    def test_21_living_members_is_empty(self):
        self.assertEqual(self.rooms_data['iroko'].members, {})   
    
    def test_22_living_no_of_occupants(self):
        self.assertEqual(self.rooms_data['iroko'].no_of_occupants, 0)

    def test_23_living_max_occupants(self):
        self.assertEqual(self.rooms_data['iroko'].max_occupants, 4)

    def test_24_create_living_wrong_type_raises_error(self):
        self.assertRaises(Exception, self.amity.create_room, ['Mahogany'],'living')

    def test_25_print_living_room(self):
        self.amity.print_room('iroko')
        displayline = '..............................................'\
                      '................................'
        self.assertEqual(sys.stdout.getvalue(), 'Loading IROKO (LIVING) members...'\
            '\nIROKO(LIVING) - 0 of 4\n%s\nEMPTY\n\n\n'%(displayline))

    def test_26_print_all_room(self):
        self.amity.print_allocations()
        displayline = '.......................................'\
                      '.......................................'
        output = 'Loading All Rooms...\nNEPTUNE(OFFICE) - 0 of 6\n%s\nEMPTY\n\n'%(displayline)
        output += '\nIROKO(LIVING) - 0 of 4\n%s\nEMPTY\n\n'%(displayline)
        self.assertEqual(''.join(sorted(sys.stdout.getvalue())),\
                         ''.join(sorted(output)))

    def test_27_reallocate_wrong_id_raises_error(self):
        self.assertRaises(Exception, self.amity.reallocate_person, 'ABDCQ','iroko')

    def test_28_add_fellow(self):
        self.amity.add_person('Adeola','Adedoyin','fellow','y')
    
    def test_29_allocate_fellow(self):
        self.amity.print_room('iroko')
        displayline = '................................................'\
                      '..............................'
        expectedoutput = 'Loading IROKO (LIVING) members...'\
                        '\nIROKO(LIVING) - 1 of 4\n%s\nADEOLA ADEDOYIN\n\n\n'%(displayline)
        self.assertEqual(sys.stdout.getvalue(), expectedoutput)

    def test_30_unallocated(self):
        self.amity.add_person('Adedoyin', 'Israel', 'fellow')      
      
    def test_31_print_unallocated(self):
        self.amity.print_unallocated()
        expectedoutput = 'Loading all unallocated people...\nADEDOYIN ISRAEL ' \
                          '(FELLOW)\nBOLADE ALAWODE (STAFF)\nSAMUEL AKINTOLA ' \
                          '(FELLOW)\nADEOLA ADEDOYIN (FELLOW)\n\n'
        self.assertEqual(''.join(sorted(sys.stdout.getvalue())), \
                         ''.join(sorted(expectedoutput)))

    def test_32_add_staff(self):
        self.amity.add_person('Bukola','Makinwa','staff')
    
    def test_33_allocate_staff(self):
        self.amity.print_room('neptune')
        displayline = '.........................................'\
                     '.....................................'
        expectedoutput = 'Loading NEPTUNE (OFFICE) members...\nNEPTUNE(OFFICE) - 3 of 6'\
                        '\n%s\nBUKOLA MAKINWA, ADEOLA ADEDOYIN, ADEDOYIN ISRAEL\n\n\n'%(displayline)
        self.assertEqual(''.join(sorted(sys.stdout.getvalue())), \
                         ''.join(sorted(expectedoutput)))
      
    def test_34_allocate_another_staff(self):
        self.amity.add_person('Ikem','Okonkwo','staff')
    
    def test_35_allocate_another_staff(self):
        self.amity.add_person('Temilade','Ojuade','staff')
    
    def test_36_allocate_another_staff(self):
        self.amity.add_person('Nadayar','Engesi','staff')
    
    def test_39_allocate_another_staff(self):
        self.amity.add_person('Derin','Otegbola','staff')
    
    def test_40_allocate_another_staff(self):
        self.amity.print_unallocated()
        expectedoutput = 'Loading all unallocated people...\nADEOLA ADEDOYIN (FELLOW)\n'
        expectedoutput += 'ADEDOYIN ISRAEL (FELLOW)\nBOLADE ALAWODE (STAFF)'
        expectedoutput += '\nSAMUEL AKINTOLA (FELLOW)\nDERIN OTEGBOLA (STAFF)\n\n'
        self.assertEqual(''.join(sorted(sys.stdout.getvalue())),\
                         ''.join(sorted(expectedoutput)))
    
    def test_41_allocate_another_fellow(self):
        self.amity.add_person('Sunday','Nwuguru','fellow','y')
    
    def test_42_allocate_another_fellow(self):
        self.amity.add_person('Chukwuerika','Dike','fellow','y')
    
    def test_43_allocate_another_fellow(self):
        self.amity.add_person('Stephen','Oduntan','fellow','y')
    
    def test_44_allocate_another_fellow(self):
        self.amity.add_person('Lovelyn','Tijesunimi-Israel','fellow','y')
    
    def test_45_allocate_another_fellow(self):
        self.amity.print_unallocated()
    
    def test_46_allocate_person_raises_error(self):
        self.assertRaises(Exception, self.amity.add_person,'Adeolu','Akinade','office')
        
    def test_47_create_new_office(self):
        self.amity.create_room('saturn','office')

    def test_48_add_new_staff(self):
        self.amity.add_person('Seni', 'Sulaimon', 'staff')

    def test_49_get_valid_staff_id(self):
        ids = [staff_id for staff_id, staff_info in self.persons_data.items() \
            if staff_info.fullname.upper() == 'SENI SULAIMON']
        return ids[0]

    def test_50_test_reallocate_to_full_room(self):
        staff_id = self.test_49_get_valid_staff_id()
        self.amity.reallocate_person(staff_id, 'neptune')
        self.assertEqual(sys.stdout.getvalue(), 'Room NEPTUNE is full.\n')

    def test_51_test_reallocate_to_non_exiting_office(self):
        staff_id = self.test_49_get_valid_staff_id()
        self.amity.reallocate_person(staff_id, 'bombay')
        self.assertEqual(sys.stdout.getvalue(), \
            'Room BOMBAY does not exist as required space\n')

    def test_52_get_valid_staff_id(self):
        ids = [staff_id for staff_id, staff_info in self.persons_data.items() \
              if staff_info.fullname.upper() == 'IKEM OKONKWO']
        return ids[0]
      
    def test_53_reallocate_staff(self):
        staff_id = self.test_52_get_valid_staff_id()
        self.amity.reallocate_person(staff_id, 'saturn')
        
    def test_54_test_reallocate_staff(self):
        staff_id = self.test_52_get_valid_staff_id()
        self.assertTrue(staff_id in self.rooms_data['saturn'].members)

    def test_55_test_reallocate_invalid_staff_id(self):
        self.assertRaises(Exception, self.amity.reallocate_person, 'S3242444', 'saturn')
    
    def test_56_create_new_living(self):
        self.amity.create_room('cedar','living')

    def test_57_add_new_fellow(self):
        self.amity.add_person('Chiemeka','Alim','fellow','y')

    def test_58_get_valid_fellow_id(self):
        ids = [fellow_id for fellow_id, fellow_info in self.persons_data.items() \
            if fellow_info.fullname.upper() == 'CHIEMEKA ALIM']
        return ids[0]

    def test_59_test_reallocate_fellow_to_full_room(self):
        fellow_id = self.test_58_get_valid_fellow_id()
        self.amity.reallocate_person(fellow_id, 'iroko')
        self.assertEqual(sys.stdout.getvalue(), 'Room IROKO is full.\n')

    def test_60_test_reallocate_to_non_existing_living(self):
        fellow_id = self.test_58_get_valid_fellow_id()
        self.amity.reallocate_person(fellow_id, 'ojuelegba')
        self.assertEqual(sys.stdout.getvalue(), \
            'Room OJUELEGBA does not exist as required space\n')

    def test_61_test_reallocate_invalid_fellow_id(self):
        self.assertRaises(Exception, self.amity.reallocate_person, 'F32432232', 'iroko' )
    
    def test_62_get_valid_fellow_id(self):
        ids = [fellow_id for fellow_id, fellow_info in self.persons_data.items() \
            if fellow_info.fullname.upper() == 'CHUKWUERIKA DIKE']
        return ids[0]

    def test_64_get_valid_fellow_id(self):
        ids = [fellow_id for fellow_id, fellow_info in self.persons_data.items() \
            if fellow_info.fullname.upper() == 'SUNDAY NWUGURU']
        return ids[0]

    def test_65_reallocate_fellow(self):
        fellow_id = self.test_62_get_valid_fellow_id()
        self.amity.reallocate_person(fellow_id, 'cedar')
        
    def test_66_reallocate_person(self):
        fellow_id = self.test_62_get_valid_fellow_id()
        self.assertTrue(fellow_id in self.rooms_data['cedar'].members)

    def test_67_load_people(self):
        self.amity.load_people("tests/test_data_files/test_input.txt")
        self.assertTrue('EBUN OMONI' in self.rooms_data['neptune'].members.values() \
            or 'EBUN OMONI' in self.rooms_data['saturn'].members.values())

    def test_68_load_people(self):
        self.amity.load_people("tests/test_data_files/test_input.txt")
        self.assertTrue('MAYOWA FALADE' in self.rooms_data['iroko'].members.values()\
            or 'MAYOWA FALADE' in self.rooms_data['cedar'].members.values())

    def test_69_load_people_raises_error(self):
        self.assertRaises(Exception, self.amity.load_people, 'no_file.txt')
    
    def test_70_print_room_raises_error(self):
        self.assertRaises(Exception, self.amity.print_room, 'no_room')

    def test_71_load_rooms_raises_error(self):
        self.assertRaises(Exception, self.amity.print_allocations, 'no_file.txt')

if __name__ == '__main__':
    unittest.main()
    

