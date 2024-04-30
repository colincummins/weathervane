class Quote:
#For storing quote information

    def __init__(self,body='',author=''):
        self.body = body
        self.author = author
    
    def __str__(self):
        return self.body + '\n\n--' + self.author