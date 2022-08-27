from django.views.generic import TemplateView

from telegram import get_tg_link


class HomeView(TemplateView):
    template_name = "core/pages/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["telegram_link"] = get_tg_link()
        return context
