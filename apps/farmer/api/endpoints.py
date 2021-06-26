from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated

from .serializers import FarmerProfileSerializer
from ..models import FarmerProfile


class FarmerProfileEndpoint(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FarmerProfileSerializer

    def get_queryset(self):
        qs = FarmerProfile.objects.all()
        logged_in_user_profile = qs.filter(user=self.request.user)
        return logged_in_user_profile

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj