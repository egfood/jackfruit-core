from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse

from core.menu_data import MenuItem
from core.views.base import BaseView
from ..forms.profile import FarmerAreaProfileForm


class FarmerBasePagesView(BaseView, LoginRequiredMixin):
    login_url = '/login/'

    # This property is using by BaseView for menu generation
    @property
    def left_sidebar_menu_items(self):
        return [
            MenuItem(title="Мои продукты", link=reverse("farmer:foodstuffs"), icon="fab fa-pagelines"),
            # MenuItem(title="Заказы", link=reverse("farmer:orders"), icon="fas fa-shopping-basket"),
            MenuItem(title="Мои продажи", link=reverse("farmer:payments"), icon="fas fa-money-bill-wave-alt"),
            MenuItem(title="Мой рейтинг", link=reverse("farmer:foodstuffs"), icon="fas fa-star"),
        ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['app_home_url'] = reverse('farmer:foodstuffs')
        if hasattr(self.request.user, 'profile'):
            context['farmer_profile_api_url'] = reverse('farmer-api:profile',
                                                        kwargs={'pk': self.request.user.profile.id})
            context['farmer_profile_form'] = FarmerAreaProfileForm(instance=self.request.user.profile)
        else:
            messages.error(self.request, 'Farmer profile can not found.')
        return context
