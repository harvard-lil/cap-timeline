import pytest
import factory
from pytest_factoryboy import register
from django.contrib.auth.models import Group
# from autoslug import AutoSlugField
from django.utils.text import slugify

from users.models import TimelineUser
from research.models import Meta as TimelineMeta


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
        model = TimelineUser

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
