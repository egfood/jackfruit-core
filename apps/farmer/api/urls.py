from django.urls import path

from .endpoints import FarmerProfileEndpoint, FeedbackCreationEndpoint

app_name = 'farmer-api'

urlpatterns = [
    path('profile/<int:pk>', FarmerProfileEndpoint.as_view(), name='profile'),
    path('order-item/<int:order_item_pk>/feedback/', FeedbackCreationEndpoint.as_view(), name='estimate-feedback'),
]
