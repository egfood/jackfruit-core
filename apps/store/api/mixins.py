from decimal import Decimal
from functools import cached_property

from apps.store.models.delivery import FoodDelivery
from .exceptions import HasNoActiveDelivery
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response


class NearestDeliveryMixin:
    @cached_property
    def delivery(self):
        delivery = FoodDelivery.get_nearest_delivery()
        if delivery is None:
            raise HasNoActiveDelivery
        else:
            return delivery


class DataPreparedUpdateModelMixin(UpdateModelMixin):
    """
    Customized mixin for update a model instance with data preparing.
    """

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=self.get_prepared_data(request.data), partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    @staticmethod
    def get_prepared_data(data):
        patched_data = dict(data)
        if patched_data:
            product_item_value = data.get("value")
            if product_item_value and not isinstance(product_item_value, Decimal):
                if "," in product_item_value:
                    product_item_value = product_item_value.replace(",", ".")
                patched_data["value"] = Decimal(product_item_value)
        return patched_data
