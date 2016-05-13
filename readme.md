<snippet>
<content>

[![Build Status](https://travis-ci.org/andela-hoyeboade/amity_room_allocator.svg?branch=working)](https://travis-ci.org/andela-hoyeboade/amity_room_allocator) [![Coverage Status](https://coveralls.io/repos/github/andela-hoyeboade/amity_room_allocator/badge.svg?branch=working)](https://coveralls.io/github/andela-hoyeboade/amity_room_allocator?branch=working)

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
  amity.py create_room (<room_names> <room_types>)...
  amity.py add_person <first_name> <last_name> <STAFF/FELLOW> [<wants_accommodation>]
  amity.py reallocate_person <person_identifier> <new_room_name>
  amity.py load_people <filename>
  amity.py print_room <room_name>
  amity.py print_allocations [--o=filename]
  amity.py print_unallocated [--o=filename]
  amity.py save_state [--db=sqlite_database]
  amity.py load_state [--db=sqlite_database]
  amity.py print_people
  amity.py -h | --help
```
## Usage Examples:

  ```python amity.py create_room Moon office``` Create a new office Moon <br />
  ```python amity.py create_room Cedar living``` Create a new living space Cedar <br />
  ```python amity.py create_room Neptune office Iroko living Saturn office``` Create multiple rooms with Neptune as office, Iroko as living space and Saturn as office <br />
  ```python amity.py add_person HASSAN OYEBOADE FELLOW N``` Add a fellow HASSAN OYEBOADE to the system <br />
  ```python amity.py add_person SUNDAY NWUGURU FELLOW Y``` Add a fellow SUNDAY NWUGURU to the system and allocate him to an available living space <br />
  ```python amity.py add_person PROSPER OTEMUYIWA STAFF``` Add a staff PROSPER OTEMUYIWA to the system and allocate him to an available office <br />
  ```python amity.py reallocate_person F3WEDS32WED obeche``` Reallocate person with ID: F3WEDS32WED to room obeche <br />
  ```python amity.py load_people input.txt``` Load people from text file input.txt and add them to the system <br />
  ```python amity.py print_allocations``` Print all allocations to the screen <br />
  ```python amity.py print_allocations [--o=allocations.txt]``` Print all allocations to the text file allocations.txt <br />
  ```python amity.py print_room obeche``` Print all the members of Room Obeche <br />
  ```python amity.py print_unallocated``` Print all unallocated people to the screen <br />
  ```python amity.py print_unallocated [--o=unallocated.txt]``` Print all unallocated people to text file unallocated.txt <br />
  ```amity.py save_state``` Save the state of the system to the database <br />
  ```amity.py save_state [--db=mydatabase.db]``` Save the state of system to the database mydatabase.db <br />
  ```amity.py load_state``` Load the state of the system from the database <br />
  ```amity.py load_state [--db=mydatabase.db]``` Load the state of the system from the database mydatabase.db <br />
  ```amity.py print_people``` Print a list of all persons in the system to get their ID, Name and Allocations

## Running tests
1. Navigate to the project direcory
2. Run nosetests --with-coverage --cover-package=model --cover-package=data to run test and check coverage

## Credits
Glory be to God Almighty for helping me complete this task. I would also like to appreciate my trainer, Anthony Nandaa, my mentor `Mayowa Falade` and my team mates `Sunday Nwuguru` and `Chukwuerika Dike` for their constant help throughout the course of implementing this checkpoint. And to all those who assisted me in one way or the other during the course of this project. I say `Thank you all`

## Author
Hassan Oyeboade

## License
MIT License

</content>
</snippet>