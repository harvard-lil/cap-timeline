import os
import json
from django.shortcuts import render
from django.http import HttpResponse

from research.models import Event
from timeline import settings


def index(request):
    print("hello index.html")
    return render(request, "index.html")


def events(request):
    with open(os.path.join(settings.DB_DIR, 'json/events.json'), 'r') as f:
        all_events = f.read()
    return HttpResponse(all_events, content_type='application/json')


def event(request, event_id):
    event_obj = Event.objects.get(id=event_id)
    one_event = json.dumps(event_obj.as_json())

    return HttpResponse(one_event, content_type='application/json')


def years(request):
    # get all active years
    all_events = Event.objects.filter(hide=False).order_by('start_date')
    all_years = set()
    # if an event takes several years, add all years between start year and end year
    for event_instance in all_events:
        if event_instance.end_date:
            years = range(event_instance.start_date.year, event_instance.end_date.year + 1)
            all_years = all_years.union(set(years))
        else:
            all_years.add(event_instance.start_date.year)

    return HttpResponse(json.dumps(sorted(all_years)), content_type='application/json')
