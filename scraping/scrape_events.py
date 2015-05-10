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
import slate
import urllib2
from urllib2 import Request, urlopen
from StringIO import StringIO
from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run
import json
import MySQLdb as mdb

days_of_the_week = {'Mondays': MO, 'Tuesdays':TU, 'Wednesdays': WE, 'Thursdays':TH, 'Fridays':FR, 'Saturdays':SA, 'Sundays':SU}
ordered_days = ['Sundays', 'Mondays', 'Tuesdays', 'Wednesdays', 'Thursdays', 'Fridays', 'Saturdays']
headers = {'User-Agent': 'Mozilla/5.0'}

all_events = []

# Google Developers API key
cal_key = 'AIzaSyCKbcXTZ1vk_CzAwYLrvCFDiiLiVxoVtd8'

'''
HELPER FUNCTIONS
'''

'''
Returns the datetime of the last day of exams for the current semester.
'''
def get_end_of_semester():
    calendar_url = 'http://registrar.princeton.edu/events/'
    response = requests.get(calendar_url, headers=headers)
    soup = BeautifulSoup(response.text)
    
    date = datetime.datetime.now()
    for x in soup.select('div.category2.department1'):
        if 'Term examinations end' in x.get_text():
            for y in x.select('div.event_datelocation'):
                date = parse(y.get_text())
    return date

'''
Returns day of the week code from a string.
(Can determine that "wed" "WED", "Wednesday" and "Wednesdays" all mean the same day)
'''
def get_day_of_week(input):
    if not input:
        return None
    for d in days_of_the_week:
        if input.lower() in d.lower():
            return days_of_the_week[d]
    return None

'''
Given a recurring event's details (name, start and end dates and times, info and category)
and what days of the week it repeats (weekly), generates each instance of that
event and appends it to the list of all events.
'''
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
Splits text by a list of separators - adapted from Stackoverflow.com code
'''
def split(txt, seps):
    default_sep = seps[0]

    # skip seps[0] because that's the default seperator
    for sep in seps[1:]:
        txt = txt.replace(sep, default_sep)
    return txt.split(default_sep)

'''
SCRAPING FUNCTIONS
'''

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
                        if end_time < start_time:
                            new_hour = end_time.hour + 12
                            end_time = end_time.replace(hour=new_hour)
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
    info = 'Tango Club: ' + paragraphs[0].get_text()
    
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
        if re.search('\.pdf', href) and re.search('\d', link.get_text()):
            new_url = fitness_url + href
            
            # read in csv file
            csv_file = href[:-4] + '.csv' 
            csv_rows = []
            with open(csv_file, 'rU') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    csv_rows.append(row)
            
            start_date = None
            end_date = None
            day_of_week = days_of_the_week['Sundays']
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
                                
                                if name and 'no classes' in name.lower():
                                    last_time = start_time
                                    name = None
                                    info = ""
                                    if not start_date_set:
                                        start_date = None
                                    start_time = None
                                    end_time = None
                                    week_index += 1
                                    day_of_week = (days_of_the_week[ordered_days[week_index]])
                                
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
                                        cat = 'fitness'
                                        if 'yoga' in name.lower() or 'yoga' in info.lower():
                                            cat = 'yoga'
                                        
                                        make_weekly_events(name, start_date, end_date, start_time, end_time, day_of_week, info, cat)    
                                        
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
                                        cat = 'fitness'
                                        if 'yoga' in name.lower() or 'yoga' in info.lower():
                                            cat = 'yoga'
                                        make_weekly_events(name, start_date, end_date, start_time, end_time, day_of_week, info, cat)
                                        
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
                cat = 'fitness'
                if 'yoga' in name.lower() or 'yoga' in info.lower():
                    cat = 'yoga'
                if 'no classes' not in name.lower():
                    make_weekly_events(name, start_date, end_date, start_time, end_time, day_of_week, info, cat)

'''
Scrape the Dillon Gym facilities schedules.
'''
def facilities():
    dillon_url = 'http://www.princeton.edu/campusrec/dillon-gym/facility-schedules/'

    response = requests.get(dillon_url, headers=headers)
    soup = BeautifulSoup(response.text)
    links = soup.select('div.filename')
    
    # scrape each schedule that Dillon has on its website
    for l in links:
        if re.search('\d', l.get_text()) and 'TBD' not in l.get_text():
            dates = l.select('a')[0].get_text()
            start_date = parse(dates.split('-')[0], fuzzy=True)
            
            url = dillon_url + l.select('a')[0]['href']
            remoteFile = urlopen(Request(url)).read()
            memoryFile = StringIO(remoteFile)
            doc = slate.PDF(memoryFile)
        
            # separate schedule by all-caps category words: schedule[1] is everything after 'DILLON GYM', etc
            categories = ['DILLON GYM', 'STEPHENS FITNESS CENTER', 'DILLON POOL', 
                          'DILLON SQUASH COURTS', 'DILLON GYM MAIN FLOOR', 'CAMPUS RECREATION MAIN OFFICE',
                          'DENUNZIO POOL', 'JADWIN GYM INDOOR TENNIS COURTS', 'JADWIN GYM INDOOR TRACK']
            schedule = split(doc[0], categories)
            
            # parse through schedule of events
            # schedule[1] is Dillon Gym Hours
            get_facilities_hours(schedule[1].split(), 'Dillon Gym Open Hours', 'dillon', 'Dillon Gym', start_date)
            # parse fitness center hours
            get_facilities_hours(schedule[2].split(), 'Stephens Fitness Center Open Hours', 'stephens', 'Stephens Fitness Center', start_date)
            # parse Dillon Pool hours
            get_facilities_hours(schedule[3].split(), 'Dillon Pool Open Rec Swimming', 'swimming', 'Dillon Pool', start_date)
            # parse squash courts hours
            get_facilities_hours(schedule[4].split(), 'Dillon Squash Courts Hours', 'squash', 'Dillon Squash Courts', start_date)
            # parse Denunzio Pool hours
            get_facilities_hours(schedule[7].split(), 'Denunzio Pool Open Rec Swimming', 'swimming', 'Denunzio Pool', start_date)
            # parse Jadwin tennis hours
            get_facilities_hours(schedule[8].split(), 'Indoor Tennis Court Hours', 'tennis', 'Jadwin Gym Indoor Tennis Courts', start_date)
            # parse indoor track hours
            get_facilities_hours(schedule[9].split(), 'Indoor Track Hours', 'running', 'Jadwin Gym Indoor Track', start_date) 

'''
Parse individual facilities hours and add their hours as events.
'''
def get_facilities_hours(hours, name, category, info, start_date):
    my_date = start_date
    last_time = None
    for d in hours:
        if re.search('\d:', d):
            start_time = re.split('-|—', d)[0]
            end_time = re.split('-|—', d)[1]
            start_hr = int(re.split('[a|p]o*m', start_time.split(':')[0])[0])
            end_hr = int(re.split('[a|p]o*m', end_time.split(':')[0])[0])
            start_min = int(re.split('[a|p]o*m', start_time.split(':')[1])[0])
            end_min = int(re.split('[a|p]o*m', end_time.split(':')[1])[0])

            if 'p' in start_time:
                if start_hr < 12:
                    start_hr += 12
            if 'p' in end_time:
                if end_hr < 12:
                    end_hr += 12
            else:
                if end_hr == 12:
                    end_hr -= 12
            
            start = datetime.time(start_hr, start_min)
            end = datetime.time(end_hr, end_min)
            
            today = my_date
            start_datetime = datetime.datetime.combine(today, start)
            if end < start:
                today = my_date + relativedelta(days=1)
            end_datetime = datetime.datetime.combine(today, end)
            
            #update day of week
            if last_time:
                if start_datetime < last_time:
                    my_date = my_date + relativedelta(days=1)
                    start_datetime = start_datetime + relativedelta(days=1)
                    end_datetime = end_datetime + relativedelta(days=1)
                        
            last_time = end_datetime
            
            e = event.Event(name, start_datetime, end_datetime, info, category)
            all_events.append(e)
        
        # if calendar says "closed", update day
        if 'CLOSED' in d:
            my_date = my_date + relativedelta(days=1)

'''
Scrape the special Stephens Fitness Center events.
'''
def special_fitness():
    fitness_url = 'http://www.princeton.edu/campusrec/stephens-fitness-center/special-events/'
    
    response = requests.get(fitness_url, headers=headers)
    soup = BeautifulSoup(response.text)
    links = soup.select('div.filename')
    
    for l in links:
        title = l.select('a')[0].get_text()
        
        # '>' indicates this is an event link
        if '>' in title:
        
            url = fitness_url + l.select('a')[0]['href']
            text = ''
            
            # open the PDF to get information on the event
            try:
                remoteFile = urlopen(Request(url)).read()
                memoryFile = StringIO(remoteFile)
                doc = slate.PDF(memoryFile)
                text = doc[0]
            except urllib2.HTTPError:
                continue
            
            # parse event information
            name = title.split(':')[0]
            date = title.split(':')[1].split('>')[0]
            time = title.split(':')[1].split('>')[1]
            
            date_time = parse(date, fuzzy=True)
            
            start = time.split('to')[0]
            end = time.split('to')[1]
            start_hr = int(re.split('[a|p]m', start)[0])
            end_hr = int(re.split('[a|p]m', end)[0])
            
            if 'p' in start:
                start_hr += 12
            if 'p' in end:
                end_hr += 12
            
            starttime = datetime.datetime.combine(date_time, datetime.time(start_hr))
            endtime = datetime.datetime.combine(date_time, datetime.time(end_hr))
            
            e = event.Event(name, starttime, endtime, text, 'stephens')
            all_events.append(e)

'''
Scrape the Aikido Club website's scheduled events.
'''
def aikido():
    aikido_url = 'http://www.princeton.edu/~aikido/classes.html'
    response = requests.get(aikido_url, headers=headers)
    soup = BeautifulSoup(response.text)
    text = soup.select('div.text-right')[0]
    
    location = text.p.get_text()
    head = text.select('h3')
    start_date = datetime.datetime.today()
    end_date = get_end_of_semester()
    
    # for every event, parse the information inside
    for h in head:
        name = 'Aikido Class'
        category = 'martial'
        
        dates = h.get_text().split(',')
        weekly = (get_day_of_week(dates[0]),)
        
        times = dates[1].split('-')
        start_hr = int(times[0].split(':')[0]) + 12
        end_hr = int(times[1].split(':')[0]) + 12
        start_min = int(times[0].split(':')[1])
        end_min = int(times[1].split(':')[1])
        
        start = datetime.time(start_hr, start_min)
        end = datetime.time(end_hr, end_min)
        info = h.find_next().get_text() + '\n' + location
        
        make_weekly_events(name, start_date, end_date, start, end, weekly, info, category)

'''
Scrape the Dillon Gym's Noon Hoops events page.
'''
def basketball():
    basketball_url = 'http://www.princeton.edu/campusrec/informal-recreation/noon-hoops/'
    response = requests.get(basketball_url, headers=headers)
    soup = BeautifulSoup(response.text)
    section = soup.select('div.body')[0]
    text = section.get_text().strip()
    
    start_date = datetime.datetime.today()
    end_date = get_end_of_semester()
    
    name = text.split(' is held ')[0]
    info = text.split(' is held ')[1]
    time_info = location = info.split(' in ', 1)[0].split()
    location = info.split(' in ', 1)[1]
    
    # put together weekly information
    weekly = ()
    for t in time_info:
        day = get_day_of_week(t.strip(','))
        if day:
            weekly = weekly + (day,)
    
    # find start and end times
    start = None
    end = None
    for t in time_info:
        if re.search('\d', t):
            start_time = t.split('-')[0]
            end_time = t.split('-')[1]
            start_hr = int(re.split('[a|p]m', start_time.split(':')[0])[0])
            end_hr = int(re.split('[a|p]m', end_time.split(':')[0])[0])
            start_min = int(re.split('[a|p]m', start_time.split(':')[1])[0])
            end_min = int(re.split('[a|p]m', end_time.split(':')[1])[0])
            
            if 'p' in start_time:
                if start_hr < 12:
                    start_hr += 12
            if 'p' in end_time:
                if end_hr < 12:
                    end_hr += 12
            
            start = datetime.time(start_hr, start_min)
            end = datetime.time(end_hr, end_min)
            
    make_weekly_events(name, start_date, end_date, start, end, weekly, location, 'basketball')
 
'''
Scrape the Princeton Tiger Athletics webpage for home events.
'''   
def sports():
    sports_url = 'http://www.goprincetontigers.com/main/Schedule.dbml'
    response = requests.get(sports_url, headers=headers)
    soup = BeautifulSoup(response.text)
    # only interested in home games
    game = soup.select('tr.home')
    
    for g in game:
        
        # get date information
        date_info = g.select('td.date')[0].get_text().strip().split('-')
        date = parse(date_info[0].encode('ascii', errors='ignore'), fuzzy=True)
        end_date = None
        if len(date_info) > 1:
            end_date = parse(date_info[1].encode('utf-8'), fuzzy=True)
        name = g.select('td.team')[0].get_text().strip()
        name = name + ' vs. ' + g.select('td.opponent')[0].get_text().strip()
        name = re.sub(' \*', ' Conference Game', name)
        location = g.select('td.location')[0].get_text().strip()
        time = g.select('td.time')[0].get_text().strip()
        
        start_datetime = date
        end_datetime = date
        
        if re.search('\d', time):
            temp_time = time.split(' ')
            hr = int(temp_time[0].split(':')[0])
            min = int(temp_time[0].split(':')[1])
            if 'P' in temp_time[1]:
                if hr < 12:
                    hr += 12
            time = datetime.time(hr, min)
            start_datetime = datetime.datetime.combine(date, time)
            end_datetime = start_datetime + relativedelta(hours=2)
        
        list_of_start_dates = None
        if end_date:
            list_of_start_dates = list(rrule(DAILY, dtstart=start_datetime, until=end_date))
            list_of_end_dates = list(rrule(DAILY, dtstart=end_datetime, until=end_date))
        
        # if the event is multi-day, put all of them into event
        if list_of_start_dates:
            for s, e in zip(list_of_start_dates, list_of_end_dates):
                e = event.Event(name, s, e, location, 'watching')
                all_events.append(e)
        
        # if event is not multi-day, insert it into database:
        else:
            e = event.Event(name, start_datetime, end_datetime, location, 'watching')
            all_events.append(e)

'''
Scrape the Baker Ice Rink Google Calendar of open skating hours.
'''
def ice():  
    iceId = '59tmhsi6gspp713e2aa91i0ea88c5h6g@import.calendar.google.com'
    timeMin = datetime.datetime.now() - relativedelta(months=1)
    timeMin = timeMin.isoformat('T') + 'Z'
    
    # request JSON of all events in the calendar
    ice_url = 'https://www.googleapis.com/calendar/v3/calendars/' + iceId + '/events?singleEvents=true&timeMin=' + timeMin + '&key=' + cal_key
    response = requests.get(ice_url, headers=headers)
    j = response.json()
    
    category = 'skating'
    info = 'Free skating at Baker Ice Rink'
    for x in j['items']:
        end = parse(x['end']['dateTime'])
        start = parse(x['start']['dateTime'])
        name = x['summary']
        e = event.Event(name, start, end, info, category)
        all_events.append(e)

'''
Scrape the Swing Dancing Club for their weekly classes.
'''
def swing():  
    swing_url = 'http://swing.princeton.edu/announcements/'
    response = requests.get(swing_url, headers=headers)
    soup = BeautifulSoup(response.text)
    announcement = soup.select('article')[0]
    schedule = announcement.div.get_text().split('\n')
    heading = announcement.a.get_text()
    start_date = parse(announcement.time.get_text())
    
    # don't parse announcement if it's about a cancelled class
    if 'canceled' in heading.lower():
        return
    
    # announcements are either about tonight or tomorrow
    if 'tomorrow' in heading.lower():
        start_date = start_date + datetime.timedelta(days=1)
    
    info = None
    end_date = get_end_of_semester()
    category = 'dance'
    
    for s in schedule:
        if 'Come' in s:
            info = re.split('[A-Z][A-Z]', s)[0]
        if re.match('\d', s):
            details = s.split(' – '.decode('utf-8'))
            name = details[1]
            hours = details[0]
            
            start_time = None
            end_time = None
            
            if '-' in hours:
                start_time = int(hours.split('-')[0]) + 12
                end_time = int(hours.split('-')[1].split()[0]) + 12
            else:
                start_time = int(hours.split()[0]) + 12
                end_time = start_time + 1
            
            start_time = datetime.time(start_time, 0)
            end_time = datetime.time(end_time, 0)
            
            list_of_dates = list(rrule(WEEKLY, dtstart=start_date, until=end_date))
    
            for l in list_of_dates:
                day = l
                start_datetime = datetime.datetime.combine(day, start_time)
                
                # handle case of end time being on a different day
                if end_time < start_time:
                    day = day + relativedelta(days=+1)
                
                end_datetime = datetime.datetime.combine(day, end_time)
                e = event.Event(name, start_datetime, end_datetime, info, category)
                all_events.append(e)
    
 
oa()
dance()
fitness()
tango()
facilities()
special_fitness()
aikido()
basketball()
sports()
ice()
swing()

'''
for e in all_events:
    print e
    print ''

'''

# Insert each event into the database
con = mdb.connect('bae.cp0g2lykd7ui.us-east-1.rds.amazonaws.com', 'bae', 'bae333bae', 'bae333');

with con:
    
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS mainBae")
    cur.execute("CREATE TABLE mainBae(NAME VARCHAR(100), \
CATEGORY VARCHAR(100), START DATETIME, END DATETIME, INFO VARCHAR(1000), CANCELLED INTEGER, UPDATED INTEGER)")
    for e in all_events:
        name = e.name
        start = e.starttime
        end = e.endtime
        info = e.info
        cat = e.category
        cur.execute("INSERT INTO mainBae (NAME, CATEGORY, START, END, INFO, CANCELLED, UPDATED) VALUES (%s, %s, %s, %s, %s, 0, 0)", (name, cat, start, end, info))
