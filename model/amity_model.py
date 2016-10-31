from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import shelve

from data.data_manager import DataManager
from data.database_manager import DatabaseManager
from fellow import Fellow
from living import Living
from office import Office
from staff import Staff


class Amity():
    """This class is the entry point for the system"""

    def __init__(self, rooms_file='data_files/rooms',
                 persons_file='data_files/persons'):
        """Initializes the class and get the rooms file and persons file"""
        self.rooms_data = shelve.open(rooms_file)
        self.persons_data = shelve.open(persons_file)
        self.manager = DataManager(self.rooms_data, self.persons_data)

    def add_person(self, firstname, lastname,
                   person_type, living_choice='N'):
        """Calls the add_person method from the DataManager class"""
        self.manager.add_person(firstname, lastname,
                                person_type, living_choice)
        self.close_file()

    def create_room(self, room_name, room_type):
        """Checks room_type and calls save_room method from DataManager"""
        if room_type.upper() == 'OFFICE' or room_type.upper() == 'LIVING':
            self.manager.save_room(room_name, room_type)
        else:
            raise Exception('Room type invalid. Must be office or living')
        self.close_file()

    def print_allocations(self, filename=''):
        """Checks room_type and calls save_room method from DataManager"""
        self.manager.load_all_rooms(filename)
        self.close_file()

    def print_unallocated(self, filename=''):
        """Calls print_unallocated from DataManager class"""
        self.manager.print_unallocated(filename)
        self.close_file()

    def print_room(self, room_name):
        """Calls print_room method from DataManager class"""
        self.manager.print_room(room_name)
        self.close_file()

    def reallocate_person(self, person_id, new_room_name):
        """Calls reallocate_person method from DataManager class"""
        self.manager.reallocate_person(person_id, new_room_name)
        self.close_file()

    def load_people(self, filename):
        """Calls load_people method from DataManager class"""
        self.manager.load_people(filename)
        self.close_file()

    def save_state(self, filename):
        """Calls save_state method from DatabaseManager class"""
        DatabaseManager(self.rooms_data, self.persons_data,
                        filename).save_state()
        self.close_file()

    def load_state(self, filename):
        """Calls save_state method from DatabaseManager class"""
        DatabaseManager(self.rooms_data, self.persons_data,
                        filename).load_state()
        self.close_file()

    def print_people(self):
        """Calls save_state method from DataManager class"""
        self.manager.print_people()
        self.close_file()

    def close_file(self):
        """Close files"""
        self.rooms_data.close()
        self.persons_data.close()
