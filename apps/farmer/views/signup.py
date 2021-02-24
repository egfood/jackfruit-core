from django.views.generic import TemplateView


class FarmerSignupView(TemplateView):
    template_name = 'farmer/pages/farmer-signup.html'

#TODO: After login/logout implementation the view must be decorated login_required
class FarmerWelcomeView(TemplateView):
    template_name = 'farmer/pages/farmer-welcome.html'
