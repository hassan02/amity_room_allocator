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
    def __init__(self, rooms_file='data_files/rooms', 
                 persons_file='data_files/persons'):
        self.rooms_file = rooms_file
        self.persons_file = persons_file
        self.manager = DataManager(self.rooms_file, self.persons_file)
        
    def add_person(self, firstname, lastname, 
                   person_type, living_choice='N'):
        self.manager.add_person(firstname,lastname,person_type,living_choice)
        self.manager.close_file()
   
    def create_room(self, room_name, room_type):
        if room_type.upper() == 'OFFICE' or room_type.upper() == 'LIVING':
            self.manager.save_room(room_name, room_type)
        else:
          raise Exception('Room type invalid. Must be office or living')
        self.manager.close_file()
    
    def print_allocations(self, filename=''):
        self.manager.load_all_rooms(filename)
        self.manager.close_file()
    
    def print_unallocated(self, filename=''):
        self.manager.print_unallocated(filename)
        self.manager.close_file()
    
    def print_room(self, room_name):
        self.manager.print_room(room_name)
        self.manager.close_file()
    
    def reallocate_person(self, person_id, new_room_name):
        self.manager.reallocate_person(person_id, new_room_name)
        self.manager.close_file()
    
    def load_people(self, filename):
        self.manager.load_people(filename)
        self.manager.close_file()
    
    def save_state(self, filename):
        self.db_manager = DatabaseManager(self.rooms_file, self.persons_file, filename)
        self.db_manager.save_state()
        self.db_manager.close_file()
    
    def load_state(self, filename):
        self.db_manager = DatabaseManager(self.rooms_file, self.persons_file, filename)
        self.db_manager.load_state()
        self.db_manager.close_file()
    
    def print_people(self):
        self.manager.print_people()