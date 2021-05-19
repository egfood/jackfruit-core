from .base import BuyerBasePagesView


class BuyerCartView(BuyerBasePagesView):
    template_name = 'buyer/pages/buyer-cart.html'
