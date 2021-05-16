from .base import FarmerBasePagesView


class FarmerFoodstuffsPageView(FarmerBasePagesView):
    template_name = "farmer/pages/farmer-foodstuffs.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context