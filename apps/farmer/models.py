from django.conf import settings
from django.db import models

from apps.store.models import RootProduct
from core.models import AbsProfile, FoodAbstract


class FarmerProfile(AbsProfile):
    service_zone = models.TextField(verbose_name='Зона обслуживания', blank=True, default="")
    legal_name = models.CharField(verbose_name='Название компании / фермерского хозяйства', max_length=500, blank=True,
                                  default="")

    @property
    def stringify_profile_type(self):
        return "фермера"


class FarmerProduct(FoodAbstract):
    UNIT_PRODUCT = (
        ('kg', 'кг'),
        ('gm', 'гр.'),
        ('pс', 'шт.'),
        ('L.', 'л'),
    )
    SIZE_CHOICES = (
        ('s', 'Маленький'),
        ('M', 'Средний'),
        ('L', 'Большой'),
    )
    farmer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Фермер')
    product = models.ForeignKey(RootProduct, on_delete=models.CASCADE, verbose_name="Базовый продукт")
    value = models.DecimalField(max_digits=10, decimal_places=1, verbose_name='Объем/Кол./Вес')
    unit = models.CharField(max_length=2, choices=UNIT_PRODUCT, verbose_name='Ед. измерения',
                            default=UNIT_PRODUCT[0][0])
    size = models.CharField(max_length=1, choices=SIZE_CHOICES, verbose_name='Размер', default=SIZE_CHOICES[1][0])
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')

    def __str__(self):
        return f"Продукт #{self.product.id} [фермер={self.farmer}]"
