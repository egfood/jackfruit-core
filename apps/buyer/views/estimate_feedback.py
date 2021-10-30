from apps.buyer.views import BuyerBasePagesView
from apps.store.models import order_item, order
from apps.buyer.forms import estimate_feedback


class BuyerOrdersFeedback(BuyerBasePagesView):
    template_name = 'buyer/pages/estimate-feedback.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        order_item_queryset = order_item.FoodOrderItem.objects.filter(order_id=kwargs['order_id'])
        this_order = order.FoodOrder.objects.get(pk=kwargs['order_id'])
        context['order'] = this_order
        context['order_item'] = order_item_queryset
        context['form_feedback'] = estimate_feedback.EstimateFeedbackForm
        return context
