from staff import Staff
from fellow import Fellow
from living import Living
from office import Office
from data.data_manager import DataManager

#from data import DataManager

class Amity():
    def add_person(self, firstname, lastname, person_type, living_choice ='N'):
        if person_type.upper() == 'STAFF' and living_choice.upper() == 'Y':
            raise Exception('Mismatch. Staff cannot be allocated living space')
        elif person_type.upper() == 'STAFF' and living_choice.upper() == 'N':
            self.add_staff(firstname,lastname)
        elif person_type.upper() == 'FELLOW' and living_choice.upper() == 'Y':
            self.add_fellow(firstname,lastname)
        else:
            print('Unidentifiable format')

    def add_staff(self,firstname,lastname):
        DataManager().add_staff(firstname,lastname)

    def add_fellow(self,firstname,lastname):
        DataManager().add_fellow(firstname,lastname)
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

    def create_office(self,office_name):
        DataManager().save_office(office_name)

    def create_living(self,living_name):
        DataManager().save_living(living_name)
    def print_allocations(self):
        DataManager().load_offices()
        DataManager().load_livings()
    def print_room(self,room_name):
        DataManager().print_room(room_name)
    def reallocate_person(self,person_id,new_room_name):
        DataManager().reallocate_person(person_id, new_room_name)
    def clear_room(self, room_name):
        DataManager().clear_room(room_name)
    def remove_room(self,room_name):
        DataManager().remove_room(room_name)