import pytest
from django.utils.text import slugify
from test_fixtures.fixtures import *  # noqa

from research.models import Meta


@pytest.mark.django_db
def test_create_meta():
    title = "My New Timeline"
    meta = Meta.objects.create(title=title)
    assert meta.slug == slugify(title)

    # creates a unique slug the second time
    new_meta = Meta.objects.create(title=title)
    assert new_meta.slug is not slugify(title)


@pytest.mark.django_db
def test_publish(timelinemeta):
    assert not timelinemeta.published

    timelinemeta.publish_meta()
    assert timelinemeta.published


@pytest.mark.django_db
def test_unpublish(timelinemeta):
    timelinemeta.published = True
    timelinemeta.save()
    timelinemeta.unpublish_meta()
    assert not timelinemeta.published
