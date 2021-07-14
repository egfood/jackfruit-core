from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse

from core.menu_data import MenuItem
from core.views.base import BaseView


class BuyerBasePagesView(BaseView, LoginRequiredMixin):
    login_url = '/login/'

    # This property is using by BaseView for menu generation
    @property
    def left_sidebar_menu_items(self):
        return [
            MenuItem(title="Витрина", link=reverse("buyer:home"), icon="fas fa-store"),
            MenuItem(title="Корзина", link=reverse("buyer:cart"), icon="fas fa-shopping-basket"),
            MenuItem(title="Платежи", link=reverse("buyer:home"), icon="fas fa-money-bill-wave-alt"),
            MenuItem(title="Рейтинг фермеров", link=reverse("buyer:home"), icon="fas fa-star"),
        ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['app_home_url'] = reverse('buyer:home')
        return context
