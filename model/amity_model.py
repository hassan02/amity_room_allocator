from staff import Staff
from fellow import Fellow
from living import Living
from office import Office
from data.data_manager import DataManager
from data.database_manager import DatabaseManager
import shelve
#from data import DataManager

class Amity():

    def __init__(self, office_data = 'data_files/offices', living_data = 'data_files/living', fellow_data = 'data_files/fellows', staff_data = 'data_files/staff'):
        self.manager = DataManager(office_data, living_data, fellow_data, staff_data)
       
    def add_person(self, firstname, lastname, person_type, living_choice):
        self.manager.add_person(firstname,lastname,person_type,living_choice)
        self.manager.close_file()
   
    def create_room(self,room_name,room_type):
        if not isinstance(room_name,str):
            raise Exception('Room name invalid. Must be a string')
        if room_type.upper() == 'OFFICE':
            self.create_office(room_name)
        elif room_type.upper() == 'LIVING':
            self.create_living(room_name)
        else:
          raise Exception('Room type invalid. Must be office or living')
        self.manager.close_file()
    def create_office(self,office_name):
        self.manager.save_office(office_name)
        self.manager.close_file()
    def create_living(self,living_name):
        self.manager.save_living(living_name)
        self.manager.close_file()
    def print_allocations(self):
        self.manager.load_all_rooms()
        self.manager.close_file()
    def print_unallocated(self):
        self.manager.print_unallocated()
        self.manager.close_file()
    def print_room(self,room_name):
        self.manager.print_room(room_name)
        self.manager.close_file()
    def reallocate_person(self,person_id,new_room_name):
        self.manager.reallocate_person(person_id, new_room_name)
        self.manager.close_file()
    def clear_room(self, room_name):
        self.manager.clear_room(room_name)
        self.manager.close_file()
    def remove_room(self,room_name):
        self.manager.remove_room(room_name)
        self.manager.close_file()
    def load_people(self,filename):
        self.manager.load_people(filename)
        self.manager.close_file()
    def save_state(self,filename):
         self.database_manager = DatabaseManager(filename)
         self.database_manager.save_state()

    def reset(self,room_name):
        pass