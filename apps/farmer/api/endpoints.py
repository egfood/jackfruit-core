from rest_framework.generics import CreateAPIView, get_object_or_404 as drf_get_object_or_404
from rest_framework import serializers

from apps.store.models.order_item import FoodOrderItem
from core.api.basic_endpoint import ProfileEndpoint
from .serializers import FarmerProfileSerializer, FarmerFeedbackSerializer
from ..models.profile import FarmerProfile


class FarmerProfileEndpoint(ProfileEndpoint):
    serializer_class = FarmerProfileSerializer
    profile_class = FarmerProfile


class FeedbackCreationEndpoint(CreateAPIView):
    serializer_class = FarmerFeedbackSerializer

    def perform_create(self, serializer):
        order_item_pk = self.kwargs.get('order_item_pk')
        order_item = drf_get_object_or_404(FoodOrderItem.objects.all(), pk=order_item_pk)
        feedback = self.serializer_class.Meta.model.objects.filter(order_item=order_item).first()
        if feedback:
            raise serializers.ValidationError({"detail": "Ваш отзыв уже был успешно отправлен ранее!"})
        serializer.save(order_item=order_item)
