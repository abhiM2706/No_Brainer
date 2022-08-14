import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from datetime import datetime, timedelta
import pprint
import datefinder
import time

SCOPES = ['https://www.googleapis.com/auth/calendar']

def initialize_calendar():
	creds=None
	if os.path.exists('token.json'):
		creds = Credentials.from_authorized_user_file('token.json', SCOPES)
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
			creds= flow.run_local_server (port=0)
		with open('token.json', 'w') as token:
			token.write(creds.to_json())
	service = build('calendar', 'v3', credentials=creds)

	return service


def create_event(start_time, end_time, summary, service, description=None, location=None, recurrence=1):
    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'colorId': None,
        'start': {
            'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': 'America/Los_Angeles',
        },
        'recurrence': [
    		f"RRULE:FREQ=DAILY;COUNT={recurrence}"
  		],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }
    return service.events().insert(calendarId='primary', body=event).execute()


def create_calendar(summary):
	calendar = {
	'summary' : summary,
	'timeZone' : 'America/Los_Angeles'
	}

	service.calendars().insert(body=calendar).execute()
	time.sleep(4)
	return get_calendar_id(summary)

def get_calendar_id(name):

	list_of_calendars = service.calendarList().list().execute()
	calendar_items = list_of_calendars['items']

	for items in calendar_items:
		if name == items['summary']:
			return items['id']

	print("Calendar NOT THERE!")





