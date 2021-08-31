from django.urls import path

from .endpoints import BuyerProfileEndpoint

app_name = 'buyer-api'

urlpatterns = [
    path('profile/<int:pk>', BuyerProfileEndpoint.as_view(), name='profile'),
]
