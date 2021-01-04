from django.urls import path

from apps.farmer.views import *

app_name = 'farmer'

urlpatterns = [
    path('', MainFarmerPageView.as_view(), name='main_page'),
    path('add-product/', AddProductView.as_view(), name='add_product'),
    path('delete-product/<int:pk>', DeleteProductView.as_view(), name='delete_product'),
    path('update-product/<int:pk>', UpdateProductView.as_view(), name='update_product'),
]
