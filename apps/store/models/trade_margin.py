from functools import cached_property

from django.conf import settings
from django.db import models
from simple_history.models import HistoricalRecords

from core.models import FoodAbstract


class TradeMargin(FoodAbstract):
    backoffice_margin = models.DecimalField(verbose_name='Наценка бэкофиса, %', blank=True, default=0, max_digits=5,
                                            decimal_places=2)
    dev_margin = models.DecimalField(verbose_name='Наценка разработчиков, %', blank=True, default=0, max_digits=5,
                                     decimal_places=2)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)

    @cached_property
    def total(self):
        return self.backoffice_margin + self.dev_margin

    @staticmethod
    def get_historical_total(historical_trade_margin):
        return historical_trade_margin.backoffice_margin + historical_trade_margin.dev_margin

    def __str__(self):
        return f'Наценка {self.total}% [бэк.={self.backoffice_margin}%, разр.={self.dev_margin}%]'
