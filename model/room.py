class Room(object):
    def __init__(self, name):
        if isinstance(name, str) and len(name) <= 30:
            self.name = name
        else:
            raise Exception('Invalid name. Room name must be string and be less than 40 characters.')
        self.members = {}
        self.no_of_occupants = len(self.members)
