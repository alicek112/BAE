'''
Visit sites to find athletic event information.

Creator: Alice Kroutikova '15
'''

import requests
from bs4 import BeautifulSoup
from urllib2 import urlopen

all_events = []

def dance():
    dance_url = 'http://arts.princeton.edu/academics/dance/co-curricular-offerings/'
    response = requests.get(dance_url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.text)
    
    sections = soup.select('div.page-mod')
    for s in sections:
        print s.find('h4').get_text()
        text = '\n'.join(s.select('p'))
        

        print '-----'
        
def oa():
    oa_url = 'https://outdooraction.princeton.edu/oa-calendar'

    response = requests.get(oa_url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.text)
    #print soup.prettify()
    sections = soup.select('div.item')
    
    for s in sections:
        
        # only want Climbing Wall events, not leader training
        if s.select('div[title~=Climbing]'):
            event = {}
            event['name'] = s.find('div', class_='views-field views-field-title').get_text()
            event['starttime'] = s.find('span', class_='date-display-start').attrs['content']
            event['endtime'] = s.find('span', class_='date-display-end').attrs['content']
            event['location'] = 'OA Climbing Wall - Princeton Stadium'
            all_events.append(event)
            print event
            print '----'

oa()
