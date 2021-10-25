from functools import cached_property

from django.conf import settings
from django.shortcuts import get_object_or_404

from apps.farmer.models.product import FarmerProduct
from apps.store.models.delivery import FoodDelivery
from apps.store.models.order_item import FoodOrderItem
from apps.store.models.product_category import ProductCategory
from core.views.mixins import PaginationMixin
from .base import BuyerBasePagesView


class BuyerStorefrontBaseView(BuyerBasePagesView, PaginationMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['farmer_product_categories'] = self.product_categories
        context['max_rating'] = settings.MAX_PRODUCT_RATING
        farmer_products = self.get_enriched_farmer_products()
        context['page'], context['farmer_products'] = self.get_paginate_page_and_subjects(
            farmer_products, settings.COUNT_OF_STOREFRONT_PRODUCTS_PER_PAGE
        )
        return context

    @cached_property
    def current_category_pk(self):
        return ProductCategory.get_category_from_list_or_404(
            self.kwargs.get('category_pk'),
            self.product_categories.values_list('pk', flat=True)
        )

    @cached_property
    def product_categories(self):
        return ProductCategory.get_not_empty_categories()

    @staticmethod
    def enrich_with_rating(farmer_products):
        ratings = FarmerProduct.get_ratings(farmer_products, return_dict_by_pk=True)
        updated_farmer_products = []
        for fp in farmer_products:
            updated_fp = fp
            updated_fp.rating = ratings[fp.pk]
            updated_farmer_products.append(updated_fp)
        return updated_farmer_products

    def enrich_with_order_items(self, farmer_products):
        order_items, _ = FoodOrderItem.get_buyer_cart_items(self.request, FoodDelivery.get_nearest_delivery())
        updated_farmer_products = []
        if order_items:
            order_item_values = {item.product.pk: item.value for item in order_items.prefetch_related('product')}
            for fp in farmer_products:
                updated_fp = fp
                updated_fp.order_item_value = order_item_values.get(fp.pk)
                updated_farmer_products.append(updated_fp)
            return updated_farmer_products
        else:
            return farmer_products

    def get_enriched_farmer_products(self):
        farmer_products = FarmerProduct.get_visible_products(category_pk=self.current_category_pk)
        farmer_products_with_rating = self.enrich_with_rating(farmer_products)
        return self.enrich_with_order_items(farmer_products_with_rating)


class BuyerStorefrontAllProductsView(BuyerStorefrontBaseView):
    template_name = 'buyer/pages/buyer-storefront-all-products.html'

    @property
    def current_category_pk(self):
        return


class BuyerStorefrontByProductCategoryView(BuyerStorefrontBaseView):
    template_name = 'buyer/pages/buyer-storefront-by-category.html'

    def get_context_data(self, **kwargs):
        self.kwargs = kwargs
        context = super().get_context_data(**kwargs)
        context['selected_category'] = get_object_or_404(ProductCategory, pk=self.current_category_pk)
        return context
