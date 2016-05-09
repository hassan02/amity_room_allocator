# Amity Room Allocation

[![Build Status](https://travis-ci.org/andela-hoyeboade/amity_model.svg?branch=working)](https://travis-ci.org/andela-hoyeboade/amity_model)

Amity has rooms which can be offices or living spaces. An office can occupy a maximum of 6 people. A living space can inhabit a maximum of 4 people.

A person to be allocated could be a fellow or staff. Staff cannot be allocated living spaces. Fellows have a choice to choose a living space or not.

This system will be used to automatically allocate spaces to people at random

1. create_room <room_name> <room_type>...​ - Creates one or rooms in Amity by specifying room name and room type. 

2. add_person <person_name> <FELLOW|STAFF> [wants_accommodation]​ - Adds a person to the system and allocates the person to a random room. Wants_accommodation​ can be either ​Y​ or ​N​. If it is not provided, it will be assumed to be ​N​.

3. reallocate_person <person_identifier> <new_room_name>​ - Reallocate the person with ​person_identifier​ to ​new_room_name​.

4. load_people​ - Adds people to rooms from a txt file. 

5. print_allocations [­o=filename]​ - Prints a list of allocations onto the screen. Specifying the optional ​­o​ option here outputs the registered allocations to the txt file specified. 

6. print_unallocated [­o=filename]​ - Prints a list of unallocated people to the screen. Specifying the ​­o​ option here outputs the information to the txt file provided.

7. print_room <room_name>​ - Prints the names of all the people in ​room_name​ on the screen.

8. save_state [­­db=sqlite_database]​ - Persists all the data stored in the app to a SQLite database. Specifying the ​­­db​ parameter explicitly stores the data in the sqlite_database​ specified.

9. load_state [db=sqlite_database>] - Loads data from a database into the application.

Using the system.

Usage:
```
  amity.py create_room (<room_names> <room_types>)...
  amity.py add_person <first_name> <last_name> <STAFF/FELLOW> [<wants_accommodation>]
  amity.py reallocate_person <person_identifier> <new_room_name>
  amity.py load_people <filename>
  amity.py print_room <room_name>
  amity.py print_allocations [--o=filename]
  amity.py print_unallocated [--o=filename]
  amity.py save_state [--db=sqlite_database]
  amity.py load_state [--db=sqlite_database]
  amity.py -h | --help
```
Examples:
```
  amity.py create_room Moon office
  amity.py create_room Cedar living
  amity.py add_person HASSAN OYEBOADE FELLOW N
  amity.py add_person SUNDAY NWUGURU FELLOW Y
  amity.py add_person PROSPER OTEMUYIWA STAFF
  amity.py reallocate_person F3WEDS32WED obeche
  amity.py load_people input.txt
  amity.py print_allocations [--o=allocations.txt]
  amity.py print_unallocated [--o=unallocated.txt]
  amity.py save_state
  amity.py save_state [--db=mydatabase.db]
  amity.py load_state
  amity.py load_state [--db=mydatabase.db]

  
```