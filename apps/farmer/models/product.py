from django.db import models
from django.db.models import Avg

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
        return f"Фер. пр. #{self.product.id} - {self.product.name} [фермер={self.farmer.name}#{self.farmer.id}]"

    @classmethod
    def get_visible_products(cls, farmer_products_queryset=None, category_pk=None):
        source = cls.objects if farmer_products_queryset is None else farmer_products_queryset
        if category_pk is not None:
            source = source.filter(product__category=category_pk).select_related('product__category')
        return source.filter(product__is_visible=True).select_related('product')

    @classmethod
    def get_ratings(cls, products_queryset=None, return_dict_by_pk=False):
        base_queryset = products_queryset if products_queryset else cls.objects
        result = base_queryset.annotate(average_rating=Avg('order_item__farmer_feedback__rating')).values(
            'pk', 'average_rating'
        )
        if return_dict_by_pk:
            return {qs['pk']: qs['average_rating'] for qs in result}
        return  result
