from django import forms
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)

from .forms import CreateOrderForm, UpdateOrderForm
from .models import Order


class OrderMixin:

    model = Order
    pk_url_kwarg = 'order_id'


class OrderDetailView(OrderMixin, DetailView):
    """Отображение информации о заказе."""

    template_name = 'orders/order_detail.html'


class OrderListView(OrderMixin, ListView):
    """Отображение всех заказов в виде таблицы."""

    template_name = 'orders/index.html'

    EXPECTED_STATUSES = {
        'в ожидании': 'Waiting',
        'готово': 'Done',
        'оплачено': 'Paid'
    }

    def get_queryset(self) -> list[Order]:
        """Возвращает список заказов в зависимоти от переданным параметров.

        Парамет 'select' - фильтрация заказов по статусу.
        Параметр 'q' - поиск заказа по номеру стола или статусу.
        Если ни один из параметров не передан возвращается список всех заказов.
        """
        select: str | None = self.request.GET.get('select')
        if select:
            return Order.objects.filter(status=select)

        query: str | None = self.request.GET.get('q')
        if query:
            query_lower: str = query.lower()
            status_keys: list[str] = [
                key for key in self.EXPECTED_STATUSES
                if key.startswith(query_lower)
            ]
            if status_keys:
                status: str = self.EXPECTED_STATUSES[status_keys[0]]
                object_list: list[Order] = Order.objects.filter(status=status)
            else:
                object_list = Order.objects.filter(
                    table_number__icontains=query
                )
            return object_list

        return super().get_queryset()


class OrderTemplateMixin:

    template_name = 'orders/order_create.html'
    success_url = reverse_lazy('orders:index')


class OrderCreateView(OrderMixin, OrderTemplateMixin, CreateView):
    """Создание заказа."""

    form_class = CreateOrderForm


class OrderUpdateView(OrderMixin, OrderTemplateMixin, UpdateView):
    """Редактирование заказа."""

    form_class = UpdateOrderForm

    def get_context_data(self, **kwargs) -> dict:
        """Заполнение формы информацией о заказе при его изменении,
        добавление формы в словарь context.
        """
        context: dict = super().get_context_data(**kwargs)
        form: forms.ModelForm = self.form_class(instance=self.get_object())
        context = {'form': form}
        return context


class OrderDeleteView(OrderMixin, OrderTemplateMixin, DeleteView):
    """Удаление заказа."""

    pass


class RevenueListView(OrderMixin, ListView):
    """Отображение информации о выручке."""

    template_name = 'orders/revenue.html'

    def get_queryset(self) -> list[Order]:
        """Возвращает заказы со статусом 'Оплачено'."""
        return Order.objects.filter(status='Paid')

    def get_context_data(self, **kwargs) -> dict:
        """Расчет общего объема выручки, добавление информации о выручке
        и об оплаченных заказах в словарь context.
        """
        context: dict = super().get_context_data(**kwargs)
        context['revenue'] = sum(
            order.total_price for order in self.get_queryset()
        )
        context['paid_orders'] = self.get_queryset()
        return context
