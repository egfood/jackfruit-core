from decimal import Decimal, getcontext
from functools import cached_property
from types import GenericAlias
from typing import Dict

from django.test import TestCase

from apps.store.price import rounding_up_to_multiplicity

PriceValues = GenericAlias(tuple, (Decimal,) * 10)


class PriceSamples:

    def __init__(self, in_prices: PriceValues, out_prices: Dict[int, PriceValues]) -> None:
        self._in = in_prices
        self._out = out_prices

    @cached_property
    def in_prices(self) -> PriceValues:
        return self._in

    @cached_property
    def multiplicities(self):
        return self._out.keys()

    def get_out_prices(self, multiplicity_index: int) -> PriceValues:
        if multiplicity_index == 1:
            return self.in_prices
        return self._out[multiplicity_index]


class RoundingToMultipleTest(TestCase):
    test_engine = PriceSamples(
        in_prices=tuple(
            map(Decimal, "1.11 1.22 1.33 2.54 7.75 9.96 19.87 99.98 9999.99 100.00".split())
        ),
        out_prices={
            5: tuple(map(Decimal, "1.10 1.20 1.35 2.55 7.75 9.95 19.85 100.00 10000.00 100.00".split())),
            10: tuple(map(Decimal, "1.10 1.20 1.30 2.50 7.80 10.0 19.9 100.00 10000.00 100.00".split())),
            50: tuple(map(Decimal, "1.00 1.00 1.50 2.50 8.00 10.0 20.0 100.00 10000.00 100.00".split())),
        }
    )

    def setUp(self):
        self.f = rounding_up_to_multiplicity

    def test_without_rounding(self):
        with self.settings(MULTIPLICITY_OF_PRICE_ROUNDING=1):
            out_values = tuple(map(self.f, self.test_engine.in_prices))
            self.assertEquals(self.test_engine.in_prices, out_values)

    def test_rounding(self):
        for index in self.test_engine.multiplicities:
            with self.settings(MULTIPLICITY_OF_PRICE_ROUNDING=index):
                out_values = tuple(map(self.f, self.test_engine.in_prices))
                self.assertEquals(self.test_engine.get_out_prices(index), out_values)
