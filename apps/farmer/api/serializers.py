from rest_framework import serializers

from ..models.feedback import FarmerFeedback
from ..models.profile import FarmerProfile


class FarmerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmerProfile
        fields = ['photo', 'phone', 'region', 'name', 'service_zone', 'legal_name']


class FarmerFeedbackSerializer(serializers.ModelSerializer):
    order_item = serializers.HiddenField(default=None)
    rating = serializers.IntegerField(required=True, max_value=5, min_value=1)
    feedback = serializers.CharField(required=True)

    class Meta:
        model = FarmerFeedback
        fields = ('order_item', 'rating', 'feedback')
