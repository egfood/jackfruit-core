from rest_framework import serializers

from apps.store.models.location import Location
from apps.store.models.order_item import FoodOrderItem


class FoodOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodOrderItem
        fields = ['value']


class LocationSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Location
        fields = ('id', 'get_short_address', 'user', 'location_type', 'name', 'phone', 'office_name', 'office_name',
                  'city_type', 'city_value', 'city_district', 'street_type', 'street_value', 'building', 'porch',
                  'floor', 'room')
