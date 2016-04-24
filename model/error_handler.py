class ErrorHandler():
    def __init__(self):
        pass
    def room_exist(self,room_name):
        print('Error. Room %s already exist'%(room_name.upper()))
    def no_available_room(self,room_type):
        print('Error. No available %s'%(room_type))
    def room_not_exist(self,room_name):
        print('Error. Room %s does not exist'%(room_name))
    def cannot_locate_file(self):
        print('Error. Cannot locate file')
