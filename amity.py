"""Amity Model

Usage:
  amity.py show
  amity.py print_allocations
  amity.py create_room <room_name> <room_type>
  amity.py add_person <first_name> <last_name> <STAFF/FELLOW> [<wants_accommodation>]
  amity.py -h | --help

Examples:
  amity.py create_room Moon office
  amity.py create_room Cedar living
  amity.py add_person HASSAN OYEBOADE FELLOW N
  amity.py add_person SUNDAY NWUGURU FELLOW Y
  amity.py add_person PROSPER OTEMUYIWA STAFF


Options:
    -h, --help  Show this screen and exit.
"""
from model.docopt import docopt
from model.amity_model import Amity

if __name__ == '__main__':
  arguments = docopt(__doc__)
  if arguments['create_room']:
    Amity().create_room(arguments['<room_name>'],arguments['<room_type>'])
  if arguments['add_person']:
    Amity().add_person(arguments['<first_name>'], arguments['<last_name>'], arguments['<STAFF/FELLOW>'], arguments['<wants_accommodation>'])
  if arguments['print_allocations']:
    Amity().print_allocations()
    