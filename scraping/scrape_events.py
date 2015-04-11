# -*- coding: utf-8 -*-
'''
Visit sites to find athletic event information.

Creator: Alice Kroutikova '15
'''

import requests
import event
from bs4 import BeautifulSoup
from dateutil.parser import *
from dateutil.rrule import *
from dateutil.relativedelta import *
import datetime
import re
import csv

days_of_the_week = {'Mondays': MO, 'Tuesdays':TU, 'Wednesdays': WE, 'Thursdays':TH, 'Fridays':FR, 'Saturdays':SA, 'Sundays':SU}
ordered_days = ['Mondays', 'Tuesdays', 'Wednesdays', 'Thursdays', 'Fridays', 'Saturdays', 'Sundays']
headers = {'User-Agent': 'Mozilla/5.0'}

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

'''
Returns day of the week code from a string.
'''
def get_day_of_week(input):
    if not input:
        return None
    for d in days_of_the_week:
        if input.lower() in d.lower():
            return days_of_the_week[d]
    return None

'''
Scrapes the dance department website for dance events.
'''
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
        
        for s in subclass.select('p'):
            
            text = str(s).split('\n')
            
            # analyze each event one by one
            my_events = []
            for x in text:
                list_of_dates = []
                has_start_time = False
                start_time = datetime.time(0, 0)
                end_time = datetime.time(0, 0)
                
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
                                start_time = exacttime
                            else:
                                end_time = exacttime
                    
                    for l in list_of_dates:
                        start_datetime = datetime.datetime.combine(l, start_time)
                        end_datetime = datetime.datetime.combine(l, end_time)
                        e = event.Event(name, start_datetime, end_datetime, '', 'dance')
                        my_events.append(e)
                elif my_events:
                    location = re.sub('<.*?>', '', x)
                    for e in my_events:
                        e.set_info(location)
                        all_events.append(e)
                        
'''
Scrape the Tango Club website's homepage.
'''
def tango():   
    dance_url = 'http://www.princeton.edu/~tango/index.shtml'
    response = requests.get(dance_url, headers=headers)
    soup = BeautifulSoup(response.text)
    
    section = soup.select('td.left')[0]
    
    # first paragraph contains both the start date and general information
    paragraphs = section.select('p')
    start_date = parse(paragraphs[0].get_text(), fuzzy=True)
    end_date = get_end_of_semester()
    info = paragraphs[0].get_text()
    
    # parse through list of scheduled events
    list = section.select('li')
    for l in list:
        name = l.get_text().rsplit(':', 1)[1]
        times = l.get_text().rsplit(':', 1)[0].split('-')
        
        start_times = re.split('\.|:', times[0])
        start_hr = int(re.split('[p|a]m', start_times[0])[0])
        start_min = 0
        if len(start_times) > 1:
            start_min = int(re.split('[p|a]m', start_times[1])[0])
        end_times = re.split('\.|:', times[1])
        end_hr = int(re.split('[p|a]m', end_times[0])[0])
        end_min = 0
        if len(end_times) > 1:
            end_min = int(re.split('[p|a]m', end_times[1])[0])
        
        if 'pm' in times[1]:
            start_hr += 12
            end_hr += 12
        if 'pm' in times[0]:
            start_hr += 12
        if 'am' in times[1] and end_hr == 12:
            end_hr -= 12       
        
        start_time = datetime.time(start_hr, start_min)
        end_time = datetime.time(end_hr, end_min)
        make_weekly_events(name, start_date, end_date, start_time, end_time, None, info, 'dance')
                  

'''
Scrape the OA website for climbing wall information.
'''        
def oa():
    oa_url = 'https://outdooraction.princeton.edu/oa-calendar'

    response = requests.get(oa_url, headers=headers)
    soup = BeautifulSoup(response.text)
    #print soup.prettify()
    sections = soup.select('div.item')
    
    for s in sections:
        
        # only want Climbing Wall events, not leader training
        if s.select('div[title~=Climbing]'):
            name = s.find('div', class_='views-field views-field-title').get_text()
            starttime = parse(s.find('span', class_='date-display-start').attrs['content'])
            endtime = parse(s.find('span', class_='date-display-end').attrs['content'])
            info = 'OA Climbing Wall - Princeton Stadium'
            e = event.Event(name, starttime, endtime, info, 'oa')
            all_events.append(e)


def make_weekly_events(name, start_date, end_date, start_time, end_time, weekly, info, category):
    list_of_dates = list(rrule(WEEKLY, dtstart=start_date, until=end_date, byweekday=weekly))
    
    for l in list_of_dates:
        day = l
        start_datetime = datetime.datetime.combine(day, start_time)
        
        # handle case of end time being on a different day
        if end_time < start_time:
            day = day + relativedelta(days=+1)
        
        end_datetime = datetime.datetime.combine(day, end_time)
        e = event.Event(name, start_datetime, end_datetime, info, category)
        all_events.append(e)

'''
Scrape the Dillon PDF Fitness schedules
'''
def fitness():
    fitness_url = 'http://www.princeton.edu/campusrec/instructional-programs/schedules-1/'
    
    response= requests.get(fitness_url, headers=headers)
    soup = BeautifulSoup(response.text)
    
    for link in soup.findAll('a', href=True):
        href = link['href']
        
        # find all the pdf-schedules on the page, load their csvs and analyze:
        if re.search('\.pdf', href):
            new_url = fitness_url + href
            
            # read in csv file
            csv_file = href[:-4] + '.csv' 
            csv_rows = []
            with open(csv_file, 'rb') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    csv_rows.append(row)
            
            start_date = None
            end_date = None
            day_of_week = (days_of_the_week['Sundays'],)
            week_index = 0
            start_time = None
            end_time = None
            name = None
            info = ""
            start_date_set = False
            time_first = True
            first_element = True
            last_time = None
            day_changed = False
            
            # check if there is a date range in the text of the link
            if re.search("\d/\d+", link.get_text()):
                dates = link.get_text().split()[0]
                start_date = parse(dates.split('-')[0], fuzzy=True)
                end_date = parse(dates.split('-')[1], fuzzy=True) 
                start_date_set = True    
            
            #parse csv file    
            for i in range(20):
                for row in csv_rows:
                    if len(row) > i:
                        this_element = re.sub('\r', '\n', row[i])
                        
                        # loop through lines one by one, identifying parts of event
                        if this_element:
                            lines = this_element.split('\n')
                            
                            # determine if events start with times or not (if it's a short element, it's a time)
                            if first_element:
                                if len(lines) > 3:
                                    time_first = False
                                first_element = False
                            
                            for line in lines:
                                
                                # check if this line is a date (if so, and if no start date, update start date)
                                if re.search('\d+/\d+', line):
                                    if not start_date_set:                                            
                                        match = re.search('\d+/\d+', line)
                                        start_date = parse(line[match.start():match.end()], fuzzy=True)
                                
                                # check if this line is a day of the week (if so, update day of week)
                                new_line = re.split(' |,', line)[0]
                                possible_days = new_line.split('/')
                                if get_day_of_week(possible_days[0]):
                                    day_changed = True
                                    day_of_week = ()
                                    for d in possible_days:
                                        day_of_week = day_of_week + (get_day_of_week(d),)
                                
                                # check if this line is time (has numbers and am/pm)
                                elif re.search('\d.*[a|p]m', line):
                                    # check if time already exists and if so, make a new set of events
                                    if time_first and start_time:
                                        if last_time:
                                            # if start time changes over but day hasn't changed, update day
                                            if start_time < last_time and not day_changed:
                                                week_index += 1
                                                day_of_week = (days_of_the_week[ordered_days[week_index]])
                                        
                                        # make new set of events
                                        make_weekly_events(name, start_date, end_date, start_time, end_time, day_of_week, info, 'fitness')
                                        
                                        last_time = start_time
                                        name = None
                                        info = ""
                                        if not start_date_set:
                                            start_date = None
                                        start_time = None
                                        end_time = None
                                    
                                    
                                    start = line.split('-')[0].split(':')
                                    end = line.split('-')[1].split(':')
                                    
                                    start_hr = int(re.split('[a|p]m', start[0])[0])
                                    start_min = 0
                                    end_hr = int(re.split('[a|p]m', end[0])[0])
                                    end_min = 0
                                    if len(start) > 1:
                                        start_min = int(re.split('[a|p]m', start[1])[0])
                                    if len(end) > 1:
                                        end_min = int(re.split('[a|p]m', end[1])[0])
                                    
                                    if 'pm' in line:
                                        if end_hr < 12:
                                            if start_hr < 12:
                                                start_hr += 12
                                            end_hr += 12
                                    
                                    start_time = datetime.time(start_hr, start_min)
                                    end_time = datetime.time(end_hr, end_min)
                                
                                # check if this line has "week" in it (if so, update end date)
                                elif 'week' in line:
                                    num_weeks = int(line.split('week')[0])
                                    end_date = start_date + relativedelta(weeks=+num_weeks)
                                    
                                    if not time_first:
                                        make_weekly_events(name, start_date, end_date, start_time, end_time, day_of_week, info, 'fitness')
                                        name = None
                                        info = ""
                                        start_time = None
                                        end_time = None
                                        end_date = None
                                
                                # check if no name, if so the next line is name
                                elif not name:
                                    name = line
                                
                                # rest of the information is "info"
                                else:
                                    info = info + ' ' + line
                               
            # whatever is remaining is an event
            if name and start_date and start_time:
                make_weekly_events(name, start_date, end_date, start_time, end_time, day_of_week, info, 'fitness')

oa()
dance()
fitness()
tango()

for e in all_events:
    print e
    print ''
