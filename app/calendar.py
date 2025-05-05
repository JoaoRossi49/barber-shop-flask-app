from googleapiclient.discovery import build
from .auth import authenticate_google_api
import datetime
import pytz

def convert_timezone(dates):
    tz_brasilia = pytz.timezone('America/Sao_Paulo')
    
    formatted_slots = []
    for slot in dates:
        start_time = slot[0].astimezone(tz_brasilia).strftime('%a, %d %b %Y %H:%M:%S GMT')
        end_time = slot[1].astimezone(tz_brasilia).strftime('%a, %d %b %Y %H:%M:%S GMT')
        formatted_slots.append([start_time, end_time])
    
    return formatted_slots

def create_event(calendar_id, summary, description, start_time, end_time, timezone="America/Sao_Paulo"):

    creds = authenticate_google_api()
    service = build('calendar', 'v3', credentials=creds)

    event = {
        "summary": summary,
        "description": description,
        "start": {
            "dateTime": start_time,
            "timeZone": timezone,
        },
        "end": {
            "dateTime": end_time,
            "timeZone": timezone,
        },
    }
    
    created_event = service.events().insert(calendarId=calendar_id, body=event).execute()
    return created_event

def get_free_slots(calendar_id, start_time, end_time, interval_minutes=15):

    creds = authenticate_google_api()
    service = build('calendar', 'v3', credentials=creds)

    body = {
        "timeMin": start_time,
        "timeMax": end_time,
        "timeZone": "America/Sao_Paulo",
        "items": [{"id": calendar_id}]
    }

    busy_slots = service.freebusy().query(body=body).execute()
    busy_times = busy_slots['calendars'][calendar_id].get('busy', [])

    busy_intervals = [
        (datetime.datetime.fromisoformat(slot['start']), datetime.datetime.fromisoformat(slot['end']))
        for slot in busy_times
    ]


    available_slots = []
    current_time = datetime.datetime.fromisoformat(start_time)

    while current_time + datetime.timedelta(minutes=interval_minutes) <= datetime.datetime.fromisoformat(end_time):
        slot_end = current_time + datetime.timedelta(minutes=interval_minutes)
        is_free = all(not (start <= current_time < end or current_time < start < slot_end) for start, end in busy_intervals)

        if is_free:
            available_slots.append((current_time, slot_end))

        current_time = slot_end

    return available_slots
