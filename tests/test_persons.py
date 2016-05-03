from model.person import Person
from model.fellow import Fellow
from model.staff import Staff
import unittest

class TestPerson(unittest.TestCase):
    person = Person('Adeola','Adedire')
    def test_new_person_class(self):
        self.assertEqual(type(self.person), Person)
    def test_new_person_first_name(self):
        self.assertEqual(self.person.fullname, 'ADEOLA ADEDIRE')
    def test_new_person_allocated(self):
        self.assertEqual(self.person.allocated, 'False')
    def test_new_person_room(self):
        self.assertEqual(self.person.room, '')
    def test_create_new_person_raises_error(self):
        self.assertRaises(Exception, Person, 9, 'Ade')


class TestFellow(TestPerson):
    fellow = Fellow('Lovelyn','Tijesunimi-Israel')
    def test_new_fellow_class(self):        
        self.assertEqual(type(self.fellow), Fellow)
    def test_new_fellow_full_name(self):
        self.assertEqual(self.fellow.fullname, 'LOVELYN TIJESUNIMI-ISRAEL')
    def test_new_fellow_id(self):
        self.assertTrue(self.fellow.id.startswith('F'))
    def test_new_fellow_id_length(self):
        self.assertEqual(len(self.fellow.id), 11)
    def test_new_fellow_allocated(self):
        self.assertEqual(self.fellow.allocated, 'False')
    def test_new_fellow_room(self):
        self.assertEqual(self.fellow.room, '')
    def test_create_new_fellow_raises_error(self):
        self.assertRaises(Exception, Fellow, [3,4], 'Ade')


class TestStaff(TestPerson):
    staff = Staff('Ikem','Okonkwo')
    def test_new_staff_class(self):        
        self.assertEqual(type(self.staff), Staff)
    def test_new_staff_full_name(self):
        self.assertEqual(self.staff.fullname, 'IKEM OKONKWO')
    def test_new_staff_id(self):
        self.assertTrue(self.staff.id.startswith('S'))
    def test_new_staff_id_length(self):
        self.assertEqual(len(self.staff.id), 11)
    def test_new_staff_allocated(self):
        self.assertEqual(self.staff.allocated, 'False')
    def test_new_staff_room(self):
        self.assertEqual(self.staff.room, '')
    def test_create_new_staffs_raises_error(self):
        self.assertRaises(Exception, Staff, {'A':'Apple'}, 4.5677)



if __name__ == '__main__':
    unittest.main()