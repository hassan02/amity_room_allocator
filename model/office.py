from room import Room


class Office(Room):
    """ This class creates a new office and inherits from Room"""

    def __init__(self, room_name):
        """initializes a new office & inherit from the super class Room"""
        super(Office, self).__init__(room_name)
        self.room_type = 'office'
        self.max_occupants = 6
