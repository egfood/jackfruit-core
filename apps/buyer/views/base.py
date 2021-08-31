from django.conf import settings
from django.contrib import messages
from django.urls import reverse

from core.menu_data import MenuItem
from core.views.base import BaseView
from ..forms.profile import BuyerAreaProfileForm
from ..models.balance import BuyerBalance


class BuyerBasePagesView(BaseView):
    login_url = '/login/'

    # This property is using by BaseView for menu generation
    @property
    def left_sidebar_menu_items(self):
        return [
            MenuItem(title="Витрина", link=reverse("buyer:home"), icon="fas fa-store"),
            MenuItem(title="Корзина", link=reverse("buyer:cart"), icon="fas fa-shopping-basket"),
            MenuItem(title="Платежи", link=reverse("buyer:home"), icon="fas fa-money-bill-wave-alt"),
            MenuItem(title="Фермеры", link=reverse("buyer:farmers-rating"), icon="fas fa-star"),
        ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['app_home_url'] = reverse('buyer:home')
        if hasattr(self.request.user, 'profile'):
            profile = self.request.user.profile
            context['buyer_profile_api_url'] = reverse('buyer-api:profile',
                                                       kwargs={'pk': profile.id})
            context['buyer_profile_form'] = BuyerAreaProfileForm(instance=profile)
            context['buyer_balance'] = BuyerBalance.get_total_balance(profile)
            context['CURRENT_CURRENCY'] = settings.CURRENT_CURRENCY
            context['BUYER_BALANCE_VALUE_HINT1'] = settings.BUYER_BALANCE_VALUE_HINT1
            context['BUYER_BALANCE_VALUE_HINT2'] = settings.BUYER_BALANCE_VALUE_HINT2
        else:
            messages.error(self.request, 'Buyer profile can not found.')
        return context
