from room import Room
class Living(Room):
  def __init__(self,room_name):
    super(Living, self).__init__(room_name)
    self.max_occupants = 4