from __future__ import print_function
import httplib2
import os
from googleapiclient.discovery import build
from oauth2client import client, tools
from oauth2client.file import Storage
import sys
sys.path.insert(1, '/Library/Python/2.7/site-packages')


try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'apicalendar.json'
APPLICATION_NAME = 'Google Calendar API Python - Testowanie'

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join('./', '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,'user_data.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store, flags)
        print('Storing credentials to ' + credential_path)
    return credentials


def check(data):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = build('calendar', 'v3', http=http)

    #now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('10 najbliższych wydarzeń:')
    eventsResult = service.events().list(
        calendarId='primary', timeMin='{}T00:00:00+01:00'.format(data),timeMax='{}T23:59:59+01:00'.format(data), maxResults=50, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    if not events:
        print('Żadnych wydarzeń!')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])
def add(wydarzenie):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = build('calendar', 'v3', http=http)
    event = wydarzenie
    event = service.events().insert(calendarId='primary', body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))
def del1(wydarzenie):
    # usuwa pojedyńcze wydarzenie
    # w przypadku większej ilości wydarzeń kończy prace
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = build('calendar', 'v3', http=http)
    eventsResult = service.events().list(calendarId='primary').execute()
    events = eventsResult.get('items', [])
    licznik = 0
    if not events:
        print('Żadnych wydarzeń!')
        return 1
    for event in events:
        if event['summary']==wydarzenie.nazwa:
            licznik = licznik +1

    if licznik == 0:
        print("Nie ma takiego wydarzenia")
        return 1
    if licznik == 1:
        for event in events:
            if event['summary'] == wydarzenie.nazwa:
                eventID = event.get('id')
                service.events().delete(calendarId='primary', eventId=eventID).execute()
                return 2
    else:
        return 0
def del2(wydarzenie):
    #usuwa konkretne wydarzenie
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = build('calendar', 'v3', http=http)
    eventsResult = service.events().list(calendarId='primary').execute()
    events = eventsResult.get('items', [])
    if not events:
        print('Żadnych wydarzeń!')
        return 1
    for event in events:
        if event['summary'] == wydarzenie.nazwa and event['start'].get('dateTime') == "{}T{}+01:00".format(wydarzenie.data, wydarzenie.h_start):
            eventID = event.get('id')
            service.events().delete(calendarId='primary', eventId=eventID).execute()
            return 2

    return 1
def del3(wydarzenie):
    # usuwa wszystkie wydarzenia o danej nazwie
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = build('calendar', 'v3', http=http)
    eventsResult = service.events().list(calendarId='primary').execute()
    events = eventsResult.get('items', [])
    if not events:
        print('Żadnych wydarzeń!')
        return 1
    for event in events:
        if event['summary'] == wydarzenie.nazwa:
            eventID = event.get('id')
            service.events().delete(calendarId='primary', eventId=eventID).execute()

    return 2
def edit_jedno(nazwa,nowa_nazwa,nowa_data,nowa_h_start,nowa_data_koniec, nowa_h_koniec,nowy_opis, nowa_lokalizacja):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = build('calendar', 'v3', http=http)
    eventsResult = service.events().list(calendarId='primary').execute()
    events = eventsResult.get('items', [])
    for event in events:
        if event['summary'] == nazwa:
            # 1
            if nowa_nazwa == "":
                pass
                print(event['summary'])
            else:
                event['summary'] = nowa_nazwa
                print(event['summary'])

            # 2 data i godzina początkowa bez zmian
            if nowa_data == "" and nowa_h_start == "":
                pass

            if nowa_data == "":
                d = event['start'].get('dateTime')
                nowa_data = d[0:10]
                event['start.dateTime'] = "{}T{}+01:00".format(nowa_data, nowa_h_start)
                print(event['start.dateTime'])
            if nowa_data == "":
                h = event['start'].get('dateTime')
                nowa_h_start = h[11:19]
                event['start.dateTime'] = "{}T{}+01:00".format(nowa_data, nowa_h_start)
                print(event['start.dateTime'])
            else:
                event['start.dateTime'] = "{}T{}+01:00".format(nowa_data, nowa_h_start)
                print(event['start.dateTime'])
            # 3 data i godzina koncowa bez zmian
            if nowa_data_koniec == "" and nowa_h_koniec == "":
                pass

            if nowa_data_koniec == "":
                d = event['start'].get('dateTime')
                nowa_data_koniec = d[0:10]
                event['end.dateTime'] = "{}T{}+01:00".format(nowa_data_koniec, nowa_h_koniec)
                print(event['end.dateTime'])
            if nowa_data_koniec == "":
                h = event['start'].get('dateTime')
                nowa_h_koniec = h[11:19]
                event['end.dateTime'] = "{}T{}+01:00".format(nowa_data_koniec, nowa_h_koniec)
                print(event['end.dateTime'])
            else:
                event['end.dateTime'] = "{}T{}+01:00".format(nowa_data_koniec, nowa_h_koniec)
                print(event['end.dateTime'])

            # 4 nowy opis
            if nowy_opis == "":
                pass
            else:
                event['description'] = nowy_opis
                print(event['description'])

            # 5 nowa lokalizacja
            if nowy_opis == "":
                pass
            else:
                event['localization'] = nowa_lokalizacja

            p = service.events().update(calendarId='primary', eventId=event['id'], body=event).execute()
            print("Edytowano!")
            print(p)

def edit_konkret(nazwa, data, godzina, nowa_nazwa,nowa_data,nowa_h_start,nowa_data_koniec, nowa_h_koniec,nowy_opis, nowa_lokalizacja):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = build('calendar', 'v3', http=http)
    eventsResult = service.events().list(calendarId='primary').execute()
    events = eventsResult.get('items', [])
    for event in events:
        if event['summary'] == nazwa and event['start'].get('dateTime') == "{}T{}+01:00".format(data, godzina):
            # 1
            if nowa_nazwa == "":
                pass
                print(event['summary'])
            else:
                event['summary'] = nowa_nazwa
                print(event['summary'])

            # 2 data i godzina początkowa bez zmian
            if nowa_data == "" and nowa_h_start == "":
                pass

            if nowa_data == "":
                d = event['start'].get('dateTime')
                nowa_data = d[0:10]
                event['start.dateTime'] = "{}T{}+01:00".format(nowa_data, nowa_h_start)
                print(event['start.dateTime'])
            if nowa_data == "":
                h = event['start'].get('dateTime')
                nowa_h_start = h[11:19]
                event['start.dateTime'] = "{}T{}+01:00".format(nowa_data, nowa_h_start)
                print(event['start.dateTime'])
            else:
                event['start.dateTime'] = "{}T{}+01:00".format(nowa_data, nowa_h_start)
                print(event['start.dateTime'])
            # 3 data i godzina koncowa bez zmian
            if nowa_data_koniec == "" and nowa_h_koniec == "":
                pass

            if nowa_data_koniec == "":
                d = event['start'].get('dateTime')
                nowa_data_koniec = d[0:10]
                event['end.dateTime'] = "{}T{}+01:00".format(nowa_data_koniec, nowa_h_koniec)
                print(event['end.dateTime'])
            if nowa_data_koniec == "":
                h = event['start'].get('dateTime')
                nowa_h_koniec = h[11:19]
                event['end.dateTime'] = "{}T{}+01:00".format(nowa_data_koniec, nowa_h_koniec)
                print(event['end.dateTime'])
            else:
                event['end.dateTime'] = "{}T{}+01:00".format(nowa_data_koniec, nowa_h_koniec)
                print(event['end.dateTime'])

            # 4 nowy opis
            if nowy_opis == "":
                pass
            else:
                event['description'] = nowy_opis
                print(event['description'])

            # 5 nowa lokalizacja
            if nowy_opis == "":
                pass
            else:
                event['localization'] = nowa_lokalizacja

            p = service.events().update(calendarId='primary', eventId=event['id'], body=event).execute()
            print("Edytowano!")
            print(p)
def sprawdzam(nazwa):
    def checks(nazwa):
        credentials = get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = build('calendar', 'v3', http=http)
        eventsResult = service.events().list(calendarId='primary').execute()
        events = eventsResult.get('items', [])
        licznik = 0
        if not events:
            print('Żadnych wydarzeń!')
            return 0
        for event in events:
            if event['summary'] == nazwa:
                licznik = licznik + 1

        if licznik == 0:
            print("Nie ma takiego wydarzenia")
            return 0
        if licznik == 1:
            return 1
        else:
            return 2
    odp = checks(nazwa)
    return odp
def sprawdzam2(nazwa, data, godzina):
    def checks2(nazwa, data, godzina):
        credentials = get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = build('calendar', 'v3', http=http)
        eventsResult = service.events().list(calendarId='primary').execute()
        events = eventsResult.get('items', [])
        licznik = 0
        if not events:
            print('Żadnych wydarzeń!')
            return 0
        for event in events:
            if event['summary'] == nazwa and event['start'].get('dateTime') == "{}T{}+01:00".format(data, godzina):
                licznik = licznik + 1

        if licznik == 0:
            print("Nie ma takiego wydarzenia")
            return 0
        if licznik == 1:
            return 1

    odp = checks2(nazwa,data,godzina)
    return odp


#edit_jedno("przygoda","zabawa","","","","","","")

