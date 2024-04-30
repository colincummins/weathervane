class Subscriber:
#For individual recipients of Weathervanes
    
    def __init__(self,email='',zipcode=''):
        self.zipcode = zipcode
        self.email = email
    
    def __str__(self):
        return self.email + ' ' + self.zipcode