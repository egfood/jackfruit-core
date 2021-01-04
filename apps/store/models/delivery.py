from datetime import datetime, timedelta

from django.db import models
from django.utils import timezone

from core.settings_common import DELIVERY_DEADLINE_IN_HOURS
from core.models.base import FoodAbstract


class FoodDelivery(FoodAbstract):
    DELIVERY_STATE_CHOICES = (
        ('collecting', 'Сбор заявок'),
        ('processing', 'Обработка заявок'),
        ('processing', 'Обработка заявок'),
        ('finished', 'Заказы доставлены'),
        ('suspended', 'Сбор заявок приостановлен'),
        ('cancelled', 'Отменена'),
    )

    date = models.DateTimeField(verbose_name='Дата и время поставки')
    is_urgently_deactivated = models.BooleanField(verbose_name='Срочно выключить', default=False)
    state = models.CharField(verbose_name="Статус доставки", max_length=80, choices=DELIVERY_STATE_CHOICES,
                             default=DELIVERY_STATE_CHOICES[0][0])
    __short_name = None

    @property
    def is_deactivated(self) -> bool:
        if self.is_urgently_deactivated or timezone.now() > self.delivery_deadline:
            return True
        return False

    @property
    def delivery_deadline(self) -> datetime:
        return self.date - timedelta(hours=DELIVERY_DEADLINE_IN_HOURS)

    def delivery_state_message(self):
        return 'Деактивирована' if self.is_deactivated else 'Активна'

    delivery_state_message.short_description = 'Статус'

    @staticmethod
    def get_nearest_delivery():
        deliveries = FoodDelivery.objects.all().order_by('date')
        if deliveries is None:
            return
        active_deliveries = [d for d in deliveries if not d.is_deactivated]
        return active_deliveries[0] if active_deliveries else None

    def __str__(self):
        return f'Доставка {self.date.strftime("%d %b %Y")} ({self.delivery_state_message()})'

    @property
    def short_name(self):
        if self.__short_name is None:
            self.__short_name = f'#{self.pk}({self.date.strftime("%d %b %Y")})'
        return self.__short_name
