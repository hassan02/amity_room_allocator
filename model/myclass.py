from sqlalchemy import *
from sqlalchemy.orm import *

db = create_engine('sqlite:///tutorial.db')

db.echo = False  # Try changing this to True and see what happens
metadata = MetaData(db)
living = Table('living4', metadata, autoload=True)
office = Table('office', metadata, autoload=True)

class Room(object):
  def getName(self):
    return self.__name

  def setName(self, name):
    if isinstance(name, str):
      self.__name = name
    else:
      raise 'Invalid argument'

class Living(Room):
  def __init__(self,name):
    self.setName(name)
    self.living_name = self.getName()
    self.members = 'EMPTY'
    self.no_of_occupants = 0
    
   

  def create_new_living(self):
    name = 'Iroko'
    no_of_occupants = 0
    members = 'EMPTY'
    DataManager().insert_row_living(name,no_of_occupants,members)

  def view_living(self):
    DataManager().view_living()

class Office(Room):
  def __init__(self,name):
    self.setName(name)
    self.office_name = self.getName()
    self.members = 'EMPTY'
    self.no_of_occupants = 0
    
  def create_new_office(self):
    name = 'Iroko'
    no_of_occupants = 0
    members = 'EMPTY'
    DataManager().insert_row_office(name,no_of_occupants,members)

  def view_office(self):
    DataManager().view_office()

class Save_Living(object):
  
  def __init__(self, name):
    self.name = name
  def save_to_memory(self):
    session = Session()
    mapper(Living, living)
    newliving = Living(self.name)
    session.add(newliving)
    session.commit()
    clear_mappers()
    print 'Living room created'

class Save_Office(object):
  
  def __init__(self, name):
    self.name = name
  def save_to_memory(self):
    session = Session()
    mapper(Office, office)
    newoffice = Office(self.name)
    session.add(newoffice)
    session.commit()
    clear_mappers()
    print 'Office created'
class Save_to_database():
  session2 = Session() 
  def __init__(self):
    pass

