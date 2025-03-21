from http import HTTPStatus

import pytest

from orders.models import Order


@pytest.mark.django_db
class TestOrdersAPI:

    orders_url = '/api/orders/'
    orders_detail_url = '/api/orders/{id}/'
    revenue_url = '/api/orders/revenue/'

    def check_fields(self, response_data):
        expected_fields = (
            'id', 'table_number', 'items', 'status', 'total_price'
        )
        for field in expected_fields:
            assert field in response_data

    def test_get_orders_list(self, client, order):
        response = client.get(self.orders_url)
        assert response.status_code == HTTPStatus.OK
        response_data = response.json()
        assert isinstance(response_data, list)
        assert len(response_data) == Order.objects.count()
        self.check_fields(response_data[0])

    def test_get_orders_detail(self, client, order):
        response = client.get(self.orders_detail_url.format(id=order.id))
        assert response.status_code == HTTPStatus.OK
        response_data = response.json()
        assert isinstance(response_data, dict)
        self.check_fields(response_data)

    def test_order_create_with_invalid_data(self, client):
        orders_count = Order.objects.count()
        response = client.post(self.orders_url, data={})
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert orders_count == Order.objects.count()

    def test_order_create(self, client, create_data):
        orders_count = Order.objects.count()
        response = client.post(self.orders_url, data=create_data)
        assert response.status_code == HTTPStatus.CREATED
        assert Order.objects.count() - orders_count == 1
        response_data = response.json()
        assert isinstance(response_data, dict)
        self.check_fields(response_data)
        assert response_data['table_number'] == create_data['table_number']
        for item in response_data['items']:
            item in create_data['items']
        assert response_data['status'] == 'Waiting'

    def test_order_edit(self, client, order, edit_data):
        response = client.patch(
            self.orders_detail_url.format(id=order.id),
            data=edit_data,
            content_type="application/json"
        )
        assert response.status_code == HTTPStatus.OK
        response_data = response.json()
        self.check_fields(response_data)
        for item in response_data['items']:
            item in edit_data['items']
        assert response_data['status'] == edit_data['status']

    def test_order_delete(self, client, order):
        response = client.delete(self.orders_detail_url.format(id=order.id))
        assert response.status_code == HTTPStatus.NO_CONTENT
        assert Order.objects.filter(id=order.id).exists() is False

    def test_revenue(self, client, order):
        response = client.get(self.revenue_url)
        response_data = response.json()
        assert isinstance(response_data, dict)
        expected_fields = (
            'revenue', 'paid_orders'
        )
        for field in expected_fields:
            assert field in response_data
        initial_revenue = response_data['revenue']
        response = client.patch(
            self.orders_detail_url.format(id=order.id),
            data={'status': 'Paid'},
            content_type="application/json"
        )
        response = client.get(self.revenue_url)
        response_data = response.json()
        assert response_data['revenue'] - initial_revenue == order.total_price
