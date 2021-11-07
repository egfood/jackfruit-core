from django.db.models import Sum
from itertools import groupby

from .base import FarmerBasePagesView
from apps.store.models import delivery, order_item, order
from apps.buyer.models import balance
from apps.farmer.models import product
from core.views.mixins import PaginationMixin


class FarmerOrdersView(FarmerBasePagesView, PaginationMixin):
    template_name = 'farmer/pages/payments.html'

    def payments_farmer(self):
        user_id = self.request.user.pk
        delivery_orders_queryset = delivery.FoodDelivery.objects.order_by('date').filter(
            order__order_item__product__farmer__user_id=user_id)
        result_list = []
        total = 0
        unique_delivery = [d for d, _ in groupby(delivery_orders_queryset)]
        for unique in unique_delivery:
            products_this_delivery = product.FarmerProduct.objects. \
                filter(farmer__user_id=user_id). \
                filter(order_item__order__delivery=unique)
            unique_products_this_delivery = {p for p in products_this_delivery}
            for prod in unique_products_this_delivery:
                product_item_delivery = order_item.FoodOrderItem.objects.filter(product=prod).filter(
                    order__delivery=unique)
                deduction = balance.BuyerBalance.get_total_balance_delivery(product_item_delivery)
                sum_actual_value = product_item_delivery.aggregate(sum_value=Sum('actual_value'))
                sum_price = prod.price * sum_actual_value['sum_value']
                total = total + sum_price
                result_dict = {"delivery": unique, 'product': prod, 'deduction': deduction, 'sum_price': sum_price}
                result_list.append(result_dict)
        return result_list, total

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        payments, total = self.payments_farmer()
        context['total'] = total

        context['page'], context['payments'] = self.get_paginate_page_and_subjects(payments)
        return context

