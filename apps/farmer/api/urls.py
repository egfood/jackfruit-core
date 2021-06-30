from django.urls import path

from .endpoints import FarmerProfileEndpoint

app_name = 'farmer-api'

urlpatterns = [
    path('profile/<int:pk>', FarmerProfileEndpoint.as_view(), name='profile'),
]