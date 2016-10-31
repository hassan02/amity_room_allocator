from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
import os
import random
import shelve
import string

from model.fellow import Fellow
from model.living import Living
from model.office import Office
from model.staff import Staff


class DataManager(object):
    """This class manage saving to and loading from shelve files"""

    def __init__(self, rooms_data, persons_data):
        """Initializes class and gets the files"""
        # Opens all shelve file
        self.rooms_data = rooms_data
        self.persons_data = persons_data

    def save_room(self, room_name, room_type):
        """Save rooms to files"""
        # Save room into data based on room type
        if room_name.lower() not in self.rooms_data:
            room = Office(room_name) if room_type.upper(
            ) == 'OFFICE' else Living(room_name)
            self.rooms_data[room_name.lower()] = room
            print('Room %s created as %s' %
                  (room_name.upper(), room_type.upper()))
        else:
            print('Room %s already exist' % (room_name.upper()))

    def load_all_rooms(self, filename=''):
        """Load all rooms and print or save to file"""
        displayline = '..............................................................................'
        # Load all offices from data
        output = 'Loading All Rooms...\n'
        for room, room_info in self.rooms_data.items():
            members_list = ', '.join(room_info.members.values()) \
                           if room_info.members else 'EMPTY'
            room_info.no_of_occupants = len(room_info.members)
            output += ('%s(%s) - %d of %d\n%s\n%s\n\n' % (room_info.name.upper(),
                                                          room_info.room_type.upper(), room_info.no_of_occupants,
                                                          room_info.max_occupants, displayline, members_list.upper()))

        # Write to file if specified
        if filename:  # Check if file is specified
            if os.path.isfile(filename):  # Check if file exist
                openfile = open(filename, 'w')
                openfile.write(output)
                print('Successfully output allocations to file')
            else:
                raise Exception('Cannot locate file')  # Cannot locate file
        else:  # If file is not specified
            print(output)

    def get_available_room(self, room_type):
        """Get available office or living space"""
        # Get available office or living space
        if self.rooms_data != {}:
            avail_rooms = [room for room, room_info in self.rooms_data.items()
                           if (room_info.room_type.upper() == room_type.upper())
                           and (room_info.no_of_occupants < room_info.max_occupants)]
            return avail_rooms[random.randint(0, len(avail_rooms) - 1)] if avail_rooms else None
        else:
            return None

    def add_person(self, firstname, lastname, person_type, living_choice='N'):
        """Add a person to the system"""
        if not living_choice:
            living_choice = 'N'
        if person_type.upper() == 'STAFF' and \
           (living_choice.upper() == 'Y' or living_choice.upper() == 'N'):
            person = Staff(firstname, lastname)
            picked_office = self.get_available_room('OFFICE')
            self.add_person_to_room(person, picked_office) \
                if picked_office != None else \
                self.add_person_to_unallocated(person)
        elif person_type.upper() == 'FELLOW' and living_choice.upper() == 'Y':
            person = Fellow(firstname, lastname)
            picked_living = self.get_available_room('LIVING')
            if picked_living != None:
                person = self.add_person_to_room(person, picked_living)
            else:
                self.add_person_to_unallocated(person)

            picked_office = self.get_available_room('OFFICE')
            self.add_person_to_room(person, picked_office) \
                if picked_office != None else \
                self.add_person_to_unallocated(person)
        elif person_type.upper() == 'FELLOW' and living_choice.upper() == 'N':
            person = Fellow(firstname, lastname)
            picked_office = self.get_available_room('OFFICE')
            self.add_person_to_room(person, picked_office) \
                if picked_office != None else \
                self.add_person_to_unallocated(person)

        else:
            raise Exception('Unidentifiable format')

    def add_person_to_room(self, person, picked_room):
        """Add person to a particular room"""
        # Check for person_type Fellow or Staff
        room_info = self.rooms_data[picked_room]
        room_info.members[person.id] = person.fullname
        room_info.no_of_occupants = len(room_info.members)

        if self.rooms_data[picked_room].room_type.upper() == 'LIVING':
            person.living_allocated = True
            person.living = picked_room
        else:
            person.office = picked_room
            person.office_allocated = True
        self.rooms_data[picked_room] = room_info
        self.persons_data[person.id] = person
        print('%s %s with ID NO: %s added to %s (%s)' % (person.person_type.upper(),
                                                         person.fullname, person.id, picked_room.upper(),
                                                         self.rooms_data[picked_room].room_type.upper()))
        return person

    def add_person_to_unallocated(self, person):
        """add person to unallocated based on choice or room unavailability"""
        # Add person to list of unallocated
        self.persons_data[person.id] = person
        # return person
        print('%s %s with ID NO: %s has been added to the system but unallocated.'
              % (person.person_type.upper(), person.fullname, person.id))

    def print_room(self, room_name):
        """Print members of a room"""
        displayline = '..............................................................................'
        room_name = room_name.lower()

        if room_name in self.rooms_data:  # Print room members if room exist
            room_info = self.rooms_data[room_name]
            members_list = ", ".join(
                room_info.members.values()) if room_info.members else 'EMPTY'
            room_info.no_of_occupants = len(room_info.members)
            print('Loading %s (%s) members...' %
                  (room_name.upper(), room_info.room_type.upper()))
            print('%s(%s) - %d of %d\n%s\n%s\n\n' % (room_info.name.upper(),
                                                     room_info.room_type.upper(), room_info.no_of_occupants, room_info.max_occupants,
                                                     displayline, members_list.upper()))
        else:
            # Throw an exception if room does not exist
            raise Exception('Error. Room does not exist')

    def get_person_details(self, person_id):
        """Get person details"""
        return [self.persons_data[person_id].fullname,
                self.persons_data[person_id].office_allocated, self.persons_data[
                    person_id].office,
                self.persons_data[person_id].living_allocated, self.persons_data[person_id].living] \
            if person_id in self.persons_data else []

    def reallocate_person(self, person_id, new_room_name):
        """Reallocate a person to another room"""
        person_details = self.get_person_details(person_id)
        person_id = person_id.upper()
        new_room_name = new_room_name.lower()
        if person_details:
            if (person_details[2] != new_room_name) and \
               (person_details[4] != new_room_name):
                if new_room_name in self.rooms_data:
                    room_type = self.rooms_data[
                        new_room_name].room_type.upper()
                    person_allocated = str(person_details[1]).lower() \
                        if room_type == 'OFFICE' else str(person_details[3]).lower()
                    person_room = person_details[2] if room_type == 'OFFICE' \
                        else person_details[4]
                    if person_allocated != 'false':
                        room_info = self.rooms_data[new_room_name]
                        if room_info.no_of_occupants < room_info.max_occupants:
                            room_info.members[person_id] = person_details[0]
                            room_info.no_of_occupants = len(room_info.members)
                            self.rooms_data[new_room_name] = room_info
                            person_info = self.persons_data[person_id]
                            if room_type == 'OFFICE':
                                person_info.office = new_room_name
                            else:
                                person_info.living = new_room_name
                            self.persons_data[person_id] = person_info
                            former_room = self.rooms_data[person_room]
                            former_room.members.pop(person_id)
                            former_room.no_of_occupants = len(
                                former_room.members)
                            self.rooms_data[person_room] = former_room
                            print('%s with ID: %s has been reallocated to %s' % (
                                person_details[0], person_id, new_room_name.upper()))
                        else:
                            print('Room %s is full.' % (new_room_name.upper()))
                    else:
                        print('%s with ID: %s is not pre-allocated' %
                              (person_details[0], person_id))
                else:
                    print('Room %s does not exist as required space' %
                          (new_room_name.upper()))
            else:
                print('%s with ID: %s is already in %s' %
                      (person_details[0], person_id, new_room_name.upper()))
        else:
            raise Exception(
                'Person ID invalid. Run print_people to print all IDs')

    def load_people(self, filename):
        """Load people from a file and add them to the system"""
    # Load people from file into data
        if os.path.isfile(filename):  # Check if file exist
            with open(filename, 'r') as openfile:
                for line in openfile:
                    argument = " ".join(line.split()).strip()
                    strlength = len(argument.split(' '))
                    if strlength >= 3 and strlength <= 4:
                        first_name = argument.split(' ')[0].strip()
                        last_name = argument.split(' ')[1].strip()
                        person_role = argument.split(' ')[2].strip()
                        living_choice = argument.split(
                            ' ')[3].strip() if strlength == 4 else 'N'
                    self.add_person(first_name, last_name,
                                    person_role, living_choice)
        else:
            # Raise exception if file does not exist
            raise Exception('Cannot locate file')

    def print_unallocated(self, filename):
        """Print unallocated people"""
        unallocated_list = 'Loading all unallocated people...\n'
        for person, person_info in self.persons_data.items():
            if (str(person_info.office_allocated) or str(person_info.living_allocated) == 'False')\
                    and person_info.person_type.upper() == 'FELLOW':
                unallocated_list += person_info.fullname + ' (FELLOW)' + '\n'

            if person_info.person_type.upper() == 'STAFF' and str(person_info.office_allocated) == 'False':
                unallocated_list += person_info.fullname + ' (STAFF)' + '\n'

        if filename:
            if os.path.isfile(filename):  # Check if file exist
                openfile = open(filename, 'w')
                openfile.write(unallocated_list)
                openfile.close()
                print('Successfully output list of unallocated people to file')
            else:
                raise Exception('Cannot locate file')
        else:
            print(unallocated_list)

    def print_people(self):
        """Print all people to see their details"""
        all_persons = 'Loading all persons...\n'
        all_persons += 'ID NO\t\tFULL NAME\t\tPERSON-TYPE\tLIVING_ALLOCATED'\
                       '\tLIVING_SPACE\tOFFICE_ALLOCATED\tOFFICE_SPACE\n'
        all_persons += '............................................................'\
            '.........................................................................\n'
        for person, person_data in self.persons_data.items():
            all_persons += '%s\t%s\t\t%s\t\t%s\t\t\t%s\t\t%s\t\t\t%s\n' % (person_data.id,
                                                                           person_data.fullname, person_data.person_type.upper(),
                                                                           str(person_data.living_allocated), person_data.living.upper(
                                                                           ),
                                                                           person_data.office_allocated, person_data.office.upper())

        print(all_persons)
