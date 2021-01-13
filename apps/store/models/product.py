from django.conf import settings
from django.db import models

from core.models.base import FoodAbstract


class FoodProduct(FoodAbstract):
    PRODUCT_UNIT_CHOICES = (
        ('kg', 'кг'),
        ('gm', 'гр.'),
        ('100gm', '100 гр.'),
        ('pс', 'шт.'),
        ('L.', 'л'),
    )
    PACKAGING_CHOICES = (
        ('not_known', 'не известно'),
        ('no_packaging', 'без упаковки'),
        ('paper_bag', 'бумажный пакет'),
    )

    farmer = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Фермер', on_delete=models.CASCADE)
    name = models.CharField(verbose_name='Название продукта', max_length=250)
    quantity_per_price = models.CharField(
        verbose_name='Количество за указанную цену',
        max_length=20,
        choices=PRODUCT_UNIT_CHOICES,
        default=PRODUCT_UNIT_CHOICES[0][0])
    min_weight = models.PositiveIntegerField(verbose_name='Минимальная масса продукта (г.)', blank=True, null=True)
    price = models.DecimalField(verbose_name='Цена', max_digits=7, decimal_places=2)
    image = models.ImageField('Изображение продукта', upload_to='products', max_length=255, blank=True)
    is_visible = models.BooleanField(verbose_name='Включен', default=True)
    description = models.TextField('Описание продукта', blank=True)
    packaging = models.TextField('Упаковка', max_length=20, choices=PACKAGING_CHOICES, default=PACKAGING_CHOICES[0][1])

    def __str__(self):
        return f'{self.name} ({self.price}BYN за {self.get_quantity_per_price_display()}) от {self.farmer.profile.name}'
