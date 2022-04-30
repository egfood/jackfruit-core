import core.settings

from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views.generic import CreateView

from apps.buyer.forms.profile import BuyerSignupProfileForm
from apps.buyer.models.profile import BuyerProfile
from core.forms.user import UserCreationForm
from core.models import GreenUser
from core.views import captcha_label


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['captcha_label'] = captcha_label()
        return context

# TODO: After login/logout implementation the view must be decorated login_required
class BuyerWelcomeView(CreateView):
    template_name = 'buyer/pages/buyer-welcome.html'
    model = BuyerProfile
    form_class = BuyerSignupProfileForm
    success_url = reverse_lazy('buyer:home')

    # @method_decorator(login_required)
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(BuyerWelcomeView, self).form_valid(form)
    # def post(self, request, *args, **kwargs):
    #     form = self.form_class(request.POST)
    #     if request.user.is_authenticated:
    #         UserProfile.user_id = request.user.id
    #         form.save()
    #     else:
    #         redirect(reverse_lazy('farmer:signup'))
# Do something for anonymous users.
