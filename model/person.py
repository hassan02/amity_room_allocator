class Person(object):
    """Create a new person object"""

    def __init__(self, first_name, last_name):
        """Set default properties for person object"""
        if (type(first_name) and type(last_name) == str) and \
            len(first_name + ' ' +last_name) <= 50:  
            self.fullname = (first_name + ' ' + last_name).upper()
            self.office_allocated = False
            self.office = ''
            self.living_allocated = False
            self.living = ''
        else:
            raise Exception ('Please enter a valid name')