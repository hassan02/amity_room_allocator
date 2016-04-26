class Person(object):
  def __init__(self, firstname, lastname):
    self.setName(firstname,lastname)
    self.fullname = self.getName().upper()
    self.allocated = False
    self.room = ''

  
  def getName(self):
    return self.__firstname + ' ' + self.__lastname

  def setName(self, firstname, lastname):
    if isinstance(firstname, str):
      self.__firstname = firstname
      self.__lastname = lastname
    else:
      raise 'Invalid argument'

# simon = Person('Simon Peter')
# print simon.getName()