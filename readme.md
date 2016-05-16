<snippet>
<content>

# Amity Room Allocation

[![Build Status](https://travis-ci.org/andela-hoyeboade/amity_room_allocator.svg?branch=working)](https://travis-ci.org/andela-hoyeboade/amity_room_allocator) [![Coverage Status](https://coveralls.io/repos/github/andela-hoyeboade/amity_room_allocator/badge.svg?branch=working)](https://coveralls.io/github/andela-hoyeboade/amity_room_allocator?branch=working)

## Description
This is a Python Checkpoint1 project for D0B fellows in Andela. It's a console application modelled for one of Andela facilities, Amity. It can be used to allocate fellows and staffs to offices or living spaces. Offices and living spaces can be created and Fellows and Staffs can be added to the rooms. Fellows and Staffs are allocated offices by default, while fellows can choose if they want a living space or not. 

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

  Create a new office called _Moon_:
  ```
  python amity.py create_room Moon office
  ```
  Create a new living space called _Cedar_:
  ```
  python amity.py create_room Cedar living
  ```
  Create multiple rooms with _Neptune_ as office, _Iroko_ as living space and _Saturn_ as office:
  ```
  python amity.py create_room Neptune office Iroko living Saturn office
  ```
  Add a fellow HASSAN OYEBOADE to the system but don't allocate him a living space:
  ```
  python amity.py add_person HASSAN OYEBOADE FELLOW N
  ```
  Add a fellow SUNDAY NWUGURU to the system and allocate him to an available living space and office:
  ```
  python amity.py add_person SUNDAY NWUGURU FELLOW Y
  ```
  Add a staff PROSPER OTEMUYIWA to the system and allocate him to an available office:
  ```
  python amity.py add_person PROSPER OTEMUYIWA STAFF
  ```
  Reallocate person with ID: F3WEDS32WED to _Obeche_:
  ```
  python amity.py reallocate_person F3WEDS32WED obeche
  ```
  Load people from text file input.txt and add them to the system:
  ```
  python amity.py load_people input.txt
  ```
  Print all allocations to the screen:
  ```
  python amity.py print_allocations
  ```
  Print all allocations to the text file allocations.txt:
  ```
  python amity.py print_allocations [--o=allocations.txt]
  ```
  Print all the members of _Obeche_:
  ```
  python amity.py print_room obeche
  ```
  Print all unallocated people to the screen:
  ```
  python amity.py print_unallocated
  ```
  Print all unallocated people to text file unallocated.txt:
  ```
  python amity.py print_unallocated [--o=unallocated.txt]
  ```
  Save the state of the system to the database:
  ```
  amity.py save_state
  ```
  Save the state of system to the database mydatabase.db:
  ```
  amity.py save_state [--db=mydatabase.db]
  ``` 
  Load the state of the system from the database:
  ```
  amity.py load_state
  ```
  Load the state of the system from the database mydatabase.db:
  ```
  amity.py load_state [--db=mydatabase.db]
  ```
  Print a list of all persons in the system to get their ID, Name and Allocations:
  ```
  amity.py print_people
  ```

## Running tests
1. Navigate to the project direcory
2. Run nosetests --with-coverage --cover-package=model --cover-package=data to run test and check coverage

## References
https://github.com/docopt/docopt
http://docopt.org/

## Author
Hassan Oyeboade

## License
MIT License

</content>
</snippet>