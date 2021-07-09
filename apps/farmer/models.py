from django.db import models
from django.conf import settings

from core.models import AbsProfile, FoodAbstract
from apps.store.models import FoodProduct


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
        ('L.', 'л'),)
    SIZE_CHOICES = (
        ('s', 'Маленький'),
        ('M', 'Средний'),
        ('L', 'Большой'),
    )
    farmer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Фермер')
    name = models.ForeignKey(FoodProduct, on_delete=models.CASCADE, verbose_name='Название продукта')
    weight = models.PositiveIntegerField(verbose_name='Вес')
    unit = models.CharField(max_length=2, choices=UNIT_PRODUCT, verbose_name='Ед. измерения')
    size = models.CharField(max_length=1, choices=SIZE_CHOICES, verbose_name='Размер')
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Цена')
