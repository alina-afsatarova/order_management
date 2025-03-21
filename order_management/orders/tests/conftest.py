import pytest
from django.urls import reverse

from orders.models import Item, Order


@pytest.fixture
def item_1():
    return Item.objects.create(
        name='Блюдо 1',
        price=100
    )


@pytest.fixture
def order(item_1):
    order = Order(table_number=1)
    order.save()
    order.items.add(item_1)
    return order


@pytest.fixture
def detail_url(order):
    return reverse('orders:detail_order', args=(order.id,))


@pytest.fixture
def edit_url(order):
    return reverse('orders:edit_order', args=(order.id,))


@pytest.fixture
def delete_url(order):
    return reverse('orders:delete_order', args=(order.id,))


@pytest.fixture
def create_form_data(item_1):
    return {
        'table_number': 2,
        'items': [item_1.id,]
    }


@pytest.fixture
def item_2():
    return Item.objects.create(
        name='Блюдо 2',
        price=100
    )


@pytest.fixture
def edit_form_data(item_2):
    return {
        'items': [item_2.id,],
        'status': 'Done'
    }
