from rest_framework import serializers

from ..models import FarmerProfile


class FarmerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmerProfile
        fields = ['id', 'photo', 'phone', 'region', 'name']
