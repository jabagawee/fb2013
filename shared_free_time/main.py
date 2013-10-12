#! /usr/bin/env python

from datetime import datetime, timedelta
import re

from icalendar import Calendar, Event
from interval import IntervalSet
import requests

def coerce_to_ics(url):
    m = re.match(r"http://ninjacourses.com/schedule/export/schedule.ics\?s=(.*)&t=(.*) ", url)
    if m:
        return url
    m = re.match(r"http://ninjacourses.com/schedule/view/(.*)/\?t=(.*) ", url)
    if m:
        return "http://ninjacourses.com/schedule/export/schedule.ics?s=%s&t=%s" % m.groups()
    return False

def event_to_minutes(event):
    minutes = IntervalSet.between(0, 0)
    d = {"MO": 0, "TU": 1, "WE": 2, "TH": 3, "FR": 4}
    start, stop = event["DTSTART"].dt, event["DTEND"].dt
    for day in event["RRULE"]["BYDAY"]:
        b = d[day] * 1440 + start.hour * 60 + start.minute
        e = d[day] * 1440 + stop.hour * 60 + stop.minute
        minutes = minutes + IntervalSet.between(b, e)
    return minutes

if __name__ == "__main__":
    urls = []

    while True:
        url = raw_input("Enter a Ninja Courses URL here (enter '.' to stop): ")
        if url == '.':
            break
        url = coerce_to_ics(url)
        if url:
            urls.append(url)
        else:
            print "ERROR: Could not extract 's' and 't' from the provided URL"
            print "Make sure your URL is in the form http://ninjacourses.com/schedule/view/#######/?t=######## or http://ninjacourses.com/schedule/export/schedule.ics?s=#######&t=########"

    calendars = [Calendar.from_ical(requests.get(url).text) for url in urls]
    events = sum((calendar.walk() for calendar in calendars), [])
    events = [event for event in events if isinstance(event, Event) and "RRULE" in event]
    events = [event for event in events if event["RRULE"]["FREQ"] == ["WEEKLY"]]

    minutes = IntervalSet.between(0, 7200)
    for event in events[::-1]:
        minutes = minutes - event_to_minutes(event)

    dow = "Monday Tuesday Wednesday Thursday Friday".split()
    for interval in minutes:
        b, e = interval.lower_bound, interval.upper_bound
        b = datetime(2013, 10, 7, 0, 0) + timedelta(minutes=b)
        e = datetime(2013, 10, 7, 0, 0) + timedelta(minutes=e)
        print "You are all free from %s to %s!" % \
                (b.strftime("%a %I:%M %p"), e.strftime("%a %I:%M %p"))
