# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.urls import reverse
# from django.views.generic import TemplateView
#
# from apps.store.models import FoodDelivery
#
#
# class BuyerBasePagesView(LoginRequiredMixin, TemplateView):
#     login_url = '/login/'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         nearest_delivery = FoodDelivery.get_nearest_delivery()
#         context['nearest_delivery_pk'] = nearest_delivery.pk if nearest_delivery else None
#         context['app_home_url'] = reverse('buyer:home')
#         return context
