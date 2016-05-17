from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
import os
import shelve
import unittest
import sqlite3

from model.amity_model import Amity
from model.office import Office
from model.living import Living
from cStringIO import StringIO  # or from StringIO ...


class TestAllocation(unittest.TestCase):
    """Test cases for Amity"""
    @classmethod
    def setUpClass(cls):
        if os.path.isfile(os.path.realpath(
                'tests/test_data_files/test_rooms.db')):
            os.remove(os.path.realpath("tests/test_data_files/test_rooms.db"))
        if os.path.isfile(os.path.realpath(
                'tests/test_data_files/test_persons.db')):
            os.remove(os.path.realpath(
                "tests/test_data_files/test_persons.db"))
    
    def setUp(self):
        self.held = sys.stdout
        sys.stdout = StringIO()
        self.test_rooms_file = 'tests/test_data_files/test_rooms'
        self.test_persons_file = 'tests/test_data_files/test_persons'
        self.rooms_data = shelve.open(self.test_rooms_file)
        self.persons_data = shelve.open(self.test_persons_file)
    
    def tearDown(self):
        self.rooms_data.close()
        self.persons_data.close()
        self.rooms_data = shelve.open(self.test_rooms_file)
        self.persons_data = shelve.open(self.test_persons_file)
        self.rooms_data.clear()
        self.persons_data.clear()
        self.rooms_data.close()
        self.persons_data.close()

        
    def test_add_fellow(self):
        Amity(self.test_rooms_file, self.test_persons_file).add_person('Samuel', 'Akintola', 'fellow')
        self.persons_data = shelve.open(self.test_persons_file)
        person_list = [
            person_info.fullname for person_id,
            person_info in self.persons_data.items()]
        self.assertTrue('SAMUEL AKINTOLA' in person_list)
    
    def test_add_staff(self):
        Amity(self.test_rooms_file, self.test_persons_file).add_person('Bolade', 'Alawode', 'staff')
        self.persons_data = shelve.open(self.test_persons_file)
        person_list = [
            person_info.fullname for person_id,
            person_info in self.persons_data.items()]
        self.assertTrue('BOLADE ALAWODE' in person_list)
    
    def test_print_people(self):
        Amity(self.test_rooms_file, self.test_persons_file).add_person('Samuel', 'Akintola', 'fellow')
        self.persons_data = shelve.open(self.test_persons_file)
        self.rooms_data = shelve.open(self.test_rooms_file)
        get_fellow_ids = [fellow_id for fellow_id, fellow_info in self.persons_data.items(
        ) if fellow_info.fullname.upper() == 'SAMUEL AKINTOLA']
        fellow_id = get_fellow_ids[0]
        self.persons_data.close()
        add_person_out = "FELLOW SAMUEL AKINTOLA with ID NO: %s "\
                         "has been added to the system but unallocated." % (fellow_id)
        all_persons = 'Loading all persons...\n'
        all_persons += 'ID NO\t\tFULL NAME\t\tPERSON-TYPE\tLIVING_ALLOCATED'\
                       '\tLIVING_SPACE\tOFFICE_ALLOCATED\tOFFICE_SPACE\n'
        all_persons += '............................................................'\
                       '.........................................................................\n'
        all_persons +=  '%s\tSAMUEL AKINTOLA\t\tFELLOW\t\tFalse\t\t\t\t\tFalse\t\t\t\n\n' \
                        % (fellow_id)
        
        Amity(self.test_rooms_file, self.test_persons_file).print_people()
        self.assertEqual(sys.stdout.getvalue(),'%s\n%s' % (add_person_out, all_persons))
    
    def test_create_office(self):
        Amity(self.test_rooms_file, self.test_persons_file).create_room('neptune', 'office')  # Create a sample office
        self.assertTrue('neptune' in self.rooms_data)
        self.assertTrue(type(self.rooms_data['neptune']), Office)
        self.assertEqual(1, len(self.rooms_data))
        self.assertEqual('neptune', self.rooms_data['neptune'].name.lower())
        self.assertEqual(self.rooms_data['neptune'].members, {})
        self.assertEqual(self.rooms_data['neptune'].max_occupants, 6)

    def test_create_living(self):
        Amity(self.test_rooms_file, self.test_persons_file).create_room('iroko', 'living')  # Create a sample office
        self.assertTrue('iroko' in self.rooms_data)
        self.assertTrue(type(self.rooms_data['iroko']), Office)
        self.assertEqual(1, len(self.rooms_data))
        self.assertEqual('iroko', self.rooms_data['iroko'].name.lower())
        self.assertEqual(self.rooms_data['iroko'].members, {})
        self.assertEqual(self.rooms_data['iroko'].max_occupants, 4)

    def test_create_room_wrong_type_raises_error(self):
        self.assertRaises(
            Exception,
            Amity(self.test_rooms_file, self.test_persons_file).create_room,
            'Cafeteria',
            'refresh')

    def test_create_living_with_invalid_name_raises_error(self):
        self.assertRaises(
            Exception,
            Amity(self.test_rooms_file, self.test_persons_file).create_room,
            ['Mahogany'],
            'living')

    def test_print_office_room(self):
        Amity(self.test_rooms_file, self.test_persons_file).create_room('saturn', 'office')
        Amity(self.test_rooms_file, self.test_persons_file).print_room('saturn')
        create_room_out = 'Room SATURN created as OFFICE'
        displayline = '.............................................'\
                      '.................................'
        expectedoutput = 'Loading SATURN (OFFICE) members...\nSATURN(OFFICE) - 0 of 6' \
                         '\n%s\nEMPTY\n\n\n' % (displayline)
        self.assertEqual(sys.stdout.getvalue(),
                         '%s\n%s'% (create_room_out, expectedoutput))

    def test_print_allocations(self):
        Amity(self.test_rooms_file, self.test_persons_file).create_room('mars', 'office')
        Amity(self.test_rooms_file, self.test_persons_file).print_allocations()
        create_room_out = 'Room MARS created as OFFICE'
        displayline = '.......................................'\
                      '.......................................'
        output = 'Loading All Rooms...\nMARS(OFFICE) - 0 of 6\n%s\nEMPTY\n\n\n' % (
            displayline)
        self.assertEqual(sys.stdout.getvalue(),
                         '%s\n%s' % (create_room_out, output))

    def test_load_people_with_invalid_file_raises_error(self):
        self.assertRaises(Exception, Amity(self.test_rooms_file, self.test_persons_file).load_people, 'no_file.txt')

     
    def test_print_room_to_invalid_file_raises_error(self):
        self.assertRaises(Exception, Amity(self.test_rooms_file, self.test_persons_file).print_room, 'no_room')

     
    def test_print_allocations_to_invalid_file_raises_error(self):
        self.assertRaises(
            Exception,
            Amity(self.test_rooms_file, self.test_persons_file).print_allocations,
            'no_file.txt')
       
    def test_load_people(self):
        Amity(self.test_rooms_file, self.test_persons_file).create_room('moon', 'office')
        Amity(self.test_rooms_file, self.test_persons_file).load_people("tests/test_data_files/test_input.txt")
        self.assertTrue('EBUN OMONI' in self.rooms_data['moon'].members.values())
    
    def test_reallocate_fellow(self):
        Amity(self.test_rooms_file, self.test_persons_file).create_room('mahogany', 'living')
        Amity(self.test_rooms_file, self.test_persons_file).add_person('Sunday', 'Nwuguru', 'fellow', 'y')
        self.persons_data = shelve.open(self.test_persons_file)
        get_fellow_ids = [fellow_id for fellow_id, fellow_info in self.persons_data.items(
        ) if fellow_info.fullname.upper() == 'SUNDAY NWUGURU']        
        fellow_id = get_fellow_ids[0]
        self.persons_data.close()
        Amity(self.test_rooms_file, self.test_persons_file).create_room('obeche', 'living')
        self.persons_data = shelve.open(self.test_persons_file)
        Amity(self.test_rooms_file, self.test_persons_file).reallocate_person(fellow_id, 'obeche')
        self.rooms_data = shelve.open(self.test_rooms_file)
        self.assertTrue(fellow_id in self.rooms_data['obeche'].members)
    
    def test_reallocate_with_invalid_id_raises_exception(self):
        self.assertRaises(
            Exception,
            Amity(self.test_rooms_file, self.test_persons_file).reallocate_person,
            'S3242444',
            'saturn')
    
    def test_print_people_allocations_to_output_file(self):
        Amity(self.test_rooms_file, self.test_persons_file).create_room('junniper', 'living')
        filename = 'tests/test_data_files/test_output.txt'
        displayline = '.......................................'\
                      '.......................................'
        expectedoutput = 'Loading All Rooms...\nJUNNIPER(LIVING) - 0 of 4\n%s\nEMPTY\n\n' % (displayline)
        Amity(self.test_rooms_file, self.test_persons_file).print_allocations(filename)
        with open(filename,'r') as openfile:
                self.assertEqual(expectedoutput,''.join(openfile.readlines()))
    
    def test_print_people_unallocated_to_output_file(self):
        Amity(self.test_rooms_file, self.test_persons_file).add_person('Hassan', 'Oyeboade', 'fellow')
        filename = 'tests/test_data_files/test_unallocated.txt'
        Amity(self.test_rooms_file, self.test_persons_file).print_unallocated(filename)
        expectedoutput = 'Loading all unallocated people...\nHASSAN OYEBOADE (FELLOW)\n'
        with open(filename,'r') as openfile:
                self.assertEqual(expectedoutput,''.join(openfile.readlines()))
    
    
if __name__ == '__main__':
    unittest.main()
