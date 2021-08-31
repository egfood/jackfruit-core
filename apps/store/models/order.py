import logging
from functools import cached_property

from django.conf import settings
from django.db import models

from apps.buyer.models.profile import BuyerProfile
from core.models.base import FoodAbstract
from .delivery import FoodDelivery
from .location import Location

log = logging.getLogger(__name__)


class FoodOrder(FoodAbstract):
    _order_item_related_name = None
    _order_weight = None
    _text_order_weight = None
    _text_delivery = None
    _text_user = None
    _phone = None

    class Meta:
        indexes = (
            models.Index(fields=['delivery', 'buyer', 'location']),
        )
        unique_together = ['delivery', 'buyer', 'location']

    ORDER_STATE_CHOICES = (
        ('awaiting_processing', 'В процессе'),
        ('delivered', 'Доставлено'),
    )

    delivery = models.ForeignKey(FoodDelivery, verbose_name='Доставка', related_name='order',
                                 on_delete=models.CASCADE)
    state = models.CharField(verbose_name='Статус заказа', max_length=85, choices=ORDER_STATE_CHOICES,
                             default=ORDER_STATE_CHOICES[0][0])
    buyer = models.ForeignKey(BuyerProfile, verbose_name='Пользователь', related_name='order',
                              on_delete=models.CASCADE)
    location = models.ForeignKey(Location, verbose_name='Адрес', related_name='order', on_delete=models.SET_NULL,
                                 null=True)

    @cached_property
    def total_cost(self):
        total_cost = sum([order_item.item_total for order_item in self.order_items_related])
        order_cost = total_cost + settings.SHIPPING_COST if self.location.is_private() else total_cost
        return order_cost

    @property
    def total_weight(self):
        if self._order_weight is None:
            self._order_weight = sum([order_item.weight for order_item in self.order_items_related])
        return self._order_weight

    @property
    def text_total_weight(self):
        if self._text_order_weight is None:
            total_weight = sum([order_item.weight for order_item in self.order_items_related])
            self._text_order_weight = f"{total_weight} {settings.WEIGHT_UNIT_ABBREVIATION}"
        return self._text_order_weight

    @property
    def text_delivery(self):
        if self._text_delivery is None:
            self._text_delivery = self.delivery.short_name
        return self._text_delivery

    @property
    def text_user(self):
        if self._text_user is None:
            self._text_user = self.buyer.email
        return self._text_user

    @property
    def text_phone(self):
        if self._phone is None:
            try:
                if self.buyer.is_farmer:
                    self._phone = self.buyer.profile.phone
                elif self.buyer.is_buyer:
                    self._phone = self.location.phone
                else:
                    log.error("Can't fetch phone number from unknown type of user profile")
                    self._phone = ""
            except AttributeError:
                self._phone = ""
        return self._phone

    @cached_property
    def order_items_related(self):
        from .order_item import FoodOrderItem
        return FoodOrderItem.objects.all()

    def __str__(self):
        base = f'{self.delivery} для {self.buyer.name} (profile#{self.buyer.id})'
        if self.location.is_private():
            base += '[домой]'
        elif self.location.is_office():
            base += '[в офис]'
        else:
            log.warning('Unknown type of location.')
        return base
