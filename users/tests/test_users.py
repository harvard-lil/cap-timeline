import pytest
from test_fixtures.fixtures import *  # noqa


@pytest.mark.django_db
def test_user(user):
    assert user.email


@pytest.mark.django_db
def test_superuser(superuser):
    assert superuser.is_staff
    assert superuser.is_superuser
