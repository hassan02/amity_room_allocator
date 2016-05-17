"""Amity Model

Usage:
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

Examples:
  python amity.py create_room Moon office
  python amity.py create_room Cedar living
  python amity.py add_person HASSAN OYEBOADE FELLOW N
  python amity.py add_person SUNDAY NWUGURU FELLOW Y
  python amity.py add_person PROSPER OTEMUYIWA STAFF
  python amity.py reallocate_person F3WEDS32WED obeche
  python amity.py load_people input.txt
  python amity.py print_room obeche
  python amity.py print_allocations
  python amity.py print_allocations --o=allocations.txt
  python amity.py print_unallocated
  python amity.py print_unallocated --o=unallocated.txt
  python amity.py save_state
  python amity.py save_state --db=mydatabase.db
  python amity.py load_state
  python amity.py load_state --db=mydatabase.db
  python amity.py print_people
  
Options:
    -h, --help  Show this screen and exit.
    
"""
from clint.textui import colored
from docopt import docopt

from model.amity_model import Amity

print(colored.yellow('..............................................................................'))
print(colored.green('....................Welcome to Amity Room Allocator...........................'))
print(colored.green('........Please run any of the commands below to perform an operation..........'))
print(colored.yellow('..............................................................................'))

if __name__ == '__main__':
  arguments = docopt(__doc__)
  if arguments['create_room']:
    room_names = arguments['<room_names>']
    room_types = arguments['<room_types>']
    for room_name, room_type in zip(room_names,room_types):
      Amity().create_room(room_name,room_type)

  elif arguments['add_person']:
    Amity().add_person(arguments['<first_name>'], arguments['<last_name>'], arguments['<STAFF/FELLOW>'], arguments['<wants_accommodation>'])
  elif arguments['print_room']:
    Amity().print_room(arguments['<room_name>'])
  elif arguments['reallocate_person']:
    Amity().reallocate_person(arguments['<person_identifier>'], arguments['<new_room_name>'])
  elif arguments['load_people']:
    Amity().load_people(arguments['<filename>'])
  elif arguments['print_allocations']:
    Amity().print_allocations(arguments['--o'])
  elif arguments['print_unallocated']:
    Amity().print_unallocated(arguments['--o'])
  elif arguments['save_state']:
    Amity().save_state(arguments['--db'])
  elif arguments['load_state']:
    Amity().load_state(arguments['--db'])
  elif arguments['print_people']:
    Amity().print_people()