from .base import BuyerBasePagesView
from apps.farmer.models.feedback import FarmerFeedback


class BuyerFarmersRatingView(BuyerBasePagesView):
    template_name = 'buyer/pages/farmers-rating.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ratings'] = FarmerFeedback.objects.all()
        return context
