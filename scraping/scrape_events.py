# -*- coding: utf-8 -*-
'''
Visit sites to find athletic event information.

Creator: Alice Kroutikova '15
'''

import requests
import event
from bs4 import BeautifulSoup
from urllib2 import urlopen
from dateutil.parser import *
from dateutil.rrule import *
import datetime
import re
from Carbon.Aliases import false

days_of_the_week = {'Mondays': MO, 'Tuesdays':TU, 'Wednesdays': WE, 'Thursdays':TH, 'Fridays':FR, 'Saturdays':SA, 'Sundays':SU}

all_events = []

'''
Returns the datetime of the last day of exams for the current semester.
'''
def get_end_of_semester():
    calendar_url = 'http://registrar.princeton.edu/events/'
    response = requests.get(calendar_url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.text)
    
    date = datetime.datetime.now()
    for x in soup.select('div.category2.department1'):
        if 'Term examinations end' in x.get_text():
            for y in x.select('div.event_datelocation'):
                date = parse(y.get_text())
    return date

def dance():
    dance_url = 'http://arts.princeton.edu/academics/dance/co-curricular-offerings/'
    response = requests.get(dance_url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.text)
    
    sections = soup.select('div.page-mod')
    
    for subclass in sections:
        class_type = subclass.find('h4').get_text()
        
        has_start_date = False
        start_date = datetime.datetime.now()
        name = ''
        end_date = get_end_of_semester()
        list_of_dates = []
        has_start_time = False
        
        for s in subclass.select('p'):
            
            text = str(s).split('\n')
            
            # analyze each event one by one
            for x in text:
                # set start date for this set of events
                if not has_start_date:
                    if "Begins" in x:
                        date = re.sub('<.*?>', '', x)
                        start_date = parse(date[7:], fuzzy=True)
                        has_start_date = True
                
                # analyze the event
                if 'strong' in x:
                    name = re.sub('<.*?>', '', x) + ' ' + class_type

                elif ':' in x: 
                    # calculate the weekly dates from start date to end date
                    dates = x.split(':')[0].split(' ')
                    weekly = ()
                    for d in dates:
                        d = re.sub('[^a-zA-Z0-9]', '', d)
                        if d in days_of_the_week:
                            new_tuple = (days_of_the_week[d],)
                            weekly = weekly + new_tuple
                    list_of_dates = list(rrule(WEEKLY, dtstart=start_date, until=end_date, byweekday=weekly))
                    
                    # calculate times
                    times = x.split(' ')
                    for t in times:
                        if any(i.isdigit() for i in t):
                            exacttime = datetime.time(int(t.split(':')[0]), int(t.split(':')[1]))
                            if not has_start_time:
                                has_start_time = True
                                start_date = datetime.datetime.combine(start_date.date(), exacttime)
                            else:
                                end_date = datetime.datetime.combine(end_date.date(), exacttime)
                    
                    print list_of_dates       
                    print start_date
                    print end_date
                    print '###'
                   
            print '-----'

        print '%%%%%%%%%%%%%%%%%%%%%%%%%%' 
                  

'''
Scrape the OA website for climbing wall information.
'''        
def oa():
    oa_url = 'https://outdooraction.princeton.edu/oa-calendar'

    response = requests.get(oa_url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.text)
    #print soup.prettify()
    sections = soup.select('div.item')
    
    for s in sections:
        
        # only want Climbing Wall events, not leader training
        if s.select('div[title~=Climbing]'):
            name = s.find('div', class_='views-field views-field-title').get_text()
            starttime = parse(s.find('span', class_='date-display-start').attrs['content'])
            endtime = parse(s.find('span', class_='date-display-end').attrs['content'])
            location = 'OA Climbing Wall - Princeton Stadium'
            e = event.Event(name, starttime, endtime, location)
            all_events.append(e)
            print e
            print '----'

#oa()
dance()
