from abc import ABC, abstractmethod
from urllib.parse import ParseResult

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from core import settings


class BaseView(ABC, LoginRequiredMixin, TemplateView):
    """
    Need to implement in child class property
    called "left_sidebar_menu_items" which get list with menu items like below:

    @property
    def left_sidebar_menu_items(self):
        return [
            MenuItem(title="Мои продукты", link=reverse("farmer:foodstuffs"), icon="fab fa-pagelines"),
            MenuItem(title="Заказы", link=reverse("farmer:orders"), icon="fas fa-shopping-basket"),
        ]

    """

    @property
    @abstractmethod
    def left_sidebar_menu_items(self):
        pass

    def get_selected_left_menu_item(self, request):
        return request.path

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["left_sidebar_menu_items"] = self.left_sidebar_menu_items
        context["selected_left_menu_item"] = self.get_selected_left_menu_item(self.request)
        tg_link = settings.TELEGRAM_CHANNEL_LINK
        context["telegram_link"] = tg_link.geturl() if isinstance(tg_link, ParseResult) else None
        return context
