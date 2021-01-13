import logging

from django.conf import settings
from django.db import models

from core.models.base import FoodAbstract
from . import Location, FoodDelivery

log = logging.getLogger(__name__)


class FoodOrder(FoodAbstract):
    _order_cost = None
    _order_item_related_name = None
    _order_weight = None
    _text_order_weight = None
    _text_delivery = None
    _text_user = None
    _phone = None
    _order_items_related = None

    class Meta:
        abstract = True
        indexes = (
            models.Index(fields=['delivery', 'user']),
        )

    ORDER_STATE_CHOICES = (
        ('awaiting_processing', 'В процессе'),
        ('delivered', 'Доставлено'),
    )

    delivery = models.ForeignKey(FoodDelivery, verbose_name='Доставка', related_name='order',
                                 on_delete=models.CASCADE)
    state = models.CharField(verbose_name='Статус заказа', max_length=85, choices=ORDER_STATE_CHOICES,
                             default=ORDER_STATE_CHOICES[0][0])
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Пользователь', related_name='order',
                             on_delete=models.CASCADE)
    location = models.ForeignKey(Location, verbose_name='Адрес', related_name='order', on_delete=models.SET_NULL,
                                 null=True)

    @property
    def total_cost(self):
        if self._order_cost is None:
            total_cost = sum([order_item.item_total for order_item in self.order_items_related])
            self._order_cost = total_cost + settings.SHIPPING_COST if self.location.is_private() else total_cost
        return self._order_cost

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
            self._text_user = self.user.email
        return self._text_user

    @property
    def text_phone(self):
        if self._phone is None:
            try:
                if self.user.is_farmer():
                    self._phone = self.user.profile.phone
                elif self.user.is_buyer():
                    self._phone = self.location.phone
                else:
                    log.error("Can't fetch phone number from unknown type of user profile")
                    self._phone = ""
            except AttributeError:
                self._phone = ""
        return self._phone

    @property
    def order_items_related(self):
        if self._order_items_related is None:
            order_items_realted_manager = getattr(self, self._order_item_related_name)
            self._order_items_related = order_items_realted_manager.all()
        return self._order_items_related

    def __str__(self):
        base = f'{self.delivery} для {self.user}'
        if self.location.is_private():
            base += '[домой]'
        elif self.location.is_office():
            base += '[в офис]'
        else:
            log.warning('Unknown type of location.')
        return base
