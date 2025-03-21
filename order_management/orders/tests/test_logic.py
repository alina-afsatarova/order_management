import pytest
from pytest_django.asserts import assertRedirects

from orders.models import Order
from .constants import CREATE_URL, INDEX_URL, REVENUE_URL


@pytest.mark.django_db
def test_create_order(client, create_form_data):
    initial_number_of_orders = Order.objects.count()
    response = client.post(CREATE_URL, data=create_form_data)
    assertRedirects(response, INDEX_URL)
    assert Order.objects.count() - initial_number_of_orders == 1
    new_order = Order.objects.get()
    assert new_order.table_number == create_form_data['table_number']
    for item in new_order.items.all():
        item.id in create_form_data['items']
    assert new_order.status == 'Waiting'


@pytest.mark.django_db
def test_edit_order(client, edit_url, edit_form_data, order):
    initial_table_number = order.table_number
    response = client.post(edit_url, data=edit_form_data)
    assertRedirects(response, INDEX_URL)
    order.refresh_from_db()
    assert order.table_number == initial_table_number
    for item in order.items.all():
        item.id in edit_form_data['items']
    assert order.status == edit_form_data['status']


@pytest.mark.django_db
def test_delete_order(client, delete_url):
    initial_number_of_orders = Order.objects.count()
    response = client.delete(delete_url)
    assertRedirects(response, INDEX_URL)
    assert initial_number_of_orders - Order.objects.count() == 1
