from person import Person 
class Fellow(Person):
    def __init__(self, first_name, last_name):
        super(Fellow, self).__init__(first_name,last_name)

#print simon.getName()
#print type(simon)