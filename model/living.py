from room import Room


class Living(Room):
    """ This class creates a new living space and inherits from Room class"""

    def __init__(self, room_name):
        """Initializes a new living space & inherit from the super class Room"""
        super(Living, self).__init__(room_name)
        self.room_type = 'living'
        self.max_occupants = 4
