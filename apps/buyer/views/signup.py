from django.views.generic import TemplateView


class BuyerSignupView(TemplateView):
    template_name = 'buyer/pages/buyer-signup.html'

#TODO: After login/logout implementation the view must be decorated login_required
class BuyerWelcomeView(TemplateView):
    template_name = 'buyer/pages/buyer-welcome.html'