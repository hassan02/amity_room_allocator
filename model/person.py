class Person(object):
    def __init__(self, first_name, last_name):
        if isinstance(first_name, str) and isinstance(last_name, str):  
            self.fullname = (first_name + ' ' + last_name).upper()
            self.allocated = False
            self.room = ''
        else:
            raise Exception ('Please enter a valid name')