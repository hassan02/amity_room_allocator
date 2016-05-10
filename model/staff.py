import shelve
import random
import string
from person import Person 
class Staff(Person):
    id_list = shelve.open('data_files/person_ids')
    def __init__(self, first_name, last_name):
        super(Staff, self).__init__(first_name,last_name)
        self.id = self.get_staff_id()
    def get_staff_id(self):
        if 'all_ids' not in self.id_list:
            self.id_list['all_ids'] = []
        person_id_list = self.id_list['all_ids']
        staff_id = 'S' + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        while staff_id in person_id_list:
            staff_id = 'S' + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        else:
            person_id_list.append(staff_id)
        return staff_id
        self.id_list.close()