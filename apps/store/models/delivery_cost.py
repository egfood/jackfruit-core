from django.db import models

from django.conf import settings
from core.models.base import FoodAbstract
from simple_history.models import HistoricalRecords


class DeliveryCost(FoodAbstract):
    value = models.DecimalField(verbose_name=f"Стоимость доставки", default=0, max_digits=5, decimal_places=2)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)

    def __str__(self):
        return f"[Стоимость доставки] {self.value} {settings.CURRENT_CURRENCY}"

    @classmethod
    def get_delivery_cost(cls):
        delivery_cost_qs = cls.objects.all()
        if len(delivery_cost_qs) < 1:
            raise Exception("No delivery costs set")
        return delivery_cost_qs[0].value
