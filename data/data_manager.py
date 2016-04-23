from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from model.living import Living
from model.office import Office
from model.staff import Staff
from model.fellow import Fellow
from model.error_handler import ErrorHandler

import shelve
import string
import random
try:
   import cPickle as pickle
except:
   import pickle



    
class DataManager(object):

    def __init__(self, id_list = 'persons_ids', office_data = 'offices', living_data = 'living'):
        self.id_list = shelve.open(id_list)
        self.office_data = shelve.open(office_data)
        self.living_data = shelve.open(living_data)
        self.displayline = '..............................................................................'

    def save_office(self,office_name):
        if office_name.lower() not in self.office_data and office_name.lower() not in self.living_data: 
            office = Office(office_name)
            self.office_data[office_name.lower()] = office
            print('Office %s created' % (office_name.upper()))
            
        else:
            ErrorHandler().room_exist(office_name)
        self.office_data.close()
        self.living_data.close()

    def save_living(self,living_name):
        if living_name.lower() not in self.living_data and living_name.lower() not in self.office_data: 
            living = Living(living_name)
            self.living_data[living_name.lower()] = living
            print('Living Room %s created' % (living_name.upper()))
           
        else:
            ErrorHandler().room_exist(living_name)
        self.office_data.close()
        self.living_data.close()
        # Write to the stream 

    def load_offices(self):
        office_output = ''
        print('Loading All Offices...')
        for key in self.office_data:
            data = self.office_data[key]
            if data.members == {}:
                members_list = 'EMPTY'
            else:
                members_list = ", ".join(data.members.values())
            data.no_of_occupants = len(data.members)
            office_output += ('%s(OFFICE) - %d of %d\n%s\n%s\n\n' % (data.room_name.upper(),data.no_of_occupants, data.max_occupants, self.displayline, members_list.upper()))
        print(office_output)
        self.office_data.close()
    def load_livings(self):
        living_output = ''
        print('Loading All Living Rooms...')
        for key in self.living_data:
            data = self.living_data[key]
            if data.members == {}:
                members_list = 'EMPTY'
            else:
                members_list = ", ".join(data.members.values())
            data.no_of_occupants = len(data.members)
            living_output += ('%s(LIVING) - %d of %d\n%s\n%s\n\n' % (data.room_name.upper(),data.no_of_occupants, data.max_occupants, self.displayline, members_list.upper()))
        print(living_output)
        self.living_data.close()
    
    def get_available_office(self):
        available_offices = []
        if self.office_data != {}:
            for key in self.office_data:
                if self.office_data[key].no_of_occupants < self.office_data[key].max_occupants:
                    available_offices.append(key)
            if available_offices != []:
                avail_office = available_offices[random.randint(0,len(available_offices)-1)]
                return avail_office
                self.office_data.close()
            else:
                ErrorHandler().no_available_room('office')
        else:
            print 'No available office exist'

    def get_available_living(self):
        available_livings = []
        if self.living_data != {}:
            for key in self.living_data:
                if self.living_data[key].no_of_occupants < self.living_data[key].max_occupants:
                    available_livings.append(key)
            if available_livings != []:
                avail_living = available_livings[random.randint(0,len(available_livings)-1)]
                return avail_living
                self.living_data.close()
            else:
                ErrorHandler().no_available_room('living room')
        else:
            print 'No available room exist'

    def add_staff(self,first_name, last_name):
        if self.get_available_office() != None:
            picked_room = self.get_available_office()
            staff_name = Staff(first_name,last_name).fullname.upper()
            staff_id = self.generate_id('STAFF')
            data = self.office_data[picked_room]
            data.members[staff_id] = staff_name
            data.no_of_occupants = len(data.members)
            self.office_data[picked_room] = data
            self.office_data.close()
            print('Staff %s with ID NO: %s added to %s' %(staff_name, staff_id, picked_room.upper()))

    def add_fellow(self, first_name, last_name):
        if self.get_available_living() != None:
            picked_room = self.get_available_living()
            fellow_name = Fellow(first_name,last_name).fullname.upper()
            fellow_id = self.generate_id('FELLOW')
            data = self.living_data[picked_room]
            data.members[fellow_id] = fellow_name
            data.no_of_occupants = len(data.members)
            self.living_data[picked_room] = data
            self.living_data.close()
            print('Fellow %s with ID NO: %s added to %s' %(fellow_name, fellow_id, picked_room.upper()))


    
    def generate_id(self,persons_type):
        if 'all_ids' not in self.id_list:
            self.id_list['all_ids'] = []
        person_id_list = self.id_list['all_ids']
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
        self.id_list.close()

    def print_room(self,room_name):
        room_name = room_name.lower()
        if room_name in self.living_data:
            print('Loading %s (LIVING) members...' % (room_name.upper()))
            data = self.living_data[room_name]
            if data.members == {}:
                members_list = 'EMPTY'
            else:
                members_list = ", ".join(data.members.values())
            data.no_of_occupants = len(data.members)
            print('%s(LIVING) - %d of %d\n%s\n%s\n\n' % (data.room_name.upper(),data.no_of_occupants, data.max_occupants, self.displayline, members_list.upper()))
            self.living_data.close()
        elif room_name in self.office_data:
            print('Loading %s (OFFICE) members...'% (room_name.upper()))
            data = self.office_data[room_name]
            if data.members == {}:
                members_list = 'EMPTY'
            else:
                members_list = ", ".join(data.members.values())
            data.no_of_occupants = len(data.members)
            print('%s(OFFICE) - %d of %d\n%s\n%s\n\n' % (data.room_name.upper(),data.no_of_occupants, data.max_occupants, self.displayline, members_list.upper()))
            self.office_data.close()
        else:
            ErrorHandler().room_not_exist(room_name)    

    def get_fellow_room(self, person_id):
        for key in self.living_data:
            data = self.living_data[key]
            if person_id in data.members:
                return key
                break
        self.living_data.close()
    def get_fellow_name(self, person_id):
        for key in self.living_data:
            data = self.living_data[key]
            if person_id in data.members:
                return data.members[person_id]
                break       
        self.living_data.close()
    def get_staff_room(self, person_id):
        for key in self.office_data:
            data = self.office_data[key]
            if person_id in data.members:
                return key
                break

    def get_staff_name(self, person_id):
        for key in self.office_data:
            data = self.office_data[key]
            if person_id in data.members:
                return data.members[person_id]
                break  

    def reallocate_person(self, person_id, new_room_name):
        if person_id.startswith('F'):
            self.reallocate_fellow(person_id,new_room_name)
        elif person_id.startswith('S'):
            self.reallocate_staff(person_id, new_room_name)
        else:
            print('Person ID invalid. Must start with F or S')

    def reallocate_fellow(self, person_id, new_room_name):
        person_id = person_id.upper()
        fellow_room = self.get_fellow_room(person_id)
        fellow_name = self.get_fellow_name(person_id)
        new_room_name = new_room_name.lower()
        if fellow_room != new_room_name:
            if fellow_room != None and fellow_name != None:
                if new_room_name in self.living_data:
                    data = self.living_data[new_room_name]
                    if data.no_of_occupants < data.max_occupants:
                        data.members[person_id] = fellow_name
                        data.no_of_occupants = len(data.members)
                        self.living_data[new_room_name] = data
                        fellow_data = self.living_data[fellow_room]
                        fellow_data.members.pop(person_id)
                        fellow_data.no_of_occupants = len(fellow_data.members)
                        self.living_data[fellow_room] = fellow_data
                        print('%s with ID: %s has been reallocated to %s' %(fellow_name, person_id, new_room_name.upper()))
                    else:
                        print('Room %s is full.' %(new_room_name.upper()))                
                else:
                    print('Room %s do not exist does not exist as Living space' % (new_room_name.upper()))
            else:
                print('Fellow ID: %s does not exist'% (person_id))
        else:
            print('FELLOW %s with ID: %s is already in %s (LIVING)' %(fellow_name, person_id, new_room_name.upper()))
        self.living_data.close()
    def reallocate_staff(self, person_id, new_room_name):
        person_id = person_id.upper()
        staff_room = self.get_staff_room(person_id)
        staff_name = self.get_staff_name(person_id)
        new_room_name = new_room_name.lower()
        if staff_room != new_room_name:
            if staff_room != None and staff_name != None:
                if new_room_name in self.office_data:
                    data = self.office_data[new_room_name]
                    if data.no_of_occupants < data.max_occupants:
                        data.members[person_id] = staff_name
                        data.no_of_occupants = len(data.members)
                        self.office_data[new_room_name] = data
                        staff_data = self.office_data[staff_room]
                        staff_data.members.pop(person_id)
                        staff_data.no_of_occupants = len(staff_data.members)
                        self.office_data[staff_room] = staff_data
                        print('STAFF %s with ID: %s has been reallocated to %s (OFFICE)' %(staff_name, person_id, new_room_name.upper()))
                    else:
                        print('Room %s is full.' %(new_room_name.upper()))                
                else:
                    print('Room %s do not exist as Office' %(new_room_name.upper()))
            else:
                print('Staff ID: %s does not exist'% (person_id))
        else:
            print('STAFF %s with ID: %s is already in %s' %(staff_name, person_id, new_room_name.upper()))
        self.office_data.close()

    def clear_room(self, room_name):
        room_name = room_name.lower()
        if room_name in self.living_data:
            data = self.living_data[room_name]
            data.members.clear()
            data.no_of_occupants = len(data.members)
            self.living_data[room_name] = data 
            print('Living room %s has been cleared'%(room_name.upper()))
        elif room_name in self.office_data:
            data = self.office_data[room_name]
            data.members.clear()
            data.no_of_occupants = len(data.members)
            self.office_data[room_name] = data
            print('Office %s has been cleared'%(room_name.upper()))
        else:
            ErrorHandler().room_not_exist(room_name)  

    def remove_room(self, room_name):
        room_name = room_name.lower()
        if room_name in self.living_data:
            del self.living_data[room_name]
            print('Living room %s has been removed'%(room_name.upper()))
            self.living_data.close()
        elif room_name in self.office_data:
            del self.office_data[room_name]
            print('Office %s has been removed'%(room_name.upper()))
            self.office_data.close()
        else:
            ErrorHandler().room_not_exist(room_name)


        #new_room_name = new_room_name.lower()
        #if new_room_name in living_data:
        #    data = 


#    count = int(raw_input('Enter number of fellows to add'))
#    for i in range(count):
#      fname = raw_input('Enter first name: ')
#     lname = raw_input('Enter last name: ')
#      add_fellow(fname,lname)