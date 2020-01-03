import pytest
from test_fixtures.factories import *


@pytest.fixture
def user():
    return UserFactory()


# @pytest.fixture
# def staff_group():
#     group = GroupFactory()
#     group.name = 'staff'
#     group.save()
#     return group
#
#
# @pytest.fixture
# def staff_user(staff_group):
#     user = UserFactory()
#     user.is_staff = True
#     # user.save()
#     staff_group.save()
#     # group = GroupFactory(name='staff')
#     user.groups.add(staff_group)
#     return user


@pytest.fixture
def superuser():
    user = UserFactory()
    user.is_staff = True
    user.is_superuser = True
    return user


@pytest.fixture
def timelinemeta():
    meta = MetaFactory()
    return meta
