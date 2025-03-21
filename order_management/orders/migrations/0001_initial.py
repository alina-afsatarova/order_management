# Generated by Django 5.1.7 on 2025-03-21 15:38

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(verbose_name='Название')),
                ('price', models.FloatField(verbose_name='Цена')),
            ],
            options={
                'verbose_name': 'блюдо',
                'verbose_name_plural': 'Блюда',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table_number', models.PositiveSmallIntegerField(verbose_name='Номер стола')),
                ('status', models.CharField(choices=[('Waiting', 'В ожидании'), ('Done', 'Готово'), ('Paid', 'Оплачено')], default='Waiting', verbose_name='Статус')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата и время создания заказа')),
                ('items', models.ManyToManyField(to='orders.item', verbose_name='Список блюд')),
            ],
            options={
                'verbose_name': 'заказ',
                'verbose_name_plural': 'Заказы',
                'ordering': ('-created_at',),
            },
        ),
    ]
