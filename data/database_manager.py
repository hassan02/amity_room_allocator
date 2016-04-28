import sqlite3

class DatabaseManager():
    def __init__(self, database_name = 'amity_data.db'):
        self.database_name = database_name
        if not self.database_name:
          self.database_name = 'amity_data.db'
        else:
          self.database_name = database_name
        self.db_conn = sqlite3.connect(self.database_name)
        self.db_cursor = self.amity_db_conn.cursor()

    def create_tables(self):
        self.db_cursor.execute('CREATE TABLE IF NOT EXISTS living( id INTEGER PRIMARY KEY AUTOINCREMENT, room_name TEXT(30), no_of_occupants INTEGER (1), members TEXT )')
        self.db_cursor.execute('CREATE TABLE IF NOT EXISTS office( id INTEGER PRIMARY KEY AUTOINCREMENT, room_name TEXT(30), no_of_occupants INTEGER (1), members TEXT )')
        self.db_cursor.execute('CREATE TABLE IF NOT EXISTS fellow( id INTEGER PRIMARY KEY AUTOINCREMENT, fellow_id TEXT(11), name TEXT (50), is_allocated TEXT(5), room_name TEXT )')
        self.db_cursor.execute('CREATE TABLE IF NOT EXISTS staff( id INTEGER PRIMARY KEY AUTOINCREMENT, staff_id TEXT(11), name TEXT (50), is_allocated TEXT(5), room_name TEXT )')
        self.db_conn.commit()
        self.db_conn.close()
        print('Table created')
    
    def save_state(self):
        if self.database_name == 'amity_data.db':
          print('Save to database')
        else:
          print('Creating table and loading from shelve')
    def save_to_database():
        pass

