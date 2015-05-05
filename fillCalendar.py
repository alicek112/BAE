import MySQLdb as mdb
import gflags
import httplib2
from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import OAuth2WebServerFlow
from oauth2client import tools
from oauth2client.tools import run_flow
import dateutil.tz
import datetime
from time import sleep

con = mdb.connect('bae.cp0g2lykd7ui.us-east-1.rds.amazonaws.com', 'bae', 'bae333bae', 'bae333');

cur = con.cursor()
cur.execute("SELECT NAME, CATEGORY, START, END, INFO FROM mainBae")
sql = cur.fetchall()

api_key = 'AIzaSyB0Bkaiq-6XynXNkw3yF9RHwHQ-_nh0W7o'

scope = 'https://www.googleapis.com/auth/calendar'
flow = OAuth2WebServerFlow('765641061823-7n5t3tdc46foqbef4c18eg1a8o6qjh61.apps.googleusercontent.com', 't5zK6t77HqfMNe-HUs3roWP_', scope)

storage = Storage('credentials.dat')
credentials = storage.get()
if credentials is None or credentials.invalid:
    flags = tools.argparser.parse_args(args=[])
    credentials = run_flow(flow, storage, flags)
http = httplib2.Http()
http = credentials.authorize(http)
service = build('calendar', 'v3', http=http, developerKey=api_key)

calIds = {'swimming': 'm7o1o5mddl6k144tfa0pmr8qd0@group.calendar.google.com',
          'skating': 'ias81kgc0r65c11oaj9ej7isg0@group.calendar.google.com',
          'watching': 'ehjrk0u8tnh7kitqeiu99c4vvg@group.calendar.google.com',
          'basketball': '3lvjeo9eja24trl9pnpsehhvm0@group.calendar.google.com',
          'martial': 'jfigilibb4pu9gurdcio7lamgc@group.calendar.google.com',
          'stephens': '0dnm92i7oa3fatu6rjt1dcbp2s@group.calendar.google.com',
          'dillon': '6qqd4mnu46umvg5q3nhoc5f3u0@group.calendar.google.com',
          'squash': 'a9s6ce6dtdcofhoohqovlsin5c@group.calendar.google.com',
          'tennis': 'qorqcfsaer8jhg29getvkbgo98@group.calendar.google.com',
          'running': 'cgaium65cu3sntgss95q6lr9kc@group.calendar.google.com',
          'fitness': 'jesqo5amcti7dumbkfqgl8k8vk@group.calendar.google.com',
          'oa': 'g066rcpl6cdiae0mau3od61a84@group.calendar.google.com',
          'dance': '8rdpbfb68003o3pe9evht802ss@group.calendar.google.com',
          'biking': '4hi03tl4aqjbftg4cgs76copk0@group.calendar.google.com',
          'yoga': 'h0emak3aebi1bp9m1ddbug7uck@group.calendar.google.com'}

#calIds = {'basketball': 'qa37h9n8loa5tt9s11v1bfk5is@group.calendar.google.com'}

localtz = dateutil.tz.tzlocal()
localoffset = localtz.utcoffset(datetime.datetime.now(localtz))
offset = int(localoffset.total_seconds() / 3600)

# clear all calendars
for cal in calIds:
    page_token = None
    while True:
      events = service.events().list(calendarId=calIds[cal], pageToken=page_token).execute()
      for event in events['items']:
        service.events().delete(calendarId=calIds[cal], eventId=event['id']).execute()
      page_token = events.get('nextPageToken')
      if not page_token:
        break


print 'finished deleting'

for s in sql:
    event = {
      'summary': s[0].replace('\xac', '').replace('\xe5\xa8', ''),
      'location': s[4].replace('\xac', '').replace('\xe5\xa8', ''),
      'start': {
        'dateTime': s[2].isoformat() + '-0' + str(offset)[1:] + ':00'
        },
      'end': {
        'dateTime': s[3].isoformat() + '-0' + str(offset)[1:] + ':00'
        }
    }
    print event
    
    if s[1] in calIds:
        created_event = service.events().insert(calendarId=calIds[s[1]], body=event).execute()
