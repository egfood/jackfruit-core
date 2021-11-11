from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import Sum

from apps.store.models.order_item import FoodOrderItem
from core.models import FoodAbstract


class BuyerBalance(FoodAbstract):
    """
    The model record reflects the current financial commitments between the project and the buyers by one order.
    Use a positive number if the project owes the buyer and a negative number if the buyer owes the project.
    """
    order = models.OneToOneField(FoodOrderItem, verbose_name='Заказ', related_name='buyer_balance',
                                 on_delete=models.CASCADE)
    value = models.DecimalField("Значение", max_digits=9, decimal_places=2, help_text=settings.BUYER_BALANCE_VALUE_HINT)
    description = models.CharField(verbose_name='Комментарий к заказу', blank=True, null=True, max_length=200)

    @classmethod
    def get_total_balance(cls, buyer_profile) -> float:
        result = cls.objects.filter(order__order__buyer=buyer_profile).aggregate(total_balance=Sum('value'))
        if result['total_balance'] is not None:
            return result['total_balance']
        else:
            return 0

    @classmethod
    def get_text_total_balance(cls, buyer_profile) -> str:
        balance = cls.get_total_balance(buyer_profile)
        return f'+{balance}' if balance > 0 else str(balance)

    def __str__(self):
        prefix = "+" if self.value > 0 else ""
        return f"{prefix}{self.value} {settings.CURRENT_CURRENCY} в {self.order}"

    @classmethod
    def get_total_balance_delivery(cls, order_item_queryset):
        result = 0
        for order_item in order_item_queryset:
            try:
                get_buyer_balance_value = cls.objects.get(order=order_item).value
            except ObjectDoesNotExist:
                get_buyer_balance_value = 0
            result = result + get_buyer_balance_value
        return result
