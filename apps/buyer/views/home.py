# from collections import namedtuple
# from itertools import chain
#
# from django.conf import settings
#
# from apps.store.models import FoodProduct, FoodDelivery, FoodHomeOrder, FoodOfficeOrder
from .base import BuyerBasePagesView
from django.views.generic.base import RedirectView


class BuyerHomeView(RedirectView, BuyerBasePagesView):
    url = 'cart'
    # template_name = 'buyer/pages/home.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['food_prices'] = FoodProduct.objects.filter(is_visible=True)
#         context['food_deliveries'] = self.__get_and_prepare_food_deliveries()
#         context['COUNT_ITEMS_ON_DELIVERY_DASHBOARD'] = settings.COUNT_ITEMS_ON_DELIVERY_DASHBOARD
#         return context
#
#     def __get_and_prepare_food_deliveries(self):
#         food_deliveries = FoodDelivery.objects.all().order_by('-date')[:settings.COUNT_ITEMS_ON_DELIVERY_DASHBOARD:-1]
#         home_orders_data = {
#             'delivery__in': food_deliveries,
#             'user': self.request.user
#         }
#         home_orders_by_deliveries = FoodHomeOrder.objects.filter(**home_orders_data).prefetch_related('home_order_item')
#         office_orders_data = {
#             'delivery__in': food_deliveries,
#             'user': self.request.user
#         }
#         office_orders_by_deliveries = FoodOfficeOrder.objects.filter(**office_orders_data).prefetch_related(
#             'office_order_item')
#         orders = list(chain(home_orders_by_deliveries, office_orders_by_deliveries))
#
#         ExtendedOrder = namedtuple('ExtendedOrder', ('total', 'order'))
#         extended_orders = {order.delivery.pk: ExtendedOrder(order.total, order) for order in orders}
#
#         updated_food_deliveries = []
#         for delivery in food_deliveries:
#             extended_order = extended_orders.get(delivery.pk, None)
#             delivery.order_total = extended_order.total if extended_order is not None else None
#
#             delivery.card_color = 'primary' if delivery.is_deactivated else 'success'
#             delivery.card_icon = 'fa-flag-checkered' if delivery.is_deactivated else 'fa-truck'
#             delivery.is_show_edit_button = self.__is_show_edit_button(delivery, extended_orders)
#             delivery.is_show_new_order_button = self.__is_show_new_order_button(delivery, extended_orders)
#             delivery.aggregated_state = self.__get_aggregated_delivery_and_order_state(delivery, extended_orders)
#
#             updated_food_deliveries.append(delivery)
#         return updated_food_deliveries
#
#     @staticmethod
#     def __get_aggregated_delivery_and_order_state(delivery: FoodDelivery, extended_orders: dict) -> str:
#         extended_order = extended_orders.get(delivery.pk, None)
#         order = extended_order.order if extended_order is not None else None
#         if order is None or delivery.state in ('finished', 'suspended', 'cancelled'):
#             return delivery.get_state_display()
#         else:
#             return order.get_state_display()
#
#     @staticmethod
#     def __is_show_edit_button(delivery: FoodDelivery, extended_orders: dict) -> bool:
#         extended_order = extended_orders.get(delivery.pk, None)
#         order = extended_order.order if extended_order is not None else None
#         if order is None:
#             return False
#         else:
#             if delivery.state in ('finished', 'suspended', 'cancelled') or \
#                     order.state in ('prepared', 'delivered', 'cancelled'):
#                 return False
#             else:
#                 return True
#
#     @staticmethod
#     def __is_show_new_order_button(delivery: FoodDelivery, extended_orders: dict) -> bool:
#         extended_order = extended_orders.get(delivery.pk, None)
#         order = extended_order.order if extended_order is not None else None
#         if order is None and delivery.state == 'collecting':
#             return True
#         else:
#             return False
