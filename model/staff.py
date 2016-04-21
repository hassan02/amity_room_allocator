from person import Person 
class Staff(Person):
    def __init__(self, first_name, last_name):
        super(Staff, self).__init__(first_name,last_name)