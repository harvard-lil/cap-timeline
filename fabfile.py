import os
import json
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'timeline.settings')
try:
    django.setup()
except Exception as e:
    print("WARNING: Can't configure Django -- tasks depending on Django will fail:\n%s" % e)

from django.conf import settings
from research.models import Event, Meta

from fabric.decorators import task
from django.core import management


@task(alias='run')
def run_django(port="127.0.0.1:8000"):
    if os.environ.get('DOCKERIZED'):
        port = "0.0.0.0:8000"
    management.call_command('runserver', port)


@task
def create_json(timeline=None):
    """
    Creating json files for each timeline (or a single timeline if arg is passed in.
    """
    if not timeline:
        metas = Meta.objects.all()
        for meta in metas:
            create_json(timeline=meta.slug)
    else:
        events = Event.objects.select_related('image', 'weight').filter(
            hide=False, timeline=timeline).order_by(
            'start_date').prefetch_related(
            'citation')
        all_events = [event.as_json() for event in events]
        storage_dir = os.path.join(settings.DB_DIR, 'json')
        if not (os.path.exists(storage_dir)):
            os.mkdir(storage_dir)

        print("timeline:", timeline)

        filename = 'events-%s.json' % timeline if timeline else 'events.json'
        with open(os.path.join(storage_dir, filename), 'w+') as f:
            json.dump(all_events, f)
