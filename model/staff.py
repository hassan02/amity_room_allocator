import random
import shelve
import string

from person import Person 

class Staff(Person):
    """ This class creates a new staff and inherits from Person class"""

    persons_data = shelve.open('data_files/persons')
    def __init__(self, first_name, last_name):
        """initializes a new staff & inherit from the super class Person"""
        super(Staff, self).__init__(first_name,last_name)
        self.person_type = 'staff'
        self.id = self.get_staff_id()

    def get_staff_id(self):
        """returns staff id by generating random string"""
        staff_id = 'S' + ''.join(random.choice(string.ascii_uppercase + string.digits) \
                                 for _ in range(10))
        while staff_id in self.persons_data:
            staff_id = 'S' + ''.join(random.choice(string.ascii_uppercase + string.digits) \
                                     for _ in range(10))
        else:
            return staff_id
        self.persons_data.close()