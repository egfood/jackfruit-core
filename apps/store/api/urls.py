from django.urls import path

from .endpoints import (
    OrderItemByFarmerProductEndpoint, LocationEndpoint, OrderEndpoint, OrderTotalEndpoint, OrderTotalCountEndpoint,
)

app_name = 'store-api'

urlpatterns = [
    path(
        'order-item/by/farmer-product/<int:farmer_product_pk>', OrderItemByFarmerProductEndpoint.as_view(),
        name='order-item'
    ),
    path('location', LocationEndpoint.as_view(), name='location'),
    path('order', OrderEndpoint.as_view(), name='order'),
    path('order/total', OrderTotalEndpoint.as_view(), name='order_total'),
    path('order/total-count', OrderTotalCountEndpoint.as_view(), name='order_total_count'),
]
