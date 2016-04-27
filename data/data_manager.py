import random
import shelve
import string

from model.living import Living
from model.office import Office
from model.staff import Staff
from model.fellow import Fellow
from model.error_handler import ErrorHandler

    
class DataManager(object):
    displayline = '..............................................................................'
    def __init__(self, offices_data, livings_data, fellows_data, staffs_data):
        self.offices_data = offices_data
        self.livings_data = livings_data
        self.fellows_data = fellows_data
        self.staffs_data = staffs_data

    def open_file(self):
        self.office_data = shelve.open(self.offices_data)
        self.living_data = shelve.open(self.livings_data)
        self.fellow_data = shelve.open(self.fellows_data)
        self.staff_data = shelve.open(self.staffs_data)
        
    def save_office(self, office_name):
        self.open_file()
        if office_name.lower() not in self.office_data and office_name.lower() not in self.living_data: 
            office = Office(office_name)
            self.office_data[office_name.lower()] = office
            print('Office %s created' % (office_name.upper()))
            
        else:
            ErrorHandler().room_exist(office_name)
        
    def save_living(self, living_name):
        self.open_file()
        if living_name.lower() not in self.living_data and living_name.lower() not in self.office_data: 
            living = Living(living_name)
            self.living_data[living_name.lower()] = living
            print('Living Room %s created' % (living_name.upper()))
           
        else:
            ErrorHandler().room_exist(living_name)
        #self.office_data.close()
        #self.living_data.close()
        # Write to the stream 

    def load_offices(self):
        self.open_file()
        office_output = ''
        print('Loading All Offices...')
        for key in self.office_data:
            data = self.office_data[key]
            if data.members == {}:
                members_list = 'EMPTY'
            else:
                members_list = ", ".join(data.members.values())
            data.no_of_occupants = len(data.members)
            office_output += ('%s(OFFICE) - %d of %d\n%s\n%s%s\n\n' % (data.room_name.upper(),data.no_of_occupants, data.max_occupants, self.displayline,data.members.keys(), members_list.upper()))
        print(office_output)
        #self.office_data.close()

    def load_livings(self):
        self.open_file()
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
        #self.living_data.close()
    
    def get_available_office(self):
        self.open_file()
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
        self.open_file()
        available_livings = []
        if self.living_data != {}:
            for key in self.living_data:
                if self.living_data[key].no_of_occupants < self.living_data[key].max_occupants:
                    available_livings.append(key)
            if available_livings != []:
                avail_living = available_livings[random.randint(0,len(available_livings)-1)]
                return avail_living
                #self.living_data.close()
            else:
                ErrorHandler().no_available_room('living room')
        else:
            print 'No available room exist'

    def add_person(self, firstname, lastname, person_type, living_choice):
        self.open_file()
        if living_choice == None:
            living_choice = 'N'
        picked_office = self.get_available_office()
        picked_living = self.get_available_living()
        if person_type.upper() == 'STAFF' and (living_choice.upper() == 'Y' or living_choice == 'N'):
            if picked_office != None:
                self.add_staff_to_room(firstname,lastname,picked_office)
            else:
                self.add_staff_to_unallocated(firstname, lastname)
        elif person_type.upper() == 'FELLOW' and living_choice.upper() == 'Y':
            if picked_living != None:
                self.add_fellow_to_room(firstname,lastname,picked_living)
            else:
                self.add_fellow_to_unallocated(firstname,lastname)
        elif person_type.upper() == 'FELLOW' and living_choice.upper() == 'N':
            self.add_fellow_to_unallocated(firstname,lastname)

        else:
            print('Unidentifiable format')


    def add_staff_to_room(self,first_name, last_name, picked_office):
        self.open_file()
        #Save to room
        staff = Staff(first_name,last_name)

        data = self.office_data[picked_office]
        data.members[staff.id] = staff.fullname
        data.no_of_occupants = len(data.members)
        self.office_data[picked_office] = data

        #Save to staffs_data
        staff.allocated = True
        staff.room = picked_office
        self.staff_data[staff.id] = staff

        #self.office_data.close()
        print('Staff %s with ID NO: %s added to %s' %(staff.fullname, staff.id, picked_office.upper()))
    
    def add_staff_to_unallocated(self,first_name, last_name):
        self.open_file()
        staff = Staff(first_name,last_name)
        self.staff_data[staff.id] = staff

         #self.office_data.close()
        print('Fellow %s with ID NO: %s has been added to the system but unallocated.' %(staff.fullname, staff.id))


    def add_fellow_to_room(self, first_name, last_name, picked_living):
        self.open_file()
        fellow = Fellow(first_name,last_name)
        data = self.living_data[picked_living]
        data.members[fellow.id] = fellow.fullname
        data.no_of_occupants = len(data.members)
        self.living_data[picked_living] = data
        #self.living_data.close()
        fellow.allocated = True
        fellow.room = picked_living
        self.fellow_data[fellow.id] = fellow



        print('Fellow %s with ID NO: %s added to %s' %(fellow.fullname, fellow.id, picked_living.upper()))

    def add_fellow_to_unallocated(self, first_name, last_name):
        self.open_file()
        fellow = Fellow(first_name,last_name)
        self.fellow_data[fellow.id] = fellow
        #self.living_data.close()
        print('Fellow %s with ID NO: %s has been added to the system but unallocated.' %(fellow.fullname, fellow.id))


    def print_room(self,room_name):
        self.open_file()
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
            #self.living_data.close()
        elif room_name in self.office_data:
            print('Loading %s (OFFICE) members...'% (room_name.upper()))
            data = self.office_data[room_name]
            if data.members == {}:
                members_list = 'EMPTY'
            else:
                members_list = ", ".join(data.members.values())
            data.no_of_occupants = len(data.members)
            print('%s(OFFICE) - %d of %d\n%s\n%s\n\n' % (data.room_name.upper(),data.no_of_occupants, data.max_occupants, self.displayline, members_list.upper()))
            #self.office_data.close()
        else:
            ErrorHandler().room_not_exist(room_name)    

    def get_fellow_room(self, person_id):
        self.open_file()
        for key in self.living_data:
            data = self.living_data[key]
            if person_id in data.members:
                return key
                break
        #self.living_data.close()
    def get_fellow_name(self, person_id):
        self.open_file()
        for key in self.living_data:
            data = self.living_data[key]
            if person_id in data.members:
                return data.members[person_id]
                break       
        #self.living_data.close()
    def get_staff_room(self, person_id):
        self.open_file()
        for key in self.office_data:
            data = self.office_data[key]
            if person_id in data.members:
                return key
                break

    def get_staff_name(self, person_id):
        self.open_file()
        for key in self.office_data:
            data = self.office_data[key]
            if person_id in data.members:
                return data.members[person_id]
                break  

    def reallocate_person(self, person_id, new_room_name):
        self.open_file()
        if person_id.startswith('F'):
            self.reallocate_fellow(person_id,new_room_name)
        elif person_id.startswith('S'):
            self.reallocate_staff(person_id, new_room_name)
        else:
            print('Person ID invalid. Must start with F or S')

    def reallocate_fellow(self, person_id, new_room_name):
        self.open_file()
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
        #self.living_data.close()

    def reallocate_staff(self, person_id, new_room_name):
        self.open_file()
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
        #self.office_data.close()

    def clear_room(self, room_name):
        self.open_file()
        room_name = room_name.lower()
        if room_name in self.living_data:
            choice = raw_input('Are you sure you want to clear %s. Enter yes to continue or any other text to exit: '%(room_name.upper()))
            if choice.lower() == 'yes':
                data = self.living_data[room_name]
                data.members.clear()
                data.no_of_occupants = len(data.members)
                self.living_data[room_name] = data 
                print('Living room %s has been cleared'%(room_name.upper()))
        elif room_name in self.office_data:
            choice = raw_input('Are you sure you want to clear %s. Enter yes to continue or any other text to exit: '%(room_name.upper()))
            if choice.lower() == 'yes':
                data = self.office_data[room_name]
                data.members.clear()
                data.no_of_occupants = len(data.members)
                self.office_data[room_name] = data
                print('Office %s has been cleared'%(room_name.upper()))
        else:
            ErrorHandler().room_not_exist(room_name)  

    def remove_room(self, room_name):
        self.open_file()
        room_name = room_name.lower()
        if room_name in self.living_data:
            #choice = raw_input('Are you sure you want to remove %s. Enter yes to continue or any other text to exit: '%(room_name.upper()))
            #if choice.lower() == 'yes':
                del self.living_data[room_name]
                print('Living room %s has been removed'%(room_name.upper()))
                #self.living_data.close()
        elif room_name in self.office_data:
            #choice = raw_input('Are you sure you want to remove %s. Enter yes to continue or any other text to exit: '%(room_name.upper()))
            #if choice.lower() == 'yes':
                del self.office_data[room_name]
                print('Office %s has been removed'%(room_name.upper()))
                #self.office_data.close()
        else:
            ErrorHandler().room_not_exist(room_name)

    def load_people(self, filename):
        self.open_file()
        if path.isfile(filename):
            with open(filename,'r') as openfile:
                for line in openfile:
                    argument = " ".join(line.split()).strip()
                    strlength = len(argument.split(' '))
                    print(strlength)
                    if strlength >= 3 and strlength <= 4:
                        first_name = argument.split(' ')[0].strip()
                        last_name = argument.split(' ')[1].strip()
                        person_role = argument.split(' ')[2].strip()
                        if strlength == 4:
                            living_choice = argument.split(' ')[3].strip()
                        else:
                            living_choice = 'N'
                    self.add_person(first_name,last_name,person_role,living_choice)
        else:
            ErrorHandler().cannot_locate_file()

    def print_unallocated(self):
        unallocated_list = ''
        print('Loading all unallocated people...')
        self.open_file()
        for key in self.fellow_data:
            fellow_data = self.fellow_data[key]
            if fellow_data.allocated == False:
                unallocated_list += fellow_data.fullname + ' (FELLOW)' + '\n'
        
        for key in self.staff_data:
            staff_data = self.staff_data[key]
            if staff_data.allocated == False:
                unallocated_list += staff_data.fullname + ' (STAFF)' + '\n'
        
        print unallocated_list
        
    def close_file(self):
        self.office_data.close()
        self.living_data.close()
        self.fellow_data.close()
        self.staff_data.close()