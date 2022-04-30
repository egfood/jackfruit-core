from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

import core.settings
from apps.farmer.forms.profile import FarmerSignupProfileForm
from apps.farmer.models.profile import FarmerProfile
from core.forms.user import UserCreationForm
from core.models import GreenUser
from core.views import captcha_label


class FarmerSignupView(CreateView):
    template_name = 'farmer/pages/farmer-signup.html'
    model = GreenUser
    form_class = UserCreationForm
    success_url = reverse_lazy('farmer:welcome')

    def form_valid(self, form):
        # super().form_valid need to execute in first because the method required form after save
        http_response = super().form_valid(form)
        user = authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password1'])
        if user is not None:
            login(self.request, user)
        else:
            http_response = super().form_invalid(form)
        return http_response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['captcha_label'] = captcha_label()
        return context


# TODO: After login/logout implementation the view must be decorated login_required
class FarmerWelcomeView(CreateView):
    template_name = 'farmer/pages/farmer-welcome.html'
    model = FarmerProfile
    form_class = FarmerSignupProfileForm
    success_url = reverse_lazy('farmer:foodstuffs')

    # @method_decorator(login_required)
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(FarmerWelcomeView, self).form_valid(form)
