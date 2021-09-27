from django.shortcuts import get_object_or_404

from apps.store.models.product_category import ProductCategory
from .base import BuyerBasePagesView


class BuyerStorefrontView(BuyerBasePagesView):
    template_name = 'buyer/pages/buyer-storefront-all-products.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['farmer_product_categories'] = ProductCategory.get_not_empty_categories()
        return context


class BuyerStorefrontByProductCategoryView(BuyerBasePagesView):
    template_name = 'buyer/pages/buyer-storefront-by-category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['farmer_product_categories'] = farmer_product_categories = ProductCategory.get_not_empty_categories()
        not_empty_category_pk = ProductCategory.get_category_from_list_or_404(
            kwargs.get('category_pk'),
            farmer_product_categories.values_list('pk', flat=True)
        )
        context['selected_category'] = get_object_or_404(ProductCategory, pk=not_empty_category_pk)
        return context
