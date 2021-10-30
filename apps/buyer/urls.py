from django.urls import path, register_converter

from .converters import PlaceOfDelivery
from .views import *

app_name = 'buyer'

register_converter(PlaceOfDelivery, 'places_of_delivery')

urlpatterns = [
    path('signup', BuyerSignupView.as_view(), name='signup'),
    path('welcome', BuyerWelcomeView.as_view(), name='welcome'),
    path('cart', BuyerCartView.as_view(), name='cart'),
    path('farmers-rating', BuyerFarmersRatingView.as_view(), name='farmers-rating'),
    path('storefront', BuyerStorefrontAllProductsView.as_view(), name='storefront'),
    path('storefront/category/<int:category_pk>', BuyerStorefrontByProductCategoryView.as_view(),
         name='storefront-by-category'),
    path('', BuyerHomeView.as_view(), name='home'),
    path('payments/', BuyerOrders.as_view(), name='payments'),
    path('payments/estimate-feedback/<int:order_id>/', BuyerOrdersFeedback.as_view(), name='estimate_feedback')
]
