from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import (
    OrderCreateSerializer, OrderReadSerializer, OrderUpdateSerializer
)
from orders.models import Order


class OrderViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Order."""
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    filterset_fields = ('status',)
    search_fields = ('table_number', 'status',)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve', 'revenue'):
            return OrderReadSerializer
        if self.action == 'partial_update':
            return OrderUpdateSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        if self.action == 'revenue':
            return Order.objects.filter(status='Paid')
        return super().get_queryset()

    @action(
        detail=False,
        methods=['get', ]
    )
    def revenue(self, request):
        """Вывод информации о выручке и об оплаченных заказах."""
        return Response(
            {
                'revenue': sum(
                    order.total_price for order in self.get_queryset()
                ),
                'paid_orders': self.get_serializer(
                    self.get_queryset(), many=True
                ).data
            },
            status=status.HTTP_200_OK
        )
