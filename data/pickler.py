import shelve
import string
import random
from model.living import Living
from model.office import Office
from model.staff import Staff
from model.fellow import Fellow
from model.error_handler import ErrorHandler
try:
   import cPickle as pickle
except:
   import pickle

id_list = shelve.open('persons_ids')
office_data = shelve.open('offices.pkl')
living_data = shelve.open('offices.pkl')
class Pickler(object):
    def save_office(self,office_name):
        if office_name.lower() not in office_data: 
            office = Office(office_name)
            office_data[office_name.lower()] = office
            print('Office %s created' % (office_name.upper()))
        else:
            ErrorHandler().room_exist()
        # Write to the stream 

    def load_offices(self):
        print('Loading All Offices...')
        for key in office_data:
            data = office_data[key]
            if data.members == {}:
                members_list = 'EMPTY'
            else:
                members_list = ", ".join(data.members.values())
            print ('%s-%d(OFFICE)\n%s' % (data.room_name.upper(),data.no_of_occupants, members_list))
        
    def add_staff(self,first_name, last_name):
        staff_name = Staff(first_name,last_name).fullname
        staff_id = self.generate_id('STAFF')
        picked_room = self.get_available_office()
        data = office_data[picked_room]
        data.members[staff_id] = staff_name
        data.no_of_occupants +=  1
        office_data[picked_room] = data
        print('Staff %s with ID NO: %s added to %s' %(staff_name, staff_id, picked_room.upper()))
    
    def get_available_office(self):
        available_offices = []
        for key in office_data:
            if office_data[key].no_of_occupants < 6:
                available_offices.append(key)
        if available_offices != []:
            avail_office = available_offices[random.randint(0,len(available_offices)-1)]
            return avail_office
        else:
            ErrorHandler().no_available_room()
        
    def generate_id(self,persons_type):
        person_id_list = id_list['all_ids']
        if persons_type.upper() == 'FELLOW': 
            fellow_id = 'F' + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
            while fellow_id in person_id_list:
                fellow_id = 'F' + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
            else:
                person_id_list.append(fellow_id)
                return fellow_id
        elif persons_type.upper() == 'STAFF':
            staff_id = 'S' + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
            while staff_id in person_id_list:
                staff_id = 'S' + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
            else:
                person_id_list.append(staff_id) 
                return staff_id



#    count = int(raw_input('Enter number of fellows to add'))
#    for i in range(count):
#      fname = raw_input('Enter first name: ')
#     lname = raw_input('Enter last name: ')
#      add_fellow(fname,lname)