from functools import cached_property

from apps.store.models.delivery import FoodDelivery
from .exceptions import HasNoActiveDelivery


class NearestDeliveryMixin:
    @cached_property
    def delivery(self):
        delivery = FoodDelivery.get_nearest_delivery()
        if delivery is None:
            raise HasNoActiveDelivery
        else:
            return delivery
