import string
import random
import shelve
from person import Person 
class Fellow(Person):
    id_list = shelve.open('data_files/person_ids')
    def __init__(self, first_name, last_name):
        super(Fellow, self).__init__(first_name,last_name)
        self.id = self.get_fellow_id()
    def get_fellow_id(self):
        if 'all_ids' not in self.id_list:
            self.id_list['all_ids'] = []
        person_id_list = self.id_list['all_ids']
        fellow_id = 'F' + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        while fellow_id in person_id_list:
            fellow_id = 'F' + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        else:
            person_id_list.append(fellow_id)
        return fellow_id
        

#print simon.getName()
#print type(simon)