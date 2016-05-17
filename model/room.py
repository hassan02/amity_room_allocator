class Room(object):
    """Create a new room object"""

    def __init__(self, name):
        """Set default properties and check for name validity"""
        if type(name) == str and len(name) <= 30:
            self.name = name
            self.members = {}
            self.no_of_occupants = len(self.members)
        else:
            raise Exception('Invalid name. Room name must be string and \
                            not more than 30 characters.')
