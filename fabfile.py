import os
import django

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

