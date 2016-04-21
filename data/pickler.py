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
living_data = shelve.open('living.pkl')
class Pickler(object):
    def save_office(self,office_name):
        if office_name.lower() not in office_data and office_name.lower() not in living_data: 
            office = Office(office_name)
            office_data[office_name.lower()] = office
            print('Office %s created' % (office_name.upper()))
        else:
            ErrorHandler().room_exist()

    def save_living(self,living_name):
        if living_name.lower() not in living_data and living_name.lower() not in office_data: 
            living = Living(living_name)
            living_data[living_name.lower()] = living
            print('Living Room %s created' % (living_name.upper()))
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
            print ('%s-%d(OFFICE)\n%s\n' % (data.room_name.upper(),data.no_of_occupants, members_list))

    def load_livings(self):
        print('Loading All Living Rooms...')
        for key in living_data:
            data = living_data[key]
            if data.members == {}:
                members_list = 'EMPTY'
            else:
                members_list = ", ".join(data.members.values())
            print ('%s-%d(LIVING)\n%s\n' % (data.room_name.upper(),data.no_of_occupants, members_list))
        
    def add_staff(self,first_name, last_name):
        staff_name = Staff(first_name,last_name).fullname
        staff_id = self.generate_id('STAFF')
        picked_room = self.get_available_office()
        data = office_data[picked_room]
        data.members[staff_id] = staff_name
        data.no_of_occupants +=  1
        office_data[picked_room] = data
        print('Staff %s with ID NO: %s added to %s' %(staff_name, staff_id, picked_room.upper()))

    def add_fellow(self, first_name, last_name):
        fellow_name = Fellow(first_name,last_name).fullname
        fellow_id = self.generate_id('FELLOW')
        picked_room = self.get_available_living()
        data = living_data[picked_room]
        data.members[fellow_id] = fellow_name
        data.no_of_occupants +=  1
        living_data[picked_room] = data
        print('Fellow %s with ID NO: %s added to %s' %(fellow_name, fellow_id, picked_room.upper()))


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

    def get_available_living(self):
        available_livings = []
        for key in living_data:
            if living_data[key].no_of_occupants < 4:
                available_livings.append(key)
        if available_livings != []:
            avail_living = available_livings[random.randint(0,len(available_livings)-1)]
            return avail_living
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

    def print_room(self,room_name):
        room_name = room_name.lower()
        if room_name in living_data:
            print('Loading %s members...' % (room_name.upper()))
            data = living_data[room_name]
            if data.members == {}:
                members_list = 'EMPTY'
            else:
                members_list = ", ".join(data.members.values())
            print ('%s-%d(LIVING)\n%s\n' % (data.room_name.upper(),data.no_of_occupants, members_list))
        elif room_name in office_data:
            print('Loading %s members...'% (room_name.upper()))
            data = office_data[room_name]
            if data.members == {}:
                members_list = 'EMPTY'
            else:
                members_list = ", ".join(data.members.values())
            print ('%s-%d(OFFICE)\n%s\n' % (data.room_name.upper(),data.no_of_occupants, members_list))
        else:
            print 'Room not exist'




#    count = int(raw_input('Enter number of fellows to add'))
#    for i in range(count):
#      fname = raw_input('Enter first name: ')
#     lname = raw_input('Enter last name: ')
#      add_fellow(fname,lname)