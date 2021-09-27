from django.db import models

from apps.store.models.product import RootProduct
from core.models import FoodAbstract
from .profile import FarmerProfile


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
    farmer = models.ForeignKey(FarmerProfile, on_delete=models.CASCADE, verbose_name='Фермер')
    product = models.ForeignKey(RootProduct, on_delete=models.CASCADE, verbose_name="Базовый продукт",
                                related_name='farmer_product')
    value = models.DecimalField(max_digits=10, decimal_places=1, verbose_name='Объем/Кол./Вес')
    unit = models.CharField(max_length=2, choices=UNIT_PRODUCT, verbose_name='Ед. измерения',
                            default=UNIT_PRODUCT[0][0])
    size = models.CharField(max_length=1, choices=SIZE_CHOICES, verbose_name='Размер', default=SIZE_CHOICES[1][0])
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')

    def __str__(self):
        return f"Продукт #{self.product.id} [фермер={self.farmer.name}#{self.farmer.id}]"

    @classmethod
    def get_visible_products(cls, farmer_products_queryset=None, category=None):
        source = cls if farmer_products_queryset is None else farmer_products_queryset
        if category is not None:
            source = source.filter(product__category=category).select_related('product__category')
        return source.objects.filter(product__is_visible=True).select_related('product')
