from django.urls import path

from .endpoints import OrderItemByFarmerProductEndpoint, LocationEndpoint, OrderEndpoint

app_name = 'store-api'

urlpatterns = [
    path(
        'order-item/by/farmer-product/<int:farmer_product_pk>', OrderItemByFarmerProductEndpoint.as_view(),
        name='order-item'
    ),
    path('location', LocationEndpoint.as_view(), name='location'),
    path('order', OrderEndpoint.as_view(), name='order'),
]
