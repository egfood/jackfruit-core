from django.contrib import admin

# from .admin_actions import ExportCSVMixin
# TODO: The file must be reworked for updated models
from .models.delivery import FoodDelivery
from .models.location import Location
from .models.order import FoodOrder
from .models.order_item import FoodOrderItem
from .models.product import RootProduct


@admin.register(RootProduct)
class FoodPriceAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_visible', 'date_creation', 'date_updated')
    list_filter = ('is_visible', 'date_creation', 'date_updated')
    search_fields = ('name',)
    ordering = ('name', 'is_visible')


@admin.register(FoodDelivery)
# class FoodDeliveryAdmin(admin.ModelAdmin, ExportCSVMixin):
class FoodDeliveryAdmin(admin.ModelAdmin):
    list_display = ('date', 'date_creation', 'date_updated', 'delivery_state_message')
    list_filter = ('date', 'date_creation', 'date_updated')
    ordering = ('date',)

    # actions = ["export_products_to_csv", "export_detail_orders_to_csv"]


@admin.register(FoodOrder)
class FoodOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'delivery', 'buyer', 'total_cost', 'location', 'state', 'date_updated', 'date_creation')
    list_filter = ('delivery', 'buyer', 'date_creation', 'date_updated', 'location', 'state')
    ordering = ('id', 'delivery', 'buyer', 'date_creation', 'date_updated', 'location', 'state')


@admin.register(FoodOrderItem)
class FoodOrderItemAdmin(admin.ModelAdmin):
    list_display = (
        'product', 'delivery_short_name', 'value', 'actual_value', 'item_total', 'date_creation', 'date_updated'
    )
    list_filter = ('product', 'date_creation', 'date_updated')
    ordering = ('product', 'value', 'actual_value', 'date_creation', 'date_updated')


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'location_type', 'city_type', 'city_value', 'city_district', 'street_type', 'street_value', 'building',
        'porch', 'floor', 'room', 'sort_key'
    )
    list_filter = ('user', 'location_type', 'city_value', 'city_district', 'street_value', 'building', 'sort_key')
    ordering = (
        'location_type', 'city_type', 'city_value', 'city_district', 'street_type', 'street_value', 'building', 'porch',
        'floor', 'room', 'sort_key'
    )
