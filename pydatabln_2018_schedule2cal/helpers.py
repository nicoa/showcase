# -*- coding: utf-8 -*-
"""Helper Functions for PyData18 schedule2cal script."""

def get_cals(service, filter_list=False):
    """Get Calendar Items from API."""
    cals = service.calendarList().list().execute().get('items')
    if filter_list and isinstance(filter_list, list):
        cals = filter(lambda d: d['summary'] in filter_list, cals)
    return cals


def create_pydata_calendars(service,
                            calendar_list=[
                                'pydata_novice',
                                'pydata_intermediate',
                                'pydata_experienced']):
    """Create Calendars named as `calendar_list`."""
    cals = get_cals(service)
    new_cals = {}
    for summary in calendar_list:
        if summary in map(lambda d: d['summary'], cals):
            continue
        calendar = {'summary': summary, 'timeZone': 'Europe/Berlin'}

        created_calendar = service.calendars().insert(body=calendar).execute()
        new_cals[summary] = created_calendar['id']
    return new_cals


def reduce_to_summary(cals, is_dict=False):
    """Reduce calendar json for summarys or dict of summary:id pairs."""
    if is_dict:
        return {x['summary']: x['id'] for x in cals}
    else:
        return map(lambda d: d['summary'], cals)


def write_event(event, cals, service):
    """Write an event (pd.Series, row of df) to calendar."""
    events = service.events()
    CalID = filter(lambda d: event.level == d['summary'], cals)[0]['id']
    l = (
        events.list(
            calendarId=CalID,
            timeMin=event.start + '+02:00',
            timeMax=event.end + '+02:00',
            singleEvents=True).execute()['items']
    )
    if (len(l) != 0) and any(map(lambda d: d['summary'] == event.summary, l)):
        print("found existing event(s): '{}'".format(
            "', '".join(map(lambda d: d['summary'], l))))
        return False
    else:
        print('creating event {}'.format(event.summary))

    event = {
        'summary': event.summary,
        'location': event.location,
        'description': event.description,
        'start': {'dateTime': event.start, 'timeZone': 'Europe/Berlin'},
        'end': {'dateTime': event.end, 'timeZone': 'Europe/Berlin'},
        # 'organizer': [{'displayName': event.attendees}],  # didn't work
        'reminders': {'useDefault': False}
        # 'attendees': [{'email': 'YOUR@MAIL.com', 'sendNotifications': False}]
    }

    event = events.insert(calendarId=CalID, body=event).execute()
    return True