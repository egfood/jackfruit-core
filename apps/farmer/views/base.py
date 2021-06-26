from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import TemplateView

from ..forms.profile import FarmerAreaProfileForm


class FarmerBasePagesView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'

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
