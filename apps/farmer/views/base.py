# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.urls import reverse
# from django.views.generic import TemplateView
#
#
# class FarmerBasePagesView(LoginRequiredMixin, TemplateView):
#     login_url = '/login/'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['app_home_url'] = reverse('farmer:main_page')
#         return context