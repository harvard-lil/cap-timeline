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
    one_event = json.dumps(Event.objects.get(id=event_id).as_json())
    return HttpResponse(one_event, content_type='application/json')
