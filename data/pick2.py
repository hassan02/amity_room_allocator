try:
   import cPickle as pickle
except:
   import pickle
class Room(object):
    def __init__(self, name):
        self.name = name
        self.no_of_occupants = 0
        self.members = 'EMPTY'

room_name = raw_input('Room name: ')
room = Room(room_name)
with open('room_data.pkl', 'rb') as input:
    print room.name
    print room.no_of_occupants
    print room.members


try:
   import cPickle as pickle
except:
   import pickle
from StringIO import StringIO
out_s = StringIO()
class Room(object):
    def __init__(self, name):
        self.name = name
        self.no_of_occupants = 0
        self.members = 'EMPTY'


out_s = open('pickle_data.pkl', 'wb')

# Write to the stream
room3 = Room('Mache')
pickle.dump(room3, out_s)
room4 = Room('Iroko')
pickle.dump(room4, out_s)
# Set up a read-able stream
in_s = open('pickle_data.pkl', 'rb')

# Read the data
while True:
    try:
        room = pickle.load(in_s)
    except EOFError:
        break
    else:
        print '%s\n%s' % (room.name, room.members)
