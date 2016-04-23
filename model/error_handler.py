class ErrorHandler():
    def __init__(self):
        pass
    def room_exist(self,room_name):
        print('Error. Room %s already exist'%(room_name.upper()))
    def no_available_room(self):
        print('Error. Room does not exist ')
