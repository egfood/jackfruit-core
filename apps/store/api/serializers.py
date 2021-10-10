from rest_framework import serializers

from apps.store.models.order_item import FoodOrderItem


class FoodOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodOrderItem
        fields = ['value']
