from django.conf import settings
from django.db import models
from simple_history.models import HistoricalRecords

from apps.farmer.image_transformer import ImageTransformer
from apps.store.models.product_category import ProductCategory
from apps.store.models.trade_margin import TradeMargin
from core.models.base import FoodAbstract


class RootProduct(FoodAbstract):
    name = models.CharField(verbose_name='Название продукта', max_length=250)
    image = models.ImageField('Изображение продукта', upload_to='products', max_length=255, blank=True)
    is_visible = models.BooleanField(verbose_name='Включен', default=True)
    description = models.TextField('Описание продукта', blank=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, verbose_name="Категория", null=True,
                                 related_name='root_product')
    trade_margin = models.ForeignKey(TradeMargin, on_delete=models.SET_NULL, verbose_name="Наценка",
                                     blank=True, null=True, default=None, related_name='root_product')
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)

    def __str__(self):
        return f'Б. пр. #{self.id} - {self.name}'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        if self.image:
            it = ImageTransformer(self.image.path, settings.ROOT_PRODUCT_IMAGE_WIDTH, settings.ROOT_PRODUCT_IMAGE_HEIGHT)
            it.transform()
