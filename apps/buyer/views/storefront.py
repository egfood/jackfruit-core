from django.conf import settings
from django.shortcuts import get_object_or_404

from apps.farmer.models.product import FarmerProduct
from apps.store.models.product_category import ProductCategory
from .base import BuyerBasePagesView


class BuyerStorefrontBaseView(BuyerBasePagesView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['farmer_product_categories'] = ProductCategory.get_not_empty_categories()
        context['max_rating'] = settings.MAX_PRODUCT_RATING
        return context


class BuyerStorefrontAllProductsView(BuyerStorefrontBaseView):
    template_name = 'buyer/pages/buyer-storefront-all-products.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['farmer_products'] = FarmerProduct.get_visible_products()

        return context


class BuyerStorefrontByProductCategoryView(BuyerStorefrontBaseView):
    template_name = 'buyer/pages/buyer-storefront-by-category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        not_empty_category_pk = ProductCategory.get_category_from_list_or_404(
            kwargs.get('category_pk'),
            context['farmer_product_categories'].values_list('pk', flat=True)
        )
        context['selected_category'] = get_object_or_404(ProductCategory, pk=not_empty_category_pk)
        farmer_products = FarmerProduct.get_visible_products(category_pk=not_empty_category_pk)
        ratings = FarmerProduct.get_ratings(farmer_products, return_dict_by_pk=True)
        updated_farmer_products = []
        for fp in farmer_products:
            updated_fp = fp
            updated_fp.rating = ratings[fp.pk]
            updated_farmer_products.append(updated_fp)
        context['farmer_products'] = updated_farmer_products
        return context
