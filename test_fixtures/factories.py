import pytest
import factory
from pytest_factoryboy import register
from django.contrib.auth.models import Group
from django.conf import settings
# from autoslug import AutoSlugField
from django.utils.text import slugify

from users.models import TimelineUser
from research.models import Meta as TimelineMeta, EventType


@register
class GroupFactory(factory.DjangoModelFactory):
    class Meta:
        model = Group
    id = factory.Sequence(lambda n: '%04d' % n)
    name = factory.Faker('name')


@register
@pytest.mark.django_db
class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = settings.AUTH_USER_MODEL

    id = factory.Sequence(lambda n: '%04d' % n)
    email = factory.Faker('email')
    password = factory.PostGenerationMethodCall('set_password', 'password')
    email_verified = True
    is_active = True
    is_staff = False
    is_superuser = False

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for group in extracted:
                self.groups.add(group)


@register
class MetaFactory(factory.DjangoModelFactory):
    class Meta:
        model = TimelineMeta
    title = factory.Faker('name')


@register
class EventTypeFactory(factory.DjangoModelFactory):
    class Meta:
        model = EventType
    name = factory.Faker('name')
