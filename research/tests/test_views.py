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


@pytest.mark.django_db
def test_metas(client, timelinemeta):
    timelinemeta.published = False
    timelinemeta.save()

    response = client.get(reverse('get-metas'))
    assert response.status_code == 200
    assert response.json() == []

    timelinemeta.publish_meta()
    response = client.get(reverse('get-metas'))
    assert response.status_code == 200
    assert len(response.json()) == 1
    res = response.json()[0]
    assert res['slug'] == timelinemeta.slug
    assert res['title'] == timelinemeta.title
