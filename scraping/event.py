# -*- coding: utf-8 -*-
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
        ret_string = self.name + '\n' + str(self.starttime) + '---' + str(self.endtime) + '\n'
        ret_string = ret_string + unicode(self.location, errors='ignore')
        return ret_string
    
    def set_location(self, location):
        self.location = location
    
    