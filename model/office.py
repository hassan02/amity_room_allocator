from room import Room
class Office(Room):
    def __init__(self,room_name):
        super(Office, self).__init__(room_name)
        self.max_occupants = 6