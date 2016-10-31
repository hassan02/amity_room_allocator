import string
import random
import shelve

from person import Person


class Fellow(Person):
    """ This class creates a new fellow and inherits from Person class"""

    persons_data = shelve.open('data/data_files/persons')

    def __init__(self, first_name, last_name):
        """Initializes a new fellow by inheriting init properties from the super class Person"""
        super(Fellow, self).__init__(first_name, last_name)
        self.person_type = 'fellow'
        self.id = self.get_fellow_id()

    def get_fellow_id(self):
        """Returns fellow id by generating random string"""
        fellow_id = 'F' + ''.join(random.choice(string.ascii_uppercase + string.digits)
                                  for _ in range(10))
        while fellow_id in self.persons_data:
            fellow_id = 'F' + \
                ''.join(random.choice(string.ascii_uppercase + string.digits)
                        for _ in range(10))
        else:
            return fellow_id
        self.persons_data.close()
