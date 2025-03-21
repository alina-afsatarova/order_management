from http import HTTPStatus

import pytest
from pytest_lazyfixture import lazy_fixture

from .constants import CREATE_URL, INDEX_URL, REVENUE_URL


@pytest.mark.django_db
@pytest.mark.parametrize(
    'url',
    (
        INDEX_URL,
        CREATE_URL,
        REVENUE_URL,
        lazy_fixture('detail_url'),
        lazy_fixture('edit_url'),
        lazy_fixture('delete_url'),
    )
)
def test_pages_availability(client, url):
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
