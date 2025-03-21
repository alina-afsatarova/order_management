from rest_framework import serializers

from orders.models import Order, STATUS


class OrderReadSerializer(serializers.ModelSerializer):
    """Отображение информации о заказе."""

    items = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Order
        fields = (
            'id', 'table_number', 'items', 'status', 'total_price',
            'created_at'
        )


class OrderCreateSerializer(serializers.ModelSerializer):
    """Создание объявления."""

    class Meta:
        model = Order
        fields = ('table_number', 'items',)

    def to_representation(self, instance) -> OrderReadSerializer:
        return OrderReadSerializer(instance).data


class OrderUpdateSerializer(serializers.ModelSerializer):
    """Изменение объявления."""

    status = serializers.ChoiceField(choices=STATUS, required=True)

    class Meta:
        model = Order
        fields = ('items', 'status',)

    def to_representation(self, instance) -> OrderReadSerializer:
        return OrderReadSerializer(instance).data
