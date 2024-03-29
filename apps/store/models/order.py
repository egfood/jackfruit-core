import logging
from functools import cached_property

from django.conf import settings
from django.db import models

from apps.buyer.models.profile import BuyerProfile
from core.models.base import FoodAbstract
from core.models.user import GreenUser
from core.status_engine import StatusEnum
from .delivery import FoodDelivery
from .location import Location

log = logging.getLogger(__name__)


class ORDER_STATE(StatusEnum):
    created = 'Создан'
    awaiting_processing = 'Ожидает обработки'
    delivered = 'Доставлено'


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

    ORDER_STATE = ORDER_STATE
    ORDER_STATES_WHEN_ORDER_WAS_SENT = ('awaiting_processing', 'delivered')

    PAYMENT_TYPE_CHOICES = (
        ('cash', 'Наличными'),
        ('card', 'Картой'),
    )

    delivery = models.ForeignKey(FoodDelivery, verbose_name='Доставка', related_name='order',
                                 on_delete=models.CASCADE)
    delivery_cost = models.DecimalField(verbose_name=f"Стоимость доставки", default=0, max_digits=5, decimal_places=2)
    state = models.CharField(verbose_name='Статус заказа', max_length=85, choices=ORDER_STATE.get_as_list(),
                             default=ORDER_STATE.created.name)
    buyer = models.ForeignKey(BuyerProfile, verbose_name='Пользователь', related_name='order',
                              on_delete=models.CASCADE)
    location = models.ForeignKey(Location, verbose_name='Адрес', related_name='order', on_delete=models.SET_NULL,
                                 null=True)
    payment_type = models.state = models.CharField(verbose_name='Способ оплаты', max_length=100,
                                                   choices=PAYMENT_TYPE_CHOICES, default=PAYMENT_TYPE_CHOICES[0][0])

    @cached_property
    def total_cost(self):
        total_cost = sum([order_item.item_total for order_item in self.order_items_related])
        return total_cost + self.delivery_cost

    @property
    def total_weight(self):
        if self._order_weight is None:
            self._order_weight = sum([order_item.weight for order_item in self.order_items_related])
        return self._order_weight

    @property
    def text_delivery(self):
        if self._text_delivery is None:
            self._text_delivery = self.delivery.short_name
        return self._text_delivery

    @property
    def text_user(self):
        if self._text_user is None:
            self._text_user = self.buyer.user
        return self._text_user

    @property
    def text_phone(self):
        if self._phone is None:
            try:
                if self.buyer.phone:
                    self._phone = self.buyer.phone
                else:
                    log.error("Can't fetch phone number from unknown type of user profile")
                    self._phone = ""
            except AttributeError:
                self._phone = ""
        return self._phone

    @property
    def locations(self):
        if self.location.location_type == 'private':
            return "НА ДОМ"
        elif self.location.location_type == 'office':
            return "ОФИС"

    @cached_property
    def order_items_related(self):
        return self.order_item.all()

    @cached_property
    def is_order_sent_by_user(self):
        return self.state in self.ORDER_STATES_WHEN_ORDER_WAS_SENT

    @classmethod
    def get_order(cls, delivery: FoodDelivery, buyer: GreenUser):
        return cls.objects.filter(delivery=delivery, buyer=buyer.profile).first()

    def save(self, *args, **kwargs):
        if isinstance(self.location, Location):
            self.delivery_cost = self.location.delivery_cost
        super().save(*args, **kwargs)

    def __str__(self):
        base = f'{self.delivery} для {self.buyer.name} (profile#{self.buyer.id})'
        try:
            if self.location.is_private():
                base += '[домой]'
            elif self.location.is_office():
                base += '[в офис]'
        except AttributeError:
            base += '[не уточненный адрес]'
        return base
