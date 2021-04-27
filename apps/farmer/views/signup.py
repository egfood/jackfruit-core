from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.utils.decorators import method_decorator

from django.views.generic.edit import CreateView

from core.models import GreenUser
from core.forms.user import UserCreationForm
from core.forms.profile import UserProfileForm
from core.models import UserProfile
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

    def post(self, request, *args, **kwargs):
        form = UserCreationForm(request.POST)
        # form.save()
        if form.is_valid():
            username = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
        form.save()
        return super().post(request, *args, **kwargs)


#TODO: After login/logout implementation the view must be decorated login_required
class FarmerWelcomeView(CreateView):
    template_name = 'farmer/pages/farmer-welcome.html'
    model = UserProfile
    form_class = UserProfileForm
    success_url = reverse_lazy('farmer:main_farmer')

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

