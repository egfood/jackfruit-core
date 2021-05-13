from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from apps.farmer.forms.profile import FarmerProfileForm
from apps.farmer.models import FarmerProfile
from core.forms.user import UserCreationForm
from core.models import GreenUser


#
# def signup(request):
#     form = UserCreationForm(request.POST)
#     username = form.set_email(form.cleaned_data['email'])
#     pas = form.set_password(form.cleaned_data['password1'])
#     user = authenticate(username=username, password=pas)
#     login(request, user)

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


# TODO: After login/logout implementation the view must be decorated login_required
class FarmerWelcomeView(CreateView):
    template_name = 'farmer/pages/farmer-welcome.html'
    model = FarmerProfile
    form_class = FarmerProfileForm
    success_url = reverse_lazy('farmer:main_page')

    # @method_decorator(login_required)
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(FarmerWelcomeView, self).form_valid(form)
    # def post(self, request, *args, **kwargs):
    #     form = self.form_class(request.POST)
    #     if request.user.is_authenticated:
    #         UserProfile.user_id = request.user.id
    #         form.save()
    #     else:
    #         redirect(reverse_lazy('farmer:signup'))
# Do something for anonymous users.
