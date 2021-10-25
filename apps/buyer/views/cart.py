from django.conf import settings

from apps.store.models.delivery import FoodDelivery
from apps.store.models.order_item import FoodOrderItem
from core.views.mixins import PaginationMixin
from .base import BuyerBasePagesView
from ..forms.order import BuyerFoodOrderForm


class BuyerCartView(BuyerBasePagesView, PaginationMixin):
    template_name = 'buyer/pages/buyer-cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['delivery'] = FoodDelivery.get_nearest_delivery()
        order_items, order = FoodOrderItem.get_buyer_cart_items(self.request, context['delivery'])
        context['page'], context['order_items'] = self.get_paginate_page_and_subjects(
            order_items, settings.COUNT_OF_CART_PRODUCTS_PER_PAGE
        )
        context['order_total'] = FoodOrderItem.get_buyer_cart_total(self.request.user.profile, context['delivery'])
        context['order_form'] = BuyerFoodOrderForm(instance=order)
        return context
