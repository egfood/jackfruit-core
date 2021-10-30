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
    product = models.ForeignKey(FarmerProduct, verbose_name='Фермерский продукт', related_name='order_item',
                                on_delete=models.CASCADE)
    value = models.PositiveIntegerField(verbose_name=f'Масса (от покупателя) ({settings.WEIGHT_UNIT_ABBREVIATION})',
                                        blank=True, null=True)
    actual_value = models.PositiveIntegerField(verbose_name=f'Фактическая масса ({settings.WEIGHT_UNIT_ABBREVIATION})',
                                               blank=True, null=True)
    order = models.ForeignKey(FoodOrder, verbose_name='Заказ', related_name='order_item', on_delete=models.CASCADE)

    @classmethod
    def get_buyer_cart_total(cls, buyer_profile, delivery) -> float:
        food_orders_args = {
            "delivery": delivery,
            "buyer": buyer_profile
        }
        order = FoodOrder.objects.filter(**food_orders_args).first()
        if order:
            return sum(order_item.item_total for order_item in cls.objects.filter(order=order))
        return 0.0

    @classmethod
    def get_buyer_cart_items_count(cls, buyer_profile, delivery) -> int:
        food_orders_args = {
            "delivery": delivery,
            "buyer": buyer_profile
        }
        order = FoodOrder.objects.filter(**food_orders_args).first()
        if order:
            return cls.objects.filter(order=order).count()
        return 0

    @classmethod
    def get_buyer_cart_items(cls, request, delivery, need_order_creation=False) -> QuerySet:
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

    @cached_property
    def item_total(self):
        return round(self.weight * self.product.price / int(self.product.value), 2)

    @cached_property
    def text_item_total(self):
        return f'{self.item_total} {settings.CURRENT_CURRENCY}'

    @cached_property
    def weight(self):
        if self.value is None and self.actual_value:
            raise ValueError("The 'value' and 'actual_value' properties can't be a Null together!")
        return self.value if self.actual_value is None else self.actual_value

    @cached_property
    def text_weight(self):
        return f"{self.weight} {settings.WEIGHT_UNIT_ABBREVIATION}"

    @cached_property
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
