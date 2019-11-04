import os
import json
import django
from timeline import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'timeline.settings')
try:
    django.setup()
except Exception as e:
    print("WARNING: Can't configure Django -- tasks depending on Django will fail:\n%s" % e)

from fabric.decorators import task
from django.core import management


@task(alias='run')
def run_django(port="127.0.0.1:8000"):
    if os.environ.get('DOCKERIZED'):
        port = "0.0.0.0:8000"
    management.call_command('runserver', port)


@task
def create_json():
    from research.models import Event
    events = Event.objects.select_related('image', 'weight').filter(hide=False).order_by('start_date').prefetch_related('citation')

    all_events = [event.as_json() for event in events]
    storage_dir = os.path.join(settings.DB_DIR, 'json')
    with open(os.path.join(storage_dir, 'events.json'), 'w+') as f:
        json.dump(all_events, f)
