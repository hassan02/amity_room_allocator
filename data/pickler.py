import shelve
import string
import random
from model.living import Living
from model.office import Office
try:
   import cPickle as pickle
except:
   import pickle

id_list = shelve.open('persons_ids')
office_data = shelve.open('offices.pkl')

class Pickler(object):
    def save_office(self,office_name):
        if office_name.lower() not in office_data: 
            office = Office(office_name)
            d[office_name.lower()] = office
            print('Office %s created' % (office_name.upper()))
            office_data.close()
        else:
            raise Exception('Room name already exist')
        # Write to the stream 

    def load_offices(self):
        print('Loading All Offices...')
        for key in office_data:
            data = office_data[key]
            if data.members == {}:
                members_list = 'EMPTY'
            else:
                members_list = ", ".join(data(values))
        print ('%s-%d(OFFICE)\n%s' % (data.room_name.upper(),data.no_of_occupants, members_list))
        d.close()

    def add_fellow(first_name, last_name):
        fellow_name = Fellow(first_name,last_name).fullname
        fellow_id = get_valid_id
        picked_room = get_available_office()
        data = office_data[picked_room]
        data.members += fellow_name + '  '
        data.no_of_occupants +=  1
        office_data[picked_room] = data
        d.close()
    
    def get_available_office(self):
        available_offices = []
        for key in office_data:
            if office_data[key].no_of_occupants < 6:
                available_offices.append(key)
        if available_offices != []:
            avail_office = available_offices[random.randint(0,len(available_offices)-1)]
            return avail_office
        else:
            raise Exception('No available_offices')
        d.close()
    def generate_id(self,persons_type):
        if persons_type.upper() == 'FELLOW': 
            fellow_id = 'F' + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
            while fellow_id in fellow_id_list:
                fellow_id = 'F' + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
            else:
                fellow_id_list.append(fellow_id)
        else:
            

#    count = int(raw_input('Enter number of fellows to add'))
#    for i in range(count):
#      fname = raw_input('Enter first name: ')
#     lname = raw_input('Enter last name: ')
#      add_fellow(fname,lname)