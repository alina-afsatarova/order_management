from django import forms
from .models import Item, Order


class CreateOrderForm(forms.ModelForm):
    """Форма для создания объявлеия."""

    items = forms.ModelMultipleChoiceField(
        queryset=Item.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Список блюд'
    )

    class Meta:
        model = Order
        fields = ('table_number', 'items')


class UpdateOrderForm(forms.ModelForm):
    """Форма для редактирования объявлеия."""

    items = forms.ModelMultipleChoiceField(
        queryset=Item.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Список блюд'
    )

    class Meta:
        model = Order
        fields = ('items', 'status')
