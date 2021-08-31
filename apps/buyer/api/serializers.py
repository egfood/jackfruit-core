from rest_framework import serializers

from ..models.profile import BuyerProfile


class BuyerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyerProfile
        fields = "__all__"
