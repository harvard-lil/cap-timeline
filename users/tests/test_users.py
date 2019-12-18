import pytest
from test_fixtures.fixtures import *  # noqa


def test_user(user):
    assert user.email


def test_superuser(superuser):
    assert superuser.is_staff
    assert superuser.is_superuser

