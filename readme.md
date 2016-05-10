<snippet>
<content>

[![Build Status](https://travis-ci.org/andela-hoyeboade/amity_model.svg?branch=working)](https://travis-ci.org/andela-hoyeboade/amity_model)

[![Coverage Status](https://coveralls.io/repos/github/andela-hoyeboade/amity_model/badge.svg?branch=working)](https://coveralls.io/github/andela-hoyeboade/amity_model?branch=working)

# Amity Room Allocation
Python console application for allocating fellows and staffs to offices or living spaces in Amity.

## Installation
Clone the repo
```git clone https://github.com/andela-hoyeboade/amity_room_allocator.git/``` and navigate to the project directory

Install dependencies
```pip install -r requirements.txt```

Run the program 
```python amity.py``` shows a list of available commands

## Usage:
```
  python amity.py create_room (<room_names> <room_types>)...
  python amity.py add_person <first_name> <last_name> <STAFF/FELLOW> [<wants_accommodation>]
  python amity.py reallocate_person <person_identifier> <new_room_name>
  python amity.py load_people <filename>
  python amity.py print_room <room_name>
  python amity.py print_allocations [--o=filename]
  python amity.py print_unallocated [--o=filename]
  python amity.py save_state [--db=sqlite_database]
  python amity.py load_state [--db=sqlite_database]
  python amity.py print_people
  python amity.py -h | --help
```
## Usage Examples:

  ```python amity.py create_room Moon office``` Create a new office Moon
  ```python amity.py create_room Cedar living``` Create a new living space Cedar
  ```python amity.py create_room Neptune office Iroko living Saturn office``` Create multiple rooms with Neptune as office, Iroko as living space and Saturn as office
  ```python amity.py add_person HASSAN OYEBOADE FELLOW N``` Add a fellow HASSAN OYEBOADE to the system 
  ```python amity.py add_person SUNDAY NWUGURU FELLOW Y``` Add a fellow SUNDAY NWUGURU to the system and allocate him to an available living space
  ```python amity.py add_person PROSPER OTEMUYIWA STAFF``` Add a staff PROSPER OTEMUYIWA to the system and allocate him to an available office
  ```python amity.py reallocate_person F3WEDS32WED obeche``` Reallocate person with ID: F3WEDS32WED to room obeche
  ```python amity.py load_people input.txt``` Load people from text file input.txt and add them to the system
  ```python amity.py print_allocations``` Print all allocations to the screen
  ```python amity.py print_allocations [--o=allocations.txt]``` Print all allocations to the text file allocations.txt
  ```python amity.py print_unallocated``` Print all unallocated people to the screen
  ```python amity.py print_unallocated [--o=unallocated.txt]``` Print all unallocated people to text file unallocated.txt
  ```amity.py save_state``` Save the state of the system to the database
  ```amity.py save_state [--db=mydatabase.db]``` Save the state of system to the database mydatabase.db
  ```amity.py load_state``` Load the state of the system from the database
  ```amity.py load_state [--db=mydatabase.db]``` Load the state of the system from the database mydatabase.db
  ```amity.py print_people``` Print a list of all persons in the system to get their ID, Name and Allocations

## Running tests
1. Navigate to the project direcory
2. Run nosetests --with-coverage --cover-package=model --cover-package=data to run test and check coverage

## Credits
Glory be to God Almighty for helping me in completing this task. I would also like to appreciate my trainer, Anthony Nandaa, my mentor Mayowa Falade and my team mates Sunday Nwuguru and Chukwuerika Dike for their help throughout the course of implementing this checkpoint. And to all thosewho assisted me in one way or the other during this projects. I say `Thank you all`

## License
MIT License 

</content>
</snippet>