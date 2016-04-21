from staff import Staff
from fellow import Fellow
from living import Living
from office import Office
from data.pickler import Pickler
#from data import DataManager

class Amity():
    def add_person(self, firstname, lastname,person_type,living_choice):
        if person_type == 'STAFF' and living_choice == 'Y':
            raise Exception('Mismatch. Staff cannot be allocated living space')
        elif person_type == 'STAFF' and (living_choice == 'N' or living_choice == None):
            self.add_staff(firstname,lastname)

    def add_staff(self,firstname,lastname):
        Pickler().add_staff(firstname,lastname)
    def add_fellow(self,firstname,lastname):
        pass
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
        Pickler().save_office(office_name)
    def create_living(self,living_name):
        Pickler().save_living(living_name)
    def print_allocations(self):
        Pickler().load_offices()
