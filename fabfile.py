import os
import json
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'timeline.settings')
try:
    django.setup()
except Exception as e:
    print("WARNING: Can't configure Django -- tasks depending on Django will fail:\n%s" % e)

from research.models import Meta

from fabric.decorators import task
from django.core import management


@task(alias='run')
def run_django(port="127.0.0.1:8000"):
    """
    Run django server
    """
    if os.environ.get('DOCKERIZED'):
        port = "0.0.0.0:8000"
    management.call_command('runserver', port)


@task
def create_json(timeline=None):
    """
    Creating json files for each timeline (or a single timeline if arg is passed in.
    For a single timeline:
    `fab create_json:timeline='single-timeline-slug'`
    """
    if timeline:
        meta = Meta.objects.get(slug=timeline)
        meta.publish_all_data_for_timeline()
    else:
        Meta.publish_all_datas()


@task
def create_meta(timeline=None):
    """
    Creating timeline meta data json.
    For a single timeline:
    `fab create_meta:timeline='single-timeline-slug'`
    """
    if timeline:
        meta = Meta.objects.get(slug=timeline)
        meta.publish_meta()
    else:
        Meta.publish_all_metas()

