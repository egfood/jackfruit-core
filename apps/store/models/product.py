from django.db import models

from apps.store.models.product_category import ProductCategory
from core.models.base import FoodAbstract


class RootProduct(FoodAbstract):
    name = models.CharField(verbose_name='Название продукта', max_length=250)
    image = models.ImageField('Изображение продукта', upload_to='products', max_length=255, blank=True)
    is_visible = models.BooleanField(verbose_name='Включен', default=True)
    description = models.TextField('Описание продукта', blank=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, verbose_name="Категория", null=True,
                                 related_name='root_product')

    def __str__(self):
        return f'Б. пр. #{self.id} - {self.name}'
