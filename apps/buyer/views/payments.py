import profile

from apps.buyer.models import balance
from apps.buyer.models import profile
from apps.buyer.views import BuyerBasePagesView
from apps.store.models import delivery
from apps.store.models.order import FoodOrder, ORDER_STATE


class BuyerOrders(BuyerBasePagesView):
    template_name = 'buyer/pages/payments.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        user_id = self.request.user.pk
        orders_queryset = FoodOrder.objects.filter(
            buyer__user_id=user_id,
            state__in=ORDER_STATE.get_state_names_greater_than_or_equal_to(ORDER_STATE.awaiting_processing)
        )
        buyer_profile = profile.BuyerProfile.objects.get(user_id=user_id)
        buyer_delivery = delivery.FoodDelivery.objects.filter(order__buyer__user_id=user_id)
        context['nearest_delivery'] = delivery.FoodDelivery.nearest_delivery(buyer_delivery)
        context['orders'] = orders_queryset
        context['total'] = balance.BuyerBalance.get_total_balance(buyer_profile=buyer_profile)
        return context
