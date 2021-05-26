from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views.generic import CreateView

from core.forms.user import UserCreationForm
from core.models import GreenUser


class BuyerSignupView(CreateView):
    template_name = 'buyer/pages/buyer-signup.html'
    model = GreenUser
    form_class = UserCreationForm
    success_url = reverse_lazy('buyer:welcome')

    def form_valid(self, form):
        # super().form_valid need to execute in first because the method required form after save
        http_response = super().form_valid(form)
        user = authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password1'])
        if user is not None:
            login(self.request, user)
        else:
            http_response = super().form_invalid(form)
        return http_response

#TODO: After login/logout implementation the view must be decorated login_required
class BuyerWelcomeView(CreateView):
    template_name = 'buyer/pages/buyer-welcome.html'