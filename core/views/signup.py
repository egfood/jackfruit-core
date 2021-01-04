from django import forms
from django.contrib import messages
from django.db import transaction
from django.shortcuts import render
from django.views.generic import TemplateView

from core.forms.profile import UserProfileForm
from core.forms.user import UserCreationForm
from core.models import UserWithProfileManager


class SignupView(TemplateView):
    template_name = 'core/pages/signup.html'
    user_manager = UserWithProfileManager()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_creation_form'] = UserCreationForm()
        context['user_creation_profile_form'] = UserProfileForm()
        return context

    def post(self, request, *args, **kwargs):
        user_creation_form = UserCreationForm(request.POST)
        user_creation_profile_form = UserProfileForm(request.POST)
        if user_creation_form.is_valid() and user_creation_profile_form.is_valid():
            self.create_user_with_profile_by_form(user_creation_form)
            messages.success(self.request, 'Вы успешно зарегистрированы. Ожидайте активации аккаунта администратором.')
        return render(request, self.template_name, {'user_creation_form': user_creation_form,
                                                    'user_creation_profile_form': user_creation_profile_form})

    @transaction.atomic
    def create_user_with_profile_by_form(self, user_creation_form: forms.ModelForm):
        prepared_user_data = {
            'password': user_creation_form.cleaned_data.pop('password1'),
            **user_creation_form.cleaned_data,
        }
        del prepared_user_data['password2']
        self.user_manager.create_user_with_profile(**prepared_user_data)
