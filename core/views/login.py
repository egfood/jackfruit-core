from django.conf import settings
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.shortcuts import resolve_url

from core.forms.login import AuthenticationUserForm


class CustomLoginView(LoginView):
    template_name = 'core/pages/login.html'
    authentication_form = AuthenticationUserForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['version'] = settings.VERSION
        return context

    def get_success_url(self):
        # TODO: need fix redirect by 'next' GET param (see django.contrib.auth.views.LoginView.get_redirect_url())
        user = self.request.user
        if user.is_superuser:
            return resolve_url("admin:index")
        try:
            getattr(user, "profile")
        except AttributeError as e:
            messages.error(self.request, 'Профиль не найден. Обратитесь к администратору.')
            return resolve_url("login")
        else:
            view_name = "farmer:foodstuffs" if user.is_farmer else "buyer:home"
            return resolve_url(view_name)
