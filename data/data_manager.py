import os
import random
import shelve
import string

from model.living import Living
from model.office import Office
from model.staff import Staff
from model.fellow import Fellow

    
class DataManager(object):
    
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
        
    def load_all_rooms(self, filename = ''):
        displayline = '..............................................................................'
        # Load all offices from data
        office_output = 'Loading All Offices...\n'
        for office, office_info in self.office_data.items():
            members_list = ', '.join(office_info.members.values()) if office_info.members else 'EMPTY'
            office_info.no_of_occupants = len(office_info.members)
            office_output += ('%s(OFFICE) - %d of %d\n%s\n%s\n\n' % (office_info.name.upper(),office_info.no_of_occupants, office_info.max_occupants, displayline, members_list.upper()))
        

        # Load all living rooms from data
        living_output = 'Loading All Living Rooms...\n'
        for living, living_info in self.living_data.items():
            members_list = ", ".join(living_info.members.values()) if living_info.members else 'EMPTY'
            living_info.no_of_occupants = len(living_info.members)
            living_output += ('%s(LIVING) - %d of %d\n%s\n%s\n\n' % (living_info.name.upper(), living_info.no_of_occupants, living_info.max_occupants, displayline, members_list.upper()))


        if filename:  # Check if file is specified
            if os.path.isfile(filename):  # Check if file exist
                openfile = open(filename,'w')
                openfile.write(office_output)
                openfile.write(living_output)
                print('Successfully output allocations to file')
            else:
                raise Exception('Cannot locate file')  # Cannot locate file
        else:  # If file is not specified
            print(office_output)
            print(living_output)

    def get_available_room(self, room_type):
        if room_type.upper() == 'LIVING' or room_type.upper() == 'OFFICE':
            rooms_data = self.living_data if room_type.upper() == 'LIVING' else self.office_data
        
            if rooms_data != {}:
                avail_rooms = [room for room, room_info in rooms_data.items() if room_info.no_of_occupants < room_info.max_occupants]        
                return avail_rooms[random.randint(0,len(avail_rooms)-1)] if avail_rooms else None
            else:
                return None
    
    def add_person(self, firstname, lastname, person_type, living_choice = 'N'):
        if not living_choice:
            living_choice = 'N'
        if person_type.upper() == 'STAFF' and (living_choice.upper() == 'Y' or living_choice.upper() == 'N'):
            picked_office = self.get_available_room('OFFICE')
            if picked_office != None:
                self.add_person_to_room(firstname,lastname, 'STAFF', picked_office)
            else:
                self.add_person_to_unallocated(firstname, lastname, 'STAFF')
        elif person_type.upper() == 'FELLOW' and living_choice.upper() == 'Y':
            picked_living = self.get_available_room('LIVING') 
            if picked_living != None:
                self.add_person_to_room(firstname,lastname, 'FELLOW', picked_living)
            else:
                self.add_person_to_unallocated(firstname,lastname, 'FELLOW')
        elif person_type.upper() == 'FELLOW' and living_choice.upper() == 'N':
            self.add_person_to_unallocated(firstname,lastname, 'FELLOW')

        else:
            raise Exception('Unidentifiable format')


    def add_person_to_room(self,first_name, last_name, person_type, picked_room):
        # Check for person_type Fellow or Staff
        if person_type.upper() == 'STAFF':
            room_info = self.office_data[picked_room]
            person = Staff(first_name, last_name)
        elif person_type.upper() == 'FELLOW':
            room_info = self.living_data[picked_room]
            person = Fellow(first_name, last_name)

        room_info.members[person.id] = person.fullname
        room_info.no_of_occupants = len(room_info.members)
        person.allocated = True  # Set allocated property as true
        person.room = picked_room  # Set person room as picked room

        if person_type.upper() == 'STAFF':
            self.office_data[picked_room] = room_info
            self.staff_data[person.id] = person
            print('Staff %s with ID NO: %s added to %s' %(person.fullname, person.id, picked_room.upper()))
        elif person_type.upper() == 'FELLOW':
            self.living_data[picked_room] = room_info
            self.fellow_data[person.id] = person
            print('Fellow %s with ID NO: %s added to %s' %(person.fullname, person.id, picked_room.upper()))
        
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
        displayline = '..............................................................................'
        room_name = room_name.lower()
        if room_name in self.living_data:  # Print room members if room is a living room
            print('Loading %s (LIVING) members...' % (room_name.upper()))
            living_info = self.living_data[room_name]
            members_list = ", ".join(living_info.members.values()) if living_info.members else 'EMPTY'
            living_info.no_of_occupants = len(living_info.members)
            print('%s(LIVING) - %d of %d\n%s\n%s\n\n' % (living_info.name.upper(),living_info.no_of_occupants, living_info.max_occupants, displayline, members_list.upper()))

        elif room_name in self.office_data:  # Print room members if room is an office
            print('Loading %s (OFFICE) members...'% (room_name.upper()))
            office_info = self.office_data[room_name]
            members_list = ', '.join(office_info.members.values()) if office_info.members else 'EMPTY'
            office_info.no_of_occupants = len(office_info.members)
            print('%s(OFFICE) - %d of %d\n%s\n%s\n\n' % (office_info.name.upper(),office_info.no_of_occupants, office_info.max_occupants, displayline, members_list.upper()))
        
        else:
            raise Exception('Error. Room does not exist')  # Throw an exception if room does not exist    

    def get_person_details(self, person_id):
        persons_data = self.fellow_data if person_id in self.fellow_data else self.staff_data
        return [persons_data[person_id].fullname, persons_data[person_id].room, persons_data[person_id].allocated] if person_id in persons_data else []

    def reallocate_person(self, person_id, new_room_name):
        person_id = person_id.upper()
        new_room_name = new_room_name.lower()
        if person_id in self.fellow_data or person_id in self.staff_data:
            rooms_data = self.living_data if person_id in self.fellow_data else self.office_data
            persons_data = self.fellow_data if person_id in self.fellow_data else self.staff_data
            person_details = self.get_person_details(person_id)
            person_name = person_details[0]
            person_room = person_details[1].lower()
            person_allocated = str(person_details[2])
            if person_allocated != 'False':
                if person_room != new_room_name:
                    if new_room_name in rooms_data:
                        room_info = rooms_data[new_room_name]
                        if room_info.no_of_occupants < room_info.max_occupants:
                            room_info.members[person_id] = person_name
                            room_info.no_of_occupants = len(room_info.members)
                            rooms_data[new_room_name] = room_info
                            person_info = persons_data[person_id]
                            person_info.room = new_room_name
                            persons_data[person_id] = person_info
                            former_room = rooms_data[person_room]
                            former_room.members.pop(person_id)
                            former_room.no_of_occupants = len(former_room.members)
                            rooms_data[person_room] = former_room
                            print('%s with ID: %s has been reallocated to %s' %(person_name, person_id, new_room_name.upper()))
                        else:
                            print('Room %s is full.' %(new_room_name.upper()))                
                    else:
                        print('Room %s does not exist as required space' % (new_room_name.upper()))
                else:
                    print('%s with ID: %s is already in %s' %(person_name, person_id, new_room_name.upper()))
            else:
                print('%s with ID: %s is not pre-allocated' %(person_name, person_id))
        else:
            raise Exception('Person ID invalid.')
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
                    self.add_person(first_name, last_name, person_role, living_choice)
        else:
            raise Exception('Cannot locate file')  # Raise exception if file does not exist

    def print_unallocated(self, filename):
        unallocated_list = 'Loading all unallocated people...\n'
        for fellow, fellow_data in self.fellow_data.items():
            if str(fellow_data.allocated) == 'False':
                unallocated_list += fellow_data.fullname + ' (FELLOW)' + '\n'
        
        for staff, staff_data in self.staff_data.items():
            if str(staff_data.allocated) == 'False':
                unallocated_list += staff_data.fullname + ' (STAFF)' + '\n'
        if filename:
            if os.path.isfile(filename):  #Check if file exist
                openfile = open(filename,'w')
                openfile.write(unallocated_list)
                print('Successfully output list of unallocated people to file')
            else:
                raise Exception('Cannot locate file')
        else:           
            print(unallocated_list)
    
    def print_people(self):
        all_persons = 'Loading all persons...\n'
        all_persons += 'ID NO\t\tFULL NAME\t\tPERSON-TYPE\tALLOCATED\tROOM NAME\n'
        all_persons += '.................................................................................\n'
        for fellow, fellow_data in self.fellow_data.items():
            all_persons +=  '%s\t%s\t\tFELLOW\t\t%s\t\t%s\n' % (fellow_data.id, fellow_data.fullname, str(fellow_data.allocated), fellow_data.room.upper())
        
        for staff, staff_data in self.staff_data.items():
            all_persons +=  '%s\t%s\t\tSTAFF\t\t%s\t\t%s\n' % (staff_data.id, staff_data.fullname, str(staff_data.allocated), staff_data.room.upper())
        
        print(all_persons)
       
    def close_file(self):
        self.office_data.close()
        self.living_data.close()
        self.fellow_data.close()
        self.staff_data.close()