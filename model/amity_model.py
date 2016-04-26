from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from staff import Staff
from fellow import Fellow
from living import Living
from office import Office
from data.data_manager import DataManager
import shelve
#from data import DataManager

class Amity():

    def __init__(self, office_data = 'data_files/offices', living_data = 'data_files/living', fellow_data = 'data_files/fellows', staff_data = 'data_files/staff'):
        self.new_data = DataManager(office_data, living_data, fellow_data, staff_data)

    def add_person(self, firstname, lastname, person_type, living_choice):
        self.new_data.add_person(firstname,lastname,person_type,living_choice)
        self.new_data.close_file()
   

    #def add_staff(self,firstname,lastname):
     #  DataManager().close_file()
    #def add_fellow(self,firstname,lastname):
     #   DataManager().add_fellow(firstname,lastname)
        #fellow = Fellow(name)

    def create_room(self,room_name,room_type):
        if not isinstance(room_name,str):
            raise Exception('Room name invalid. Must be a string')
        if room_type.upper() == 'OFFICE':
            self.create_office(room_name)
        elif room_type.upper() == 'LIVING':
            self.create_living(room_name)
        else:
          raise Exception('Room type invalid. Must be office or living')
        self.new_data.close_file()
    def create_office(self,office_name):
        self.new_data.save_office(office_name)
        self.new_data.close_file()
    def create_living(self,living_name):
        self.new_data.save_living(living_name)
        self.new_data.close_file()
    def print_allocations(self):
        self.new_data.load_offices()
        self.new_data.load_livings()
        self.new_data.close_file()
    def print_unallocated(self):
        self.new_data.print_unallocated()
        self.new_data.close_file()
    def print_room(self,room_name):
        self.new_data.print_room(room_name)
        self.new_data.close_file()
    def reallocate_person(self,person_id,new_room_name):
        self.new_data.reallocate_person(person_id, new_room_name)
        self.new_data.close_file()
    def clear_room(self, room_name):
        self.new_data.clear_room(room_name)
        self.new_data.close_file()
    def remove_room(self,room_name):
        self.new_data.remove_room(room_name)
        self.new_data.close_file()
    def load_people(self,filename):
        self.new_data.load_people(filename)
        self.new_data.close_file()
    def reset(self,room_name):
        pass