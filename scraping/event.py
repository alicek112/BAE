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
    info = ""
    category = ""
    
    '''
    Create an event with given name, start and end time, category and general information.
    '''
    def __init__(self, name, starttime, endtime, info, category):
        self.name = name 
        self.starttime = starttime
        self.endtime = endtime
        self.info = info
        self.category = category
    
    '''
    Format the event as a string.
    '''
    def __str__(self):
        ret_string = self.name + '\n' + str(self.starttime) + '---' + str(self.endtime) + '\n'
        if isinstance(self.info, unicode):
            ret_string = ret_string + self.info.encode('utf-8')
        else:
            try:
                ret_string = ret_string + self.info
            except UnicodeDecodeError:
                ret_string = ret_string + unicode(self.info, errors='ignore')
        ret_string = ret_string + '\n' + self.category
        return ret_string
    
    '''
    Set the extraneous information for the event.
    '''
    def set_info(self, info):
        self.info = info
    
    