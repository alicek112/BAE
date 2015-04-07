'''
Event object.

Created by Alice Kroutikova '15
'''
import datetime

class Event(object):
    name = ""
    starttime = datetime.datetime.now()
    endtime = datetime.datetime.now()
    location = ""
    
    def __init__(self, name, starttime, endtime, location):
        self.name = name 
        self.starttime = starttime
        self.endtime = endtime
        self.location = location 
    
    def __str__(self):
        return self.name + '\n' + str(self.starttime) + '---' + str(self.endtime) + '\n' + self.location
    
    