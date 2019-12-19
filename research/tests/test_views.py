from test_fixtures.fixtures import *  # noqa

from django.urls import reverse


@pytest.mark.django_db
def test_years(client, timelinemeta):
    # getting back a good response with existing timeline
    response = client.get(reverse('get-years', args=[timelinemeta.slug]))
    assert response.status_code == 200
    # getting back a 404 if no timeline exists
    response = client.get(reverse('get-years', args=['slug-not-found']))
    assert response.status_code == 404
