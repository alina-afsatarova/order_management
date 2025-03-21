import pytest

from orders.models import Item, Order


@pytest.fixture
def item_1():
    return Item.objects.create(
        name='Блюдо 1',
        price=100
    )


@pytest.fixture
def item_2():
    return Item.objects.create(
        name='Блюдо 2',
        price=100
    )


@pytest.fixture
def order(item_1):
    order = Order(id=1, table_number=1)
    order.save()
    order.items.add(item_1)
    return order


@pytest.fixture
def create_data(item_2):
    return {
        'table_number': 2,
        'items': [item_2.id]
    }


@pytest.fixture
def edit_data(item_2):
    return {
        'items': [item_2.id],
        'status': 'Done'
    }
