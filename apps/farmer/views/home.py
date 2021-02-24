# from django.urls import reverse
# from django.views.generic import ListView
#
# from apps.store.models import FoodProduct
#
#
# class MainFarmerPageView(ListView):
#     template_name = "farmer/pages/main_farmer.html"
#     model = FoodProduct
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['app_home_url'] = reverse('farmer:main_page')
#         context['user'] = self.request.user
#         return context
