from abc import abstractmethod, ABC

from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated


class ProfileEndpoint(ABC, RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]

    @property
    @abstractmethod
    def profile_class(self):
        pass

    def get_queryset(self):
        qs = self.profile_class.objects.all()
        logged_in_user_profile = qs.filter(user=self.request.user)
        return logged_in_user_profile

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj
