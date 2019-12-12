import pytest
from django.utils.text import slugify

from research.models import Meta


@pytest.mark.django_db
def test_create_meta():
    title = "My New Timeline"
    meta = Meta.objects.create(title=title)
    assert meta.slug == slugify(title)

    # creates a unique slug the second time
    new_meta = Meta.objects.create(title=title)
    assert new_meta.slug is not slugify(title)

