import logging
from functools import cached_property

from django.conf import settings
from django.db import models
from django.db.models import QuerySet

from apps.farmer.models.product import FarmerProduct
from core.models import FoodAbstract
from .order import FoodOrder

log = logging.getLogger(__name__)


class FoodOrderItem(FoodAbstract):
    _item_total = None
    _weight = None
    _text_weight = None

    product = models.ForeignKey(FarmerProduct, verbose_name='Фермерский продукт', related_name='order_item',
                                on_delete=models.CASCADE)
    value = models.PositiveIntegerField(verbose_name=f'Масса (от покупателя) ({settings.WEIGHT_UNIT_ABBREVIATION})',
                                        blank=True, null=True)
    actual_value = models.PositiveIntegerField(verbose_name=f'Фактическая масса ({settings.WEIGHT_UNIT_ABBREVIATION})',
                                               blank=True, null=True)
    order = models.ForeignKey(FoodOrder, verbose_name='Заказ', related_name='order_item', on_delete=models.CASCADE)

    @classmethod
    def get_buyer_order_items(cls, request, delivery, need_order_creation=False) -> QuerySet:
        food_orders_args = {
            "delivery": delivery,
            "buyer": request.user.profile
        }
        order = FoodOrder.objects.filter(**food_orders_args).first()
        if order:
            queryset = cls.objects.filter(order=order)
        elif need_order_creation:
            order = FoodOrder.objects.create(**food_orders_args)
            queryset = cls.objects.filter(order=order)
        else:
            queryset = None
        return queryset

    @property
    def item_total(self):
        if self._item_total is None:
            self._item_total = round(self.weight * self.product.price / int(self.product.value), 2)
        return self._item_total

    @property
    def weight(self):
        if self._weight is None:
            self._weight = self.value if self.actual_value is None else self.actual_value
        return self._weight

    @property
    def text_weight(self):
        if self._text_weight is None:
            self._text_weight = f"{self.weight} {settings.WEIGHT_UNIT_ABBREVIATION}"
        return self._text_weight

    @property
    def text_safety_weight(self):
        base = self.text_weight
        if self.actual_value:
            base += "[ФАКТ.]"
        return base

    @cached_property
    def delivery_short_name(self):
        base = f"Дост. {self.order.delivery.short_name}"
        if self.order.location.is_office():
            base += "(в офис)"
        elif self.order.location.is_private():
            base += "(домой)"
        else:
            log.warning("Unknown type of location")
        return base

    def __str__(self):
        return f'Позиция {self.value} г. {self.product}[{self.order}]'
