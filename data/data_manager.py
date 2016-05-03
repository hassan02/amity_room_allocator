import os
import random
import shelve
import string

from model.living import Living
from model.office import Office
from model.staff import Staff
from model.fellow import Fellow

    
class DataManager(object):
    displayline = '..............................................................................'
    def __init__(self, offices_file, livings_file, fellows_file, staffs_file):
        # Opens all shelve file
        self.office_data = shelve.open(offices_file)
        self.living_data = shelve.open(livings_file)
        self.fellow_data = shelve.open(fellows_file)
        self.staff_data = shelve.open(staffs_file)

    def save_room(self, room_name, room_type):
        # Save room into data based on room type
        if room_type.upper() == 'OFFICE':
            if room_name.lower() not in self.office_data and room_name.lower() not in self.living_data: 
                office = Office(room_name)
                self.office_data[room_name.lower()] = office
                print('Office %s created' % (room_name.upper()))
            else:
                print('Room %s already exist' % (room_name.upper()))
        elif room_type.upper() == 'LIVING':
            if room_name.lower() not in self.living_data and room_name.lower() not in self.office_data: 
                living = Living(room_name)
                self.living_data[room_name.lower()] = living
                print('Living Room %s created' % (room_name.upper()))     
            else:
                print('Room %s already exist' % (room_name.upper()))
        
    def load_all_rooms(self):
        # Load all offices from data
        office_output = 'Loading All Offices...\n'
        for office, office_info in self.office_data.items():
            members_list = ', '.join(office_info.members.values()) if office_info.members else 'EMPTY'
            office_info.no_of_occupants = len(office_info.members)
            office_output += ('%s(OFFICE) - %d of %d\n%s\n%s\n\n' % (office_info.name.upper(),office_info.no_of_occupants, office_info.max_occupants, self.displayline, members_list.upper()))
        print(office_output)

        # Load all living rooms from data
        living_output = 'Loading All Living Rooms...\n'
        for living, living_info in self.living_data.items():
            members_list = ", ".join(living_info.members.values()) if living_info.members else 'EMPTY'
            living_info.no_of_occupants = len(living_info.members)
            living_output += ('%s(LIVING) - %d of %d\n%s\n%s\n\n' % (living_info.name.upper(), living_info.no_of_occupants, living_info.max_occupants, self.displayline, members_list.upper()))
        print(living_output)
    
    def get_available_office(self):
        # Get all available offices
        available_offices = []
        if self.office_data != {}:
            for key in self.office_data:
                if self.office_data[key].no_of_occupants < self.office_data[key].max_occupants:
                    available_offices.append(key)
            if available_offices != []:
                avail_office = available_offices[random.randint(0,len(available_offices)-1)]
                return avail_office
            else:
                return None
        else:
            return None

    def get_available_living(self):
        # Get all available living spaces
        available_livings = []
        if self.living_data != {}:
            for key in self.living_data:
                if self.living_data[key].no_of_occupants < self.living_data[key].max_occupants:
                    available_livings.append(key)
            if available_livings != []:
                avail_living = available_livings[random.randint(0,len(available_livings)-1)]
                return avail_living
            else:
                return None
        else:
            return None

    def add_person(self, firstname, lastname, person_type, living_choice = 'N'):
        if not living_choice:
            living_choice = 'N'
        if person_type.upper() == 'STAFF' and (living_choice.upper() == 'Y' or living_choice == 'N'):
            picked_office = self.get_available_office()
            if picked_office != None:
                self.add_person_to_room(firstname,lastname, 'STAFF', picked_office)
            else:
                self.add_person_to_unallocated(firstname, lastname, 'STAFF')
        elif person_type.upper() == 'FELLOW' and living_choice.upper() == 'Y':
            picked_living = self.get_available_living() 
            if picked_living != None:
                self.add_person_to_room(firstname,lastname, 'FELLOW', picked_living)
            else:
                self.add_person_to_unallocated(firstname,lastname, 'FELLOW')
        elif person_type.upper() == 'FELLOW' and living_choice.upper() == 'N':
            self.add_person_to_unallocated(firstname,lastname, 'FELLOW')

        else:
            raise Exception('Unidentifiable format')


    def add_person_to_room(self,first_name, last_name, person_type, picked_room):
        #Save to room
        if person_type.upper() == 'STAFF':
            staff = Staff(first_name,last_name)  # Create a staff object
            office_info = self.office_data[picked_room]
            office_info.members[staff.id] = staff.fullname
            office_info.no_of_occupants = len(office_info.members)
            self.office_data[picked_room] = office_info

            #Save to staffs_data
            staff.allocated = True
            staff.room = picked_room
            self.staff_data[staff.id] = staff
            print('Staff %s with ID NO: %s added to %s' %(staff.fullname, staff.id, picked_room.upper()))
        
        elif person_type.upper() == 'FELLOW':
            fellow = Fellow(first_name,last_name)  # Create a Fellow object
            living_info = self.living_data[picked_room]
            living_info.members[fellow.id] = fellow.fullname
            living_info.no_of_occupants = len(living_info.members)
            self.living_data[picked_room] = living_info
            
            #Save to fellows_data
            fellow.allocated = True
            fellow.room = picked_room
            self.fellow_data[fellow.id] = fellow

            print('Fellow %s with ID NO: %s added to %s' %(fellow.fullname, fellow.id, picked_room.upper()))

    def add_person_to_unallocated(self, first_name, last_name, person_type):
        # Add person to list of allocated
        if person_type.upper() == 'STAFF':  # Check if person is staff
            staff = Staff(first_name,last_name)
            self.staff_data[staff.id] = staff
            print('Staff %s with ID NO: %s has been added to the system but unallocated.' %(staff.fullname, staff.id))
        elif person_type.upper() == 'FELLOW':  # Check if person is fellow
            fellow = Fellow(first_name,last_name)
            self.fellow_data[fellow.id] = fellow
            print('Fellow %s with ID NO: %s has been added to the system but unallocated.' %(fellow.fullname, fellow.id))

    def print_room(self,room_name):
        room_name = room_name.lower()
        if room_name in self.living_data:  # Print room members if room is a living room
            print('Loading %s (LIVING) members...' % (room_name.upper()))
            living_info = self.living_data[room_name]
            members_list = ", ".join(living_info.members.values()) if living_info.members else 'EMPTY'
            living_info.no_of_occupants = len(living_info.members)
            print('%s(LIVING) - %d of %d\n%s\n%s\n\n' % (living_info.name.upper(),living_info.no_of_occupants, living_info.max_occupants, self.displayline, members_list.upper()))

        elif room_name in self.office_data:  # Print room members if room is an office
            print('Loading %s (OFFICE) members...'% (room_name.upper()))
            office_info = self.office_data[room_name]
            members_list = ', '.join(office_info.members.values()) if office_info.members else 'EMPTY'
            office_info.no_of_occupants = len(office_info.members)
            print('%s(OFFICE) - %d of %d\n%s\n%s\n\n' % (office_info.name.upper(),office_info.no_of_occupants, office_info.max_occupants, self.displayline, members_list.upper()))
        
        else:
            raise Exception('Error. Room does not exist')  # Throw an exception    

    def get_person_room(self, person_id, person_type):
        if person_type.upper() == 'FELLOW':        
            for living, living_info in self.living_data.items():
                if person_id in living_info.members:
                    return living
                    break
        
        elif person_type.upper() == 'STAFF':
            for office, office_info in self.office_data.items():
                if person_id in office_info.members:
                    return office
                    break

    def get_person_name(self, person_id, person_type):
        if person_type.upper() == 'FELLOW':
            for living, living_info in self.living_data.items():
                if person_id in living_info.members:
                    return living_info.members[person_id]
                    break       

        elif person_type.upper() == 'STAFF':
            for office, office_info in self.office_data.items():
                if person_id in office_info.members:
                    return office_info.members[person_id]
                    break

    def reallocate_person(self, person_id, new_room_name):
        if person_id.startswith('F'):
            self.reallocate_fellow(person_id,new_room_name)
        elif person_id.startswith('S'):
            self.reallocate_staff(person_id, new_room_name)
        else:
            raise Exception('Person ID invalid. Must start with F or S')

    def reallocate_fellow(self, person_id, new_room_name):
        person_id = person_id.upper()
        fellow_room = self.get_person_room(person_id, 'fellow')
        fellow_name = self.get_person_name(person_id, 'fellow')
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
        person_id = person_id.upper()
        staff_room = self.get_person_room(person_id, 'staff')
        staff_name = self.get_person_name(person_id, 'staff')
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
    
    def load_people(self, filename):
    # Load people from file into data 
        if os.path.isfile(filename):  #Check if file exist
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
            raise Exception('Cannot locate file')  # Raise exception if file does not exist

    def print_unallocated(self):
        unallocated_list = ''
        print('Loading all unallocated people...')
        for staff, fellow_data in self.fellow_data.items():
            if str(fellow_data.allocated) == 'False':
                unallocated_list += fellow_data.fullname + ' (FELLOW)' + '\n'
        
        for staff, staff_data in self.staff_data.items():
            if str(staff_data.allocated) == 'False':
                unallocated_list += staff_data.fullname + ' (STAFF)' + '\n'
        
        print(unallocated_list)
        
    def close_file(self):
        self.office_data.close()
        self.living_data.close()
        self.fellow_data.close()
        self.staff_data.close()