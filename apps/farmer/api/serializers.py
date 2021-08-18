from rest_framework import serializers

from ..models.profile import FarmerProfile


class FarmerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmerProfile
        fields = ['photo', 'phone', 'region', 'name', 'service_zone', 'legal_name']
