class Room(object):
    def __init__(self,name):
        self.setName(name)
        self.room_name = self.getName()
        self.members = {}
        self.no_of_occupants = 0
    def getName(self):
        return self.__name

    def setName(self, name):
        if isinstance(name, str):
            self.__name = name
        else:
            raise 'Invalid argument'