'''
from model.person import Person
from model.fellow import Fellow
from model.staff import Staff
from model.room import Room
from model.office import Office
from model.living import Living
from model.amity_model import Amity

import shelve
import unittest
from cStringIO import StringIO # or from StringIO ...
import sys

class TestAllocation(unittest.TestCase):
    def setUp(self):
        self.held, sys.stdout = sys.stdout, StringIO()
        self.test_id_list = 'tests/test_data_files/test_persons_ids'
        self.test_office_data = 'tests/test_data_files/test_offices'
        self.test_living_data = 'tests/test_data_files/test_living'
        #self.clear_files()
        self.amity = Amity(self.test_office_data, self.test_living_data)
      
        self.office_file = shelve.open(self.test_office_data)
        self.living_file = shelve.open(self.test_living_data)
    #def test_if_person_allocated_raises_error(self):
        #self.assertRaises(Exception, self.amity.add_person, 'Adeola', 'Adedoyin', 'fellow', 'yes')

    #def test_if_person_is_allocated(self):
    #    self.amity.add_person('Adeola', 'Adedoyin', 'fellow', 'y')
    #    self.assertEqual(1, len(self.living_file.members))
if __name__ == '__main__':
    unittest.main()
'''