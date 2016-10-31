from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
import shelve
import sqlite3

from model.living import Living
from model.office import Office
from model.staff import Staff
from model.fellow import Fellow


class DatabaseManager():
    """This class manage saving to and from sqlite database"""

    def __init__(
            self,
            rooms_data,
            persons_data,
            database_name='data_files/amity_database.db'):
        """Initializes the class and set the files"""
        # Initializes all shelve files
        self.rooms_data = rooms_data
        self.persons_data = persons_data
        self.database_name = database_name

        # Set database name
        if not self.database_name:
            self.database_name = 'data_files/amity_database.db'
        else:
            self.database_name = database_name

        # Set up a connection and cursor
        self.db_conn = sqlite3.connect(self.database_name)
        self.db_cursor = self.db_conn.cursor()

    def save_state(self):
        """Save the state of the system to database"""
        # Call create_table method
        self.create_tables()
        self.save_rooms()
        self.save_persons()
        print('All information successfully saved to database')

    def create_tables(self):
        """Create database tables if it doesn't exist"""
        # Create tables for database
        self.db_cursor.execute(
            "CREATE TABLE IF NOT EXISTS rooms( id INTEGER "
            "PRIMARY KEY AUTOINCREMENT, room_name TEXT(30), "
            "room_type TEXT (6), no_of_occupants INTEGER (1), "
            "members TEXT )")
        self.db_cursor.execute(
            "CREATE TABLE IF NOT EXISTS persons( id INTEGER "
            "PRIMARY KEY AUTOINCREMENT, person_id TEXT(11), "
            "person_name TEXT (50), person_type TEXT(6), living_allocated TEXT(5), "
            "living TEXT(30), office_allocated TEXT(5), office TEXT (30))")
        self.db_conn.commit()

    def save_rooms(self):
        """Save rooms to database: called from save_state"""
        # Save all rooms information in the database
        for room_name, room_info in self.rooms_data.items():
            self.db_cursor.execute(
                "SELECT id FROM rooms WHERE room_name = '%s'" %
                (room_name))
            row_exist = self.db_cursor.fetchall()
            members_list = ', '.join(
                room_info.members.values()) if room_info.members else 'EMPTY'
            if len(row_exist) == 0:
                query = "INSERT INTO rooms(room_name, room_type, no_of_occupants, members)" \
                    "VALUES ('%s','%s',%d,'%s')" % (room_info.name, room_info.room_type,
                                                    room_info.no_of_occupants, members_list)
            else:
                query = "UPDATE rooms SET no_of_occupants = %d, room_type = '%s', members = '%s' WHERE " \
                        "room_name = '%s'" % (
                            room_info.no_of_occupants, room_info.room_type, members_list, room_name)
            self.db_cursor.execute(query)

    def save_persons(self):
        """Save persons to database: called from save_state"""
        # Save all person information in the database
        for person, person_info in self.persons_data.items():
            self.db_cursor.execute(
                "SELECT id FROM persons WHERE person_id = '%s'" %
                (person))
            row_exist = self.db_cursor.fetchall()
            if len(row_exist) == 0:
                query = "INSERT INTO persons (person_id, person_name, person_type, living_allocated," \
                        "living, office_allocated, office) VALUES ('%s','%s','%s','%s','%s', '%s','%s')" % \
                        (person_info.id, person_info.fullname, person_info.person_type, str(person_info.living_allocated),
                         person_info.living, str(person_info.office_allocated), person_info.office)
            else:
                query = "UPDATE persons SET person_name = '%s', living_allocated = '%s'," \
                        "living = '%s', office_allocated = '%s', office = '%s'" \
                        "WHERE person_id = '%s'" % (person_info.fullname,
                                                    str(person_info.living_allocated), person_info.living,
                                                    str(person_info.office_allocated), person_info.office, person_info.id)
            self.db_cursor.execute(query)

        # Commit and close connection
        self.db_conn.commit()
        self.db_conn.close()

        # Clear all files after saving
        self.rooms_data.clear()
        self.persons_data.clear()

    def load_rooms(self):
        """Load the rooms from database: called from load_state"""
        # Create all rooms
        roomquery = "SELECT * FROM rooms"
        # Execute the SQL command
        self.db_cursor.execute(roomquery)
        # Fetch all the rows in a list of lists.
        results = self.db_cursor.fetchall()
        for row in results:
            room_name = str(row[1]).lower()
            room_type = str(row[2]).lower()
            # Create new rooms
            room = Office(
                room_name) if room_type == 'office' else Living(room_name)
            self.rooms_data[room_name] = room

    def load_persons(self):
        """Load persons from database. called from load_state"""
        # Create all persons
        personquery = "SELECT * FROM persons"
        # Execute the SQL command
        self.db_cursor.execute(personquery)
        # Fetch all the rows in a list of lists.
        results = self.db_cursor.fetchall()
        for row in results:
            name = str(row[2])
            person_type = str(row[3])
            first_name = name.split(' ')[0]
            last_name = name.split(' ')[1]
            # Create new persons and add them to rooms or unallocated people
            person = Fellow(
                first_name,
                last_name) if person_type.upper() == 'FELLOW' else Staff(
                first_name,
                last_name)
            person.id = str(row[1])
            person.living_allocated = str(row[4])
            person.living = str(row[5]).lower()
            person.office_allocated = str(row[6])
            person.office = str(row[7]).lower()

            if person.living_allocated == 'True':
                room_info = self.rooms_data[person.living]
                room_info.members[person.id] = person.fullname
                room_info.no_of_occupants = len(room_info.members)
                self.rooms_data[person.living] = room_info

            if person.office_allocated == 'True':
                room_info = self.rooms_data[person.office]
                room_info.members[person.id] = person.fullname
                room_info.no_of_occupants = len(room_info.members)
                self.rooms_data[person.office] = room_info

            self.persons_data[person.id] = person

    def load_state(self):
        """Load system state from database"""
        self.load_rooms()
        self.load_persons()
        print('All information has been loaded back into the application')
