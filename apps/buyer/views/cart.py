from django.conf import settings

from apps.store.models.delivery import FoodDelivery
from apps.store.models.order_item import FoodOrderItem
from apps.store.models.location import Location
from core.views.mixins import PaginationMixin
from .base import BuyerBasePagesView
from ..forms.order import BuyerFoodOrderForm


class BuyerCartView(BuyerBasePagesView, PaginationMixin):
    template_name = 'buyer/pages/buyer-cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['delivery'] = FoodDelivery.get_nearest_delivery()
        order_items, order = FoodOrderItem.get_buyer_cart_items(self.request, context['delivery'])
        context['order'] = order
        context['order_total'] = FoodOrderItem.get_buyer_cart_total(self.request.user.profile, context['delivery'])
        if order and not order.is_order_sent_by_user:
            context['page'], context['order_items'] = self.get_paginate_page_and_subjects(
                order_items, settings.COUNT_OF_CART_PRODUCTS_PER_PAGE
            )
            order_form_kwargs = {
                "instance": order,
                "initial": {"location": Location(name="<Выберите адрес>")} if order.location is None else None
            }
            context['order_form'] = BuyerFoodOrderForm(**order_form_kwargs)
        return context
