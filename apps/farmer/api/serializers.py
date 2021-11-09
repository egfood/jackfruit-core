from rest_framework import serializers

from ..models.feedback import FarmerFeedback
from ..models.profile import FarmerProfile


class FarmerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmerProfile
        fields = ['photo', 'phone', 'region', 'name', 'service_zone', 'legal_name']


class FarmerFeedbackSerializer(serializers.ModelSerializer):
    order_item = serializers.HiddenField(default=None)

    class Meta:
        model = FarmerFeedback
        fields = ('order_item', 'rating', 'feedback')
