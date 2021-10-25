from rest_framework import serializers

from apps.store.models.order_item import FoodOrderItem
from apps.store.models.location import Location


class FoodOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodOrderItem
        fields = ['value']


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        exclude = ('office_name', 'location_type', 'city_district', 'sort_key', 'user')
