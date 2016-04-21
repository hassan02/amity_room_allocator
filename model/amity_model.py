from staff import Staff
from fellow import Fellow
from living import Living
from office import Office
from data.pickler import Pickler
#from data import DataManager

class Amity():
  def new_staff(name):
    staff = Staff(name)
  def new_fellow(name):
    fellow = Fellow(name)
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
