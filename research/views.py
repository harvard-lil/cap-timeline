import os
import json
from django.shortcuts import render
from django.http import HttpResponse

from research.models import Event, Group, Region
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
    related_events = []
    for relationship in event_obj.relationships.all():
        rel = relationship.preceding_event if relationship.succeeding_event == event_obj.id else relationship.succeeding_event
        related_events.append(rel.as_json())

    context = {
        'event': event_obj.as_json(),
        'related_events': related_events
    }
    return HttpResponse(json.dumps(context), content_type='application/json')


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


def groups(request):
    all_groups = Group.objects.values_list('slug', 'name').order_by('region__slug')
    return HttpResponse(json.dumps(list(all_groups)), content_type='application/json')


def groups_by_region(request):
    rgns = Region.objects.all().order_by('name')
    rg_list = []
    for rgn in rgns:
        grps = list(Group.objects.filter(region=rgn.id).order_by('region__slug').values('slug', 'name', 'region__name', 'region__slug'))
        rgn_obj = {
            'slug': rgn.slug,
            'name': rgn.name,
            'groups': grps
        }
        rg_list.append(rgn_obj)
    return HttpResponse(json.dumps(rg_list), content_type='application/json')
