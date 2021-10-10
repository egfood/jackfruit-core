from rest_framework.generics import RetrieveUpdateDestroyAPIView

from apps.store.models.delivery import FoodDelivery
from apps.store.models.order_item import FoodOrderItem
from .exceptions import HasNoActiveDelivery
from .serializers import FoodOrderItemSerializer


class OrderItemByFarmerProductEndpoint(RetrieveUpdateDestroyAPIView):
    serializer_class = FoodOrderItemSerializer
    lookup_url_kwarg = 'farmer_product_pk'
    lookup_field = 'product__pk'

    def get_queryset(self):
        delivery = FoodDelivery.get_nearest_delivery()
        if delivery is None:
            raise HasNoActiveDelivery
        return FoodOrderItem.get_buyer_cart_items(self.request, delivery, need_order_creation=True)
