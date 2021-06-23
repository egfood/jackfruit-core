from .base import BuyerBasePagesView


class BuyerCartView(BuyerBasePagesView):
    template_name = 'buyer/pages/buyer-cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
