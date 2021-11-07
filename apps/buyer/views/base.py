from functools import cached_property

from django.conf import settings
from django.urls import reverse

from apps.store.models.delivery import FoodDelivery
from apps.store.models.location import Location
from apps.store.models.order_item import FoodOrderItem
from core.menu_data import MenuItem
from core.views.base import BaseView
from ..forms.location import BuyerLocationForm
from ..forms.profile import BuyerAreaProfileForm
from ..models.balance import BuyerBalance


class BuyerBasePagesView(BaseView):
    login_url = '/login/'

    @cached_property
    def buyer_profile(self):
        return self.request.user.profile

    @cached_property
    def nearest_delivery(self):
        return FoodDelivery.get_nearest_delivery()

    @cached_property
    def cart_items_count(self):
        return FoodOrderItem.get_buyer_cart_items_count(self.buyer_profile, self.nearest_delivery)

    # This property is using by BaseView for menu generation
    @property
    def left_sidebar_menu_items(self):
        return [
            MenuItem(title="Витрина", link=reverse("buyer:storefront"), icon="fas fa-store"),
            MenuItem(
                title="Корзина", link=reverse("buyer:cart"), icon="fas fa-shopping-basket",
                counter=self.cart_items_count
            ),
            MenuItem(title="Мои Заказы", link=reverse("buyer:payments"), icon="fas fa-money-bill-wave-alt"),
            MenuItem(title="Фермеры", link=reverse("buyer:farmers-rating"), icon="fas fa-star"),
        ]

    def get_context_data(self, **kwargs):
        if not hasattr(self.request.user, 'profile'):
            raise ValueError('Buyer profile can not found.')

        context = super().get_context_data(**kwargs)
        context['app_home_url'] = reverse('buyer:home')
        context['location_form'] = BuyerLocationForm()
        context['buyer_locations'] = Location.get_user_locations(self.request.user)
        context['buyer_profile_api_url'] = reverse('buyer-api:profile', kwargs={'pk': self.buyer_profile.id})
        context['buyer_profile_form'] = BuyerAreaProfileForm(instance=self.buyer_profile)
        context['buyer_balance'] = BuyerBalance.get_total_balance(self.buyer_profile)
        context['cart_total'] = FoodOrderItem.get_buyer_cart_total(self.buyer_profile, self.nearest_delivery)
        context['cart_items_count'] = self.cart_items_count
        context['CURRENT_CURRENCY'] = settings.CURRENT_CURRENCY
        context['BUYER_BALANCE_VALUE_HINT1'] = settings.BUYER_BALANCE_VALUE_HINT1
        context['BUYER_BALANCE_VALUE_HINT2'] = settings.BUYER_BALANCE_VALUE_HINT2
        return context
