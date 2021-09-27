from django.db import models
from django.http import Http404

from core.models import FoodAbstract


class ProductCategory(FoodAbstract):
    name = models.CharField(verbose_name='Название категории', max_length=250)

    def __str__(self):
        return f"[Категория продукта]{self.name}(pk={self.pk})"

    @classmethod
    def get_not_empty_categories(cls):
        return cls.objects.filter(root_product__farmer_product__isnull=False)

    @classmethod
    def get_category_from_list_or_404(cls, category_pk, limited_categories):
        if category_pk in limited_categories:
            return category_pk
        raise Http404("Product category not found or empty")

    def get_buyer_url(self):
        from django.urls import reverse
        return reverse('buyer:storefront-by-category', kwargs={'category_pk': self.pk})
