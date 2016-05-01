import sqlite3
import shelve

class DatabaseManager():
    def __init__(self, offices_file, livings_file, fellows_file, staffs_file, database_name = 'data_files/amity_data.db'):
        self.office_data = shelve.open(offices_file)
        self.living_data = shelve.open(livings_file)
        self.fellow_data = shelve.open(fellows_file)
        self.staff_data = shelve.open(staffs_file)
        self.database_name = database_name
        if not self.database_name:
          self.database_name = 'data_files/amity_data.db'
        else:
          self.database_name = database_name
        self.db_conn = sqlite3.connect(self.database_name)
        self.db_cursor = self.db_conn.cursor()

    def create_tables(self):
        self.db_cursor.execute('CREATE TABLE IF NOT EXISTS office( id INTEGER PRIMARY KEY AUTOINCREMENT, room_name TEXT(30), no_of_occupants INTEGER (1), members TEXT )')
        self.db_cursor.execute('CREATE TABLE IF NOT EXISTS living( id INTEGER PRIMARY KEY AUTOINCREMENT, room_name TEXT(30), no_of_occupants INTEGER (1), members TEXT )')        
        self.db_cursor.execute('CREATE TABLE IF NOT EXISTS fellow( id INTEGER PRIMARY KEY AUTOINCREMENT, fellow_id TEXT(11), name TEXT (50), is_allocated TEXT(5), room_name TEXT )')
        self.db_cursor.execute('CREATE TABLE IF NOT EXISTS staff( id INTEGER PRIMARY KEY AUTOINCREMENT, staff_id TEXT(11), name TEXT (50), is_allocated TEXT(5), room_name TEXT )')
        self.db_conn.commit()
       
    
    def save_state(self):
        self.create_tables()
        
        for office_name, office_info in self.office_data.items():
            self.db_cursor.execute("SELECT id FROM office WHERE room_name = '%s'" % (office_name))
            data=self.db_cursor.fetchall()
            if len(data) == 0:
                members_list = ', '.join(office_info.members.values()) if office_info.members else 'EMPTY'
                query = "INSERT INTO office(room_name, no_of_occupants, members) \
                                   VALUES ('%s',%d,'%s')" % (office_info.name, office_info.no_of_occupants, members_list)
                self.db_cursor.execute(query)
            else:
                pass
                #members_list = ', '.join(office_info.members.values()) if office_info.members else 'EMPTY'
                #query = "UPDATE office (room_name, no_of_occupants, members) \
                #                   VALUES ('%s',%d,'%s')" % (office_info.name, office_info.no_of_occupants, members_list)
                #self.db_cursor.execute(query)

            
        for living, living_info in self.living_data.items():
            members_list = ', '.join(living_info.members.values()) if living_info.members else 'EMPTY'
            query = "INSERT INTO living(room_name, no_of_occupants, members) \
                                   VALUES ('%s',%d,'%s')" % (living_info.name, living_info.no_of_occupants, members_list)
            self.db_cursor.execute(query)

        for fellow, fellow_info in self.fellow_data.items():
            query = "INSERT INTO fellow(fellow_id, name, is_allocated, room_name) \
                                   VALUES ('%s','%s', '%s','%s')" % (fellow_info.id, fellow_info.fullname, str(fellow_info.allocated), fellow_info.room)
            self.db_cursor.execute(query)
        
        for staff, staff_info in self.staff_data.items():
            query = "INSERT INTO staff(staff_id, name, is_allocated, room_name) \
                                   VALUES ('%s','%s', '%s','%s')" % (staff_info.id, staff_info.fullname, str(staff_info.allocated), staff_info.room)
            self.db_cursor.execute(query)
        
        self.db_conn.commit()
        self.db_conn.close()
        print('All info saved')

    def load_state(self):
      officequery = "SELECT * FROM office"
      # Execute the SQL command
      self.db_cursor.execute(officequery)
      # Fetch all the rows in a list of lists.
      results = self.db_cursor.fetchall()
      for row in results:
          room_name = row[1]
          no_of_occupants = row[2]
          members_list = row[3]
          # Now print fetched result
          print "Room name=%s\nOccupants=%d\nMembers-list=%s" % \
                   (room_name, no_of_occupants, members_list)

      living_query = "SELECT * FROM living"
      # Execute the SQL command
      self.db_cursor.execute(living_query)
      # Fetch all the rows in a list of lists.
      living_results = self.db_cursor.fetchall()
      for row in living_results:
          room_name = row[1]
          no_of_occupants = row[2]
          members_list = row[3]
          # Now print fetched result
          print "Room name=%s\nOccupants=%d\nMembers-list=%s" % \
                   (room_name, no_of_occupants, members_list)
      