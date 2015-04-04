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
    for s in sections:
        class_type = s.find('h4').get_text()
        
        for subclass in s.select('p'):
            name = ''
            end_date = get_end_of_semester()
            
            for x in subclass:
                if "Begins" in x:
                    start_date = parse(x[7:].encode('utf-8'), fuzzy=True)
                
                elif x.name == 'strong':
                    name = x.get_text() + ' ' + class_type
                
                elif ':' in x:
                    dates = x.split(':')[0].split(' ')
                    weekly = ()
                    for d in dates:
                        d = re.sub('[^a-zA-Z0-9]', '', d)
                        if d in days_of_the_week:
                            new_tuple = (days_of_the_week[d],)
                            weekly = weekly + new_tuple
                    list_of_dates = list(rrule(WEEKLY, dtstart=start_date, until=end_date, byweekday=weekly))
                    print start_date
                    print ' '
            
                    for l in list_of_dates:
                        print str(l)
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
