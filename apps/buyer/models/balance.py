from django.conf import settings
from django.db import models
from django.db.models import Sum

from apps.store.models.order import FoodOrder
from core.models import FoodAbstract


class BuyerBalance(FoodAbstract):
    """
    The model record reflects the current financial commitments between the project and the buyers by one order.
    Use a positive number if the project owes the buyer and a negative number if the buyer owes the project.
    """
    order = models.ForeignKey(FoodOrder, verbose_name='Заказ', related_name='buyer_balance', on_delete=models.CASCADE)
    value = models.DecimalField("Значение", max_digits=9, decimal_places=2, help_text=settings.BUYER_BALANCE_VALUE_HINT)

    @classmethod
    def get_total_balance(cls, buyer_profile):
        result = cls.objects.filter(order__buyer=buyer_profile).aggregate(total_balance=Sum('value'))
        if result['total_balance'] is not None:
            return result['total_balance']
        else:
            return 0

    def __str__(self):
        prefix = "+" if self.value > 0 else ""
        return f"{prefix}{self.value} {settings.CURRENT_CURRENCY} в {self.order}"