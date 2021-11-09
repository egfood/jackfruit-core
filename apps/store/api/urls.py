from django.urls import path

from .endpoints import OrderItemByFarmerProductEndpoint, LocationEndpoint, SubmitOrderEndpoint

app_name = 'store-api'

urlpatterns = [
    path(
        'order-item/by/farmer-product/<int:farmer_product_pk>', OrderItemByFarmerProductEndpoint.as_view(),
        name='order-item'
    ),
    path('location', LocationEndpoint.as_view(), name='location'),
    path('order/submit', SubmitOrderEndpoint.as_view(), name='order-submit'),
]
