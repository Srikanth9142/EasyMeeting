from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file,client,tools

try:
    import argparse
    flags   =   argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/calender'
store = file.Storage('storage.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json',SCOPES)
    creds = tools.run_flow(flow,store,flags) \
             if flags else tools.run(flow,store)
CAL = build('calender','v3',http=creds.authorize(Http()))

GMT_OFF = '+05:30'
EVENT = {
    'summary':'Dinner with friends',
    'start':{'dateTime':'2019-02-08T15:30:00%s' % GMT_OFF},
    'end':{'dateTime':'2019-02-08T15:45:00%s' % GMT_OFF},
    'attendees':[
        {'email':'17pa1a05f1@vishnu.edu.in'},
        {'email':'17pa1a0577@vishnu.edu.in'}
    ],
}

e = CAL.events().insert(calenderId='primary',sendNotifications=True,body=EVENT).execute()

print('''*** %r event added:
 start: %s
 End: %s''' %(e['summary'].encode('utf-8'),
               e['start']['dateTime'],e['end']['dateTime']))