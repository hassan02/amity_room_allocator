# amity_model

Amity has rooms which can be offices or living spaces. An office can occupy a maximum of 6 people. A living space can inhabit a maximum of 4 people.

A person to be allocated could be a fellow or staff. Staff cannot be allocated living spaces. Fellows have a choice to choose a living space or not.

This system will be used to automatically allocate spaces to people at random

1. create_room <room_name>...​ - Creates rooms in Amity. Using this command I should be able to create as many rooms as possible by specifying multiple room names after the ​create_room​ command.

2. add_person <person_name> <FELLOW|STAFF> [wants_accommodation]​ - Adds a person to the system and allocates the person to a random room. Wants_accommodation​ here is an optional argument which can be either ​Y​ or ​N​. The default value if it is not provided is ​N​.

3. reallocate_person <person_identifier> <new_room_name>​ - Reallocate the person with ​person_identifier​ to ​new_room_name​.

4. load_people​ - Adds people to rooms from a txt file. See Appendix 1A for text input format.

5. print_allocations [­o=filename]​ - Prints a list of allocations onto the screen. Specifying the optional ​­o​ option here outputs the registered allocations to a txt file. See Appendix 2A for format.

6. print_unallocated [­o=filename]​ - Prints a list of unallocated people to the screen. Specifying the ​­o​ option here outputs the information to the txt file provided.

7. print_room <room_name>​ - Prints the names of all the people in ​room_name​ on the
screen.

8. save_state [­­db=sqlite_database]​ - Persists all the data stored in the app to a
SQLite database. Specifying the ​­­db​ parameter explicitly stores the data in the
sqlite_database​ specified.

9. load_state <sqlite_database>​ - Loads data from a database into the application.