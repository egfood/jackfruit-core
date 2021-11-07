from django.urls import path

from apps.farmer.views import *

app_name = 'farmer'

urlpatterns = [
    path('signup', FarmerSignupView.as_view(), name='signup'),
    path('welcome', FarmerWelcomeView.as_view(), name='welcome'),
    path('', FarmerFoodstuffsPageView.as_view(), name='foodstuffs'),
    path('payments/', FarmerOrdersView.as_view(), name='payments'),
    # path('add-product/', AddProductView.as_view(), name='add_product'),
    # path('delete-product/<int:pk>', DeleteProductView.as_view(), name='delete_product'),
    # path('update-product/<int:pk>', UpdateProductView.as_view(), name='update_product'),
]
