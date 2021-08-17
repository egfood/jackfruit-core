from .base import BuyerBasePagesView
from ...farmer.models import FarmerRating


class BuyerFarmersRatingView(BuyerBasePagesView):
    template_name = 'buyer/pages/farmers-rating.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ratings'] = FarmerRating.objects.all()
        return context
