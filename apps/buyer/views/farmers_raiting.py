from django.conf import settings
from .base import BuyerBasePagesView
from apps.farmer.models.profile import FarmerProfile


class BuyerFarmersRatingView(BuyerBasePagesView):
    template_name = 'buyer/pages/farmers-rating.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['farmers'] = FarmerProfile.objects.all()
        context['max_rating'] = settings.MAX_PRODUCT_RATING
        return context
