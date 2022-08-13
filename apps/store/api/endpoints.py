from functools import cached_property

from django.db.models import Q
from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView, ListCreateAPIView, RetrieveUpdateAPIView, get_object_or_404 as drf_get_object_or_404
)
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.store.models.order import FoodOrder
from apps.store.models.order_item import FoodOrderItem
from .mixins import NearestDeliveryMixin
from .serializers import FoodOrderItemSerializer, LocationSerializer, FoodOrderSerializer
from ..models.location import LocationStatus


class OrderEndpoint(RetrieveUpdateAPIView, NearestDeliveryMixin):
    serializer_class = FoodOrderSerializer

    def get_object(self):
        queryset_kwargs = {
            'buyer': self.request.user.profile,
            'delivery': self.delivery
        }
        queryset = self.serializer_class.Meta.model.objects.all()
        obj = drf_get_object_or_404(queryset, **queryset_kwargs)
        return obj

    def perform_update(self, serializer):
        serializer.save(state=self.serializer_class.Meta.model.ORDER_STATE.awaiting_processing.name)


class OrderItemByFarmerProductEndpoint(RetrieveUpdateDestroyAPIView, NearestDeliveryMixin):
    serializer_class = FoodOrderItemSerializer
    lookup_url_kwarg = 'farmer_product_pk'
    lookup_field = 'product__pk'

    def get_queryset(self):
        result, _ = FoodOrderItem.get_buyer_cart_items(self.request, self.delivery, need_order_creation=True)
        return result

    def get_object(self):
        """
        Returns the object the view is displaying.
        You may want to override this if you need to provide non-standard
        queryset lookups.  Eg if objects are referenced using multiple
        keyword arguments in the url conf.
        """
        queryset = self.filter_queryset(self.get_queryset())

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
                'Expected view %s to be called with a URL keyword argument '
                'named "%s". Fix your URL conf, or set the `.lookup_field` '
                'attribute on the view correctly.' %
                (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}

        if self.request.method in ('PUT'):
            obj, _ = queryset.get_or_create(**self._get_defaults_for_order_item(self.kwargs[lookup_url_kwarg]))
        else:
            obj = drf_get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj

    def _get_defaults_for_order_item(self, farmer_product_pk):
        order_args = {
            'delivery': self.delivery,
            'buyer': self.request.user.profile
        }
        order, _ = FoodOrder.objects.get_or_create(**order_args)
        return {'order': order, 'product_id': farmer_product_pk, }


class LocationEndpoint(ListCreateAPIView, UpdateModelMixin):
    serializer_class = LocationSerializer

    def get_queryset(self):
        is_added_location_type = self.request.query_params.get("add_location_type")

        # Need to refactoring by pattern matching from Python 3.10
        qs_filter = Q(user=self.request.user)
        if is_added_location_type == LocationStatus.office.name:
            qs_filter = qs_filter | Q(location_type=LocationStatus.office.name)

        return self.serializer_class.Meta.model.objects.filter(qs_filter)


class OrderTotalEndpoint(APIView, NearestDeliveryMixin):
    def get(self, request):
        order = FoodOrder.get_order(delivery=self.delivery, buyer=self.request.user)
        return Response(order.total_cost)
