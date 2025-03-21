from django.db import models
from django.db.models import Sum
from django.utils import timezone


STATUS = (
    ('Waiting', 'В ожидании'),
    ('Done', 'Готово'),
    ('Paid', 'Оплачено'),
)


class Item(models.Model):
    """Блюдо."""
    name = models.CharField('Название')
    price = models.FloatField('Цена')

    class Meta:
        verbose_name = 'блюдо'
        verbose_name_plural = 'Блюда'

    def __str__(self):
        return f'{self.name}, {self.price} руб.'


class Order(models.Model):
    """Заказ."""
    table_number = models.PositiveSmallIntegerField('Номер стола')
    items = models.ManyToManyField(Item, verbose_name='Список блюд')
    status = models.CharField('Статус', default='Waiting', choices=STATUS)
    created_at = models.DateTimeField(
        'Дата и время создания заказа', default=timezone.now
    )

    @property
    def total_price(self) -> float:
        """Вычисление общей стоимости заказа."""
        return self.items.aggregate(total_price=Sum('price'))['total_price']

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'заказ'
        verbose_name_plural = 'Заказы'
