from django.views.generic import TemplateView

from apps.buyer.views import BuyerBasePagesView


class ProfileView(BuyerBasePagesView, TemplateView):
    template_name = 'buyer/pages/profile.html'
