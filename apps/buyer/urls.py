from django.urls import path, register_converter

from .converters import PlaceOfDelivery
from .views import *

app_name = 'buyer'

register_converter(PlaceOfDelivery, 'places_of_delivery')

urlpatterns = [
    path('', BuyerHomeView.as_view(), name='home'),
    path('order/delivery/<int:delivery_pk>/office', BuyerOfficeOrderByDeliveryView.as_view(),
         name='office_order_by_delivery'),
    path('order/delivery/<int:delivery_pk>/home', BuyerHomeOrderByDeliveryView.as_view(),
         name='home_order_by_delivery'),
    path('profile', ProfileView.as_view(),
         name='buyer_profile'),
]
