from functools import cached_property

from django.db import models
from django.db.models import Count, Avg, Q

from core.models import AbsProfile


class FarmerProfile(AbsProfile):
    service_zone = models.TextField(verbose_name='Зона обслуживания', blank=True, default="")
    legal_name = models.CharField(verbose_name='Название компании / фермерского хозяйства', max_length=500, blank=True,
                                  default="")

    @property
    def stringify_profile_type(self):
        return "фермера"

    def popular_products(self, quantity=3):
        popular_product_queryset = self.farmerproduct_set.annotate(popular=Count('order_item')).values('popular',
                                                                                                       'product__name')
        if not popular_product_queryset.all().exists():
            return []
        my_dict = {qs['popular']: qs['product__name'] for qs in popular_product_queryset}
        popular_product_list = list(my_dict.items())
        popular_product_list.sort(reverse=True)
        result = [i[1] for i in popular_product_list][:quantity]
        return result

    @cached_property
    def rating(self):
        rating_queryset = self.farmerproduct_set.aggregate(
            feedback=Avg('order_item__farmer_feedback__rating'))
        if rating_queryset['feedback'] is None:
            return None
        result = round(rating_queryset['feedback'], 1)
        return result

    def feedback(self):
        rating_queryset = self.farmerproduct_set.aggregate(
            feedback=Count('order_item__farmer_feedback__feedback',
                           filter=~Q(order_item__farmer_feedback__feedback__iexact='')))
        if rating_queryset['feedback'] is None:
            return 0
        result = int(rating_queryset['feedback'])
        return result
