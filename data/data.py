from sqlalchemy import *
from sqlalchemy.orm import *
from living import Living
from office import Office

db = create_engine('sqlite:///data2.db')

db.echo = False  # Try changing this to True and see what happens

metadata = MetaData(db)

class DataManager():
  living = Table('living4', metadata, autoload=True)
  office = Table('office', metadata, autoload=True)
  def __init__(self):
    pass
  
  def new_living_table(self):
    pass
    living = Table('living4', metadata,
    Column('living_id', Integer, primary_key=True),
    Column('living_name', String(40)),
    Column('no_of_occupants', Integer),
    Column('members', String),
    )
    living.create()
  def insert_row_living(self, living_name):
    session = Session()
    mapper(Living, self.living)
    newliving = Living(living_name)
    session.add(newliving)
    session.commit()
    clear_mappers()
    print('Living room created')

  def insert_row_office(self, office_name):
    session = Session()
    mapper(Office, self.office)
    newoffice = Office(office_name)
    session.add(newoffice)
    session.commit()
    clear_mappers()
    print('Office room created')


  def view_living(self):
    s = self.living.select()
    rs = s.execute()
    for row in rs:
      print(str(row.living_id) + '\n' + row.living_name + ' (LIVING)'+ '\n' + str(row.no_of_occupants) + '\n' + row.members)

  def view_office(self):
    s = self.office.select()
    rs = s.execute()
    for row in rs:
      print (str(row.office_id) + '\n' + row.office_name + ' (OFFICE)'+ '\n' + str(row.no_of_occupants) + '\n' + row.members)

  def new_office_table(self):
    office = Table('office', metadata,
    Column('office_id', Integer, primary_key=True),
    Column('office_name', String(40)),
    Column('no_of_occupants', Integer),
    Column('members', String),
    )
    office.create()
#DataManager().new_living_table()
#DataManager().new_office_table()
#DataManager().insert_row_living('ADE',0,'EMPTY')  
#DataManager().view_living()
