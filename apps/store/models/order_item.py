import logging
from decimal import Decimal
from functools import cached_property
from typing import Tuple

from django.conf import settings
from django.db import models
from django.db.models import QuerySet
from simple_history.models import HistoricalRecords

from apps.farmer.models.product import FarmerProduct
from core.models import FoodAbstract
from .product import RootProduct
from .order import FoodOrder

log = logging.getLogger(__name__)


class FoodOrderItem(FoodAbstract):
    product = models.ForeignKey(FarmerProduct, verbose_name='Фермерский продукт', related_name='order_item',
                                on_delete=models.CASCADE)
    value = models.DecimalField(verbose_name='Объем/Кол./Вес (от покупателя)', blank=True, null=True, max_digits=10,
                                decimal_places=2)
    actual_value = models.DecimalField(verbose_name='Фактический Объем/Кол./Вес', blank=True, null=True, max_digits=10,
                                       decimal_places=2)
    order = models.ForeignKey(FoodOrder, verbose_name='Заказ', related_name='order_item', on_delete=models.CASCADE)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена (заполняется автоматически)',
                                blank=True, null=None)
    value_per_price = models.DecimalField(max_digits=10, decimal_places=1, null=True, blank=True,
                                          verbose_name='Объем/Кол./Вес за цену (заполняется автоматически)')
    trade_margin = models.DecimalField(verbose_name='Общая наценка (заполняется автоматически), %', blank=True,
                                       default=0, max_digits=5, decimal_places=2)

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
    def get_buyer_cart_items(cls, request, delivery, need_order_creation=False) -> Tuple[QuerySet, FoodOrder]:
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
        return queryset, order

    @cached_property
    def item_total(self):
        return self.get_item_total(volume_from_buyer=self.weight, price=self.price,
                                   value_per_price=self.value_per_price)

    @cached_property
    def item_total_from_buyer(self) -> Decimal:
        if self.value is None:
            raise ValueError(f"Value of product from buyer is not defined.")
        return self.get_item_total(volume_from_buyer=self.value, price=self.price,
                                   value_per_price=self.value_per_price)

    def get_item_total(self, volume_from_buyer: Decimal, price: Decimal, value_per_price: Decimal) -> Decimal:
        base_total = volume_from_buyer * price / value_per_price
        if self.trade_margin is not None:
            total = base_total * (1 + self.trade_margin_in_hundredths)
        else:
            total = base_total
        return round(total, 2)

    @cached_property
    def trade_margin_in_hundredths(self) -> Decimal:
        return self.trade_margin / 100

    @cached_property
    def text_item_total(self) -> str:
        return f'{self.item_total} {settings.CURRENT_CURRENCY}'

    @cached_property
    def weight(self):
        if self.value is None and self.actual_value:
            raise ValueError("The 'value' and 'actual_value' properties can't be a Null together!")
        return self.value if self.actual_value is None else self.actual_value

    @cached_property
    def text_weight(self):
        return f"{self.weight} {self.product.unit}"

    @cached_property
    def text_safety_weight(self):
        base = self.text_weight
        if self.actual_value:
            base += "[ФАКТ.]"
        return base

    @cached_property
    def delivery_short_name(self):
        base = f"Дост. {self.order.delivery.short_name}"
        if self.order.location:
            if self.order.location.is_office():
                base += "(в офис)"
            elif self.order.location.is_private():
                base += "(домой)"
        else:
            log.warning("Unknown type of location")
        return base

    def __str__(self):
        return f'Позиция {self.value} г. {self.product}[{self.order}]'

    def save(self, *args, **kwargs):
        farmer_product = self.product
        if isinstance(farmer_product, FarmerProduct):
            self.price = farmer_product.price
            self.value_per_price = farmer_product.value
            root_product = farmer_product.product
            if isinstance(root_product, RootProduct):
                self.trade_margin = root_product.trade_margin.total
        super().save(*args, **kwargs)

