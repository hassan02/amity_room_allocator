import sqlite3
import shelve

from model.living import Living
from model.office import Office
from model.staff import Staff
from model.fellow import Fellow


class DatabaseManager():
    def __init__(self, offices_file, livings_file, fellows_file, staffs_file, database_name = 'data_files/amity_data.db'):
        # Initializes all shelve files
        self.office_data = shelve.open(offices_file)
        self.living_data = shelve.open(livings_file)
        self.fellow_data = shelve.open(fellows_file)
        self.staff_data = shelve.open(staffs_file)
        self.data_info = shelve.open('data_files/data_info')
        self.database_name = database_name
        
        # Set database name
        if not self.database_name:
          self.database_name = 'data_files/amity_data.db'
        else:
          self.database_name = database_name

        # Set up a connection and cursor
        self.db_conn = sqlite3.connect(self.database_name)
        self.db_cursor = self.db_conn.cursor()

    def create_tables(self):
        # Create tables for database
        self.db_cursor.execute('CREATE TABLE IF NOT EXISTS office( id INTEGER PRIMARY KEY AUTOINCREMENT, room_name TEXT(30), no_of_occupants INTEGER (1), members TEXT )')
        self.db_cursor.execute('CREATE TABLE IF NOT EXISTS living( id INTEGER PRIMARY KEY AUTOINCREMENT, room_name TEXT(30), no_of_occupants INTEGER (1), members TEXT )')        
        self.db_cursor.execute('CREATE TABLE IF NOT EXISTS fellow( id INTEGER PRIMARY KEY AUTOINCREMENT, fellow_id TEXT(11), name TEXT (50), is_allocated TEXT(5), room_name TEXT )')
        self.db_cursor.execute('CREATE TABLE IF NOT EXISTS staff( id INTEGER PRIMARY KEY AUTOINCREMENT, staff_id TEXT(11), name TEXT (50), is_allocated TEXT(5), room_name TEXT )')
        self.db_conn.commit()
       
    
    def save_state(self):
        # Call create_table method
        self.create_tables()
        
        # Save all office information in the database
        for office_name, office_info in self.office_data.items():
            self.db_cursor.execute("SELECT id FROM office WHERE room_name = '%s'" % (office_name))
            members_list = ', '.join(office_info.members.values()) if office_info.members else 'EMPTY'
            row_exist=self.db_cursor.fetchall()
            if len(row_exist) == 0:    
                query = "INSERT INTO office(room_name, no_of_occupants, members) \
                                   VALUES ('%s',%d,'%s')" % (office_info.name, office_info.no_of_occupants, members_list)
            else:                
                query = "UPDATE office SET no_of_occupants = %d, members = '%s' WHERE room_name = '%s' \
                                    " % (office_info.no_of_occupants, members_list, office_name)
            self.db_cursor.execute(query)
        
        # Save all living information in the database
        for living_name, living_info in self.living_data.items():
            self.db_cursor.execute("SELECT id FROM living WHERE room_name = '%s'" % (living_name))
            members_list = ', '.join(living_info.members.values()) if living_info.members else 'EMPTY'
            row_exist=self.db_cursor.fetchall()
            if len(row_exist) == 0:
                query = "INSERT INTO living(room_name, no_of_occupants, members) \
                                       VALUES ('%s',%d,'%s')" % (living_info.name, living_info.no_of_occupants, members_list)
            else:
                query = "UPDATE living SET no_of_occupants = %d, members = '%s' WHERE room_name = '%s' \
                                    " % (living_info.no_of_occupants, members_list, office_name)
            self.db_cursor.execute(query)

        # Save all fellow information in the database
        for fellow, fellow_info in self.fellow_data.items():
            self.db_cursor.execute("SELECT id FROM fellow WHERE fellow_id = '%s'" % (fellow))
            row_exist=self.db_cursor.fetchall()
            if len(row_exist) == 0:
                query = "INSERT INTO fellow (fellow_id, name, is_allocated, room_name) \
                                       VALUES ('%s','%s', '%s','%s')" % (fellow_info.id, fellow_info.fullname, str(fellow_info.allocated), fellow_info.room)
            else:                
                query = "UPDATE fellow SET name = '%s', is_allocated = '%s', room_name = '%s'  WHERE fellow_id = '%s' \
                                    " % (fellow_info.fullname, str(fellow_info.allocated), fellow_info.room, fellow_info.id)
            self.db_cursor.execute(query)
        
        # Save all staff information in the database
        for staff, staff_info in self.staff_data.items():
            self.db_cursor.execute("SELECT id FROM staff WHERE staff_id = '%s'" % (staff))
            row_exist=self.db_cursor.fetchall()  # Check if staff_row already exist
            if len(row_exist) == 0:
                query = "INSERT INTO staff (staff_id, name, is_allocated, room_name) \
                                       VALUES ('%s','%s', '%s','%s')" % (staff_info.id, staff_info.fullname, str(staff_info.allocated), staff_info.room)
            else:                
                query = "UPDATE staff SET name = '%s', is_allocated = '%s', room_name = '%s'  WHERE staff_id = '%s' \
                                    " % (staff_info.fullname, str(staff_info.allocated), staff_info.room, staff_info.id)
            self.db_cursor.execute(query)
        
        # Commit and close connection
        self.db_conn.commit()
        self.db_conn.close()

        # Clear all files after saving
        self.office_data.clear()
        self.living_data.clear()
        self.fellow_data.clear()
        self.staff_data.clear()

        print('All information successfully saved to database')

    def load_state(self):
        # Create all offices
        officequery = "SELECT * FROM office"
        # Execute the SQL command
        self.db_cursor.execute(officequery)
        # Fetch all the rows in a list of lists.
        results = self.db_cursor.fetchall()
        for row in results:
          room_name = str(row[1])
          
          # Create new offices
          office = Office(room_name)
          self.office_data[room_name.lower()] = office
        
        # Create all living
        livingquery = "SELECT * FROM living"
        # Execute the SQL command
        self.db_cursor.execute(livingquery)
        # Fetch all the rows in a list of lists.
        results = self.db_cursor.fetchall()
        for row in results:
          room_name = str(row[1])
          
          # Create new living rooms
          living = Living(room_name)
          self.living_data[room_name.lower()] = living


        # Create all fellows
        fellowquery = "SELECT * FROM fellow"
        # Execute the SQL command
        self.db_cursor.execute(fellowquery)
        # Fetch all the rows in a list of lists.
        results = self.db_cursor.fetchall()
        for row in results:
            fellow_id = str(row[1])
            fellow_name = str(row[2])
            fellow_is_allocated = str(row[3])
            fellow_room_name = str(row[4]).lower()
            fellow_first_name = fellow_name.split(' ')[0]
            fellow_last_name = fellow_name.split(' ')[1]          
            # Create new fellows and add them to rooms or unallocated people
            fellow = Fellow(fellow_first_name, fellow_last_name)  # Create a Fellow object
            fellow.id = fellow_id
            fellow.allocated = fellow_is_allocated
            fellow.room = fellow_room_name
            
            if fellow.allocated == 'True':

                living_info = self.living_data[fellow_room_name]
                living_info.members[fellow.id] = fellow.fullname
                living_info.no_of_occupants = len(living_info.members)
                self.living_data[fellow_room_name] = living_info
                
            self.fellow_data[fellow.id] = fellow

           # Create all staffs
        
        staffquery = "SELECT * FROM staff"
        # Execute the SQL command
        self.db_cursor.execute(staffquery)
        # Fetch all the rows in a list of lists.
        results = self.db_cursor.fetchall()
        for row in results:
            staff_id = str(row[1])
            staff_name = str(row[2])
            staff_is_allocated = str(row[3])
            staff_room_name = str(row[4]).lower()
            staff_first_name = staff_name.split(' ')[0]
            staff_last_name = staff_name.split(' ')[1]          
            # Create new staffs and add them to rooms or unallocated people
            staff = Staff(staff_first_name, staff_last_name)  # Create a Staff object
            staff.id = staff_id
            staff.allocated = staff_is_allocated
            staff.room = staff_room_name

            if staff.allocated == 'True':

                office_info = self.office_data[staff_room_name]
                office_info.members[staff.id] = staff.fullname
                office_info.no_of_occupants = len(office_info.members)
                self.office_data[staff_room_name] = office_info
                
                #Save to staffs_data   
            self.staff_data[staff.id] = staff
          
        print('All information has been loaded back into the application')
        
    def close_file(self):
        self.office_data.close()
        self.living_data.close()
        self.fellow_data.close()
        self.staff_data.close()
        

      