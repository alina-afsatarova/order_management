import pytest
from pytest_lazyfixture import lazy_fixture

from orders.forms import CreateOrderForm, UpdateOrderForm
from .constants import CREATE_URL, INDEX_URL, REVENUE_URL


@pytest.mark.django_db
def test_order_in_list(client, order):
    response = client.get(INDEX_URL)
    object_list = response.context['object_list']
    assert order in object_list


@pytest.mark.django_db
def test_revenue_context(client):
    response = client.get(REVENUE_URL)
    paid_orders = response.context.get('paid_orders')
    revenue = response.context.get('revenue')
    assert paid_orders is not None
    assert revenue is not None


@pytest.mark.django_db
@pytest.mark.parametrize(
    'url, form',
    (
        (CREATE_URL, CreateOrderForm),
        (lazy_fixture('edit_url'), UpdateOrderForm),
    )
)
def test_pages_contains_form(client, url, form):
    response = client.get(url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], form)
