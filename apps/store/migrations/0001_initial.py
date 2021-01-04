# Generated by Django 3.0.3 on 2020-05-25 20:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FoodDelivery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_creation', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Изменен')),
                ('date', models.DateTimeField(verbose_name='Дата и время поставки')),
                ('is_urgently_deactivated', models.BooleanField(default=False, verbose_name='Срочно выключить')),
                ('state', models.CharField(choices=[('collecting', 'Сбор заявок'), ('processing', 'Обработка заявок'), ('processing', 'Обработка заявок'), ('finished', 'Заказы доставлены'), ('suspended', 'Сбор заявок приостановлен'), ('cancelled', 'Отменена')], default='collecting', max_length=80, verbose_name='Статус доставки')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FoodOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_creation', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Изменен')),
                ('state', models.CharField(choices=[('awaiting_processing', 'Ожидает обработки'), ('prepared', 'Заказ сформирован'), ('delivered', 'Заказ доставлен'), ('cancelled', 'Заказ доставлен')], default='awaiting_processing', max_length=85, verbose_name='Статус заказа')),
                ('delivery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order', to='store.FoodDelivery', verbose_name='Доставка')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
        ),
        migrations.CreateModel(
            name='FoodProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_creation', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Изменен')),
                ('name', models.CharField(max_length=250, verbose_name='Название продукта')),
                ('weight_per_price', models.CharField(choices=[('1000', '1000 гр.'), ('100', '100 гр.')], default='1000', max_length=20, verbose_name='Вес за указанную цену')),
                ('price', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='Цена')),
                ('image', models.ImageField(blank=True, max_length=255, upload_to='products', verbose_name='Изображение продукта')),
                ('is_visible', models.BooleanField(default=True, verbose_name='Включен')),
                ('description', models.TextField(blank=True, verbose_name='Описание продукта')),
                ('supplier_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Поставщик')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FoodOrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_creation', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Изменен')),
                ('value', models.PositiveIntegerField(blank=True, null=True, verbose_name='Масса продукта (от покупателя) (гр.)')),
                ('actual_value', models.PositiveIntegerField(blank=True, null=True, verbose_name='Фактическая масса продукта (гр.)')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_item', to='store.FoodOrder', verbose_name='Заказ')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_item', to='store.FoodProduct', verbose_name='Продукт')),
            ],
        ),
        migrations.AddConstraint(
            model_name='foodorderitem',
            constraint=models.UniqueConstraint(fields=('order', 'product'), name='each_order_item'),
        ),
        migrations.AddIndex(
            model_name='foodorder',
            index=models.Index(fields=['delivery', 'user'], name='store_foodo_deliver_d2ecad_idx'),
        ),
    ]
