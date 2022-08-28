from rest_framework import serializers

from apps.store.models.location import Location
from apps.store.models.order import FoodOrder, ORDER_STATE
from apps.store.models.order_item import FoodOrderItem


class FoodOrderSerializer(serializers.ModelSerializer):
    # state = serializers.HiddenField(default=ORDER_STATE.created)

    class Meta:
        model = FoodOrder
        fields = ['state', 'location', 'payment_type', 'total_cost', 'delivery_cost']

    def get_total_cost(self, instance):
        return instance.total_cost


class FoodOrderItemSerializer(serializers.ModelSerializer):
    item_total = serializers.SerializerMethodField()

    class Meta:
        model = FoodOrderItem
        fields = ['value', 'item_total']

    def get_item_total(self, instance):
        return instance.item_total


class LocationSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Location
        fields = (
            'id', 'short_address', 'full_address', 'user', 'location_type', 'name', 'phone', 'office_name',
            'office_name',
            'city_type', 'city_value', 'city_district', 'street_type', 'street_value', 'building', 'porch',
            'floor', 'room')
