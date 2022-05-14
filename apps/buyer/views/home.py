from django.views.generic.base import RedirectView


class BuyerHomeView(RedirectView):
    url = 'cart'