from django.urls import path

from .views import (
    OrderCreateView, OrderDeleteView, OrderDetailView, OrderListView,
    OrderUpdateView, RevenueListView
)

app_name = 'orders'

urlpatterns = [
    path('', OrderListView.as_view(), name='index'),
    path(
        'orders/<int:order_id>/',
        OrderDetailView.as_view(),
        name='detail_order'
    ),
    path('orders/create/', OrderCreateView.as_view(), name='create_order'),
    path(
        'orders/<int:order_id>/edit/',
        OrderUpdateView.as_view(),
        name='edit_order'
    ),
    path(
        'orders/<int:order_id>/delete/',
        OrderDeleteView.as_view(),
        name='delete_order'
    ),
    path(
        'orders/revenue/',
        RevenueListView.as_view(),
        name='revenue'
    )
]
