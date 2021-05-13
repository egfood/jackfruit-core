from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import resolve_url
# from django.urls import reverse_lazy

from core.models import UserProfile
from django.conf import settings
from core.forms.login import AuthenticationUserForm


class CustomLoginView(LoginView):
    template_name = 'core/pages/login.html'
    authentication_form = AuthenticationUserForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['version'] = settings.VERSION
        return context

    # def get_success_url(self):
    #     # TODO: need fix redirect by 'next' GET param (see django.contrib.auth.views.LoginView.get_redirect_url())
    #     user_profile = UserProfile.objects.filter(user=self.request.user).first()
    #     if user_profile is not None:
    #         view_name = "farmer:main_page" if user_profile.is_supplier else "buyer:home"
    #     else:
    #         messages.error(self.request, 'Профиль не найден. Обратитесь к администратору.')
    #         view_name = "login"
    #     return resolve_url(view_name)
