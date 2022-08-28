from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models.delivery_cost import DeliveryCost
from .admin_actions import ExportCSVMixin
from .models.delivery import FoodDelivery
from .models.location import Location
from .models.order import FoodOrder
from .models.order_item import FoodOrderItem
from .models.product import RootProduct
from .models.product_category import ProductCategory
from .models.trade_margin import TradeMargin


@admin.register(RootProduct)
class RootProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_visible', 'category', 'trade_margin', 'date_creation', 'date_updated')
    list_filter = ('is_visible', 'category', 'date_creation', 'date_updated', 'trade_margin')
    search_fields = ('name',)
    ordering = ('name', 'is_visible', 'category', 'trade_margin', 'date_creation', 'date_updated')


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_creation', 'date_updated')
    list_filter = ('date_creation', 'date_updated')
    search_fields = ('name',)
    ordering = ('name', 'date_creation', 'date_updated')


@admin.register(FoodDelivery)
class FoodDeliveryAdmin(admin.ModelAdmin, ExportCSVMixin):
    list_display = ('date', 'date_creation', 'date_updated', 'delivery_state_message')
    list_filter = ('date', 'date_creation', 'date_updated')
    ordering = ('date',)

    actions = ["export_products_to_csv", "export_detail_orders_to_csv"]


@admin.register(FoodOrder)
class FoodOrderAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'delivery', 'buyer', 'delivery_cost', 'total_cost', 'location', 'state', 'payment_type', 'date_updated',
        'date_creation'
    )
    list_filter = (
        'delivery', 'buyer', 'date_creation', 'delivery_cost', 'date_updated', 'location', 'state', 'payment_type'
    )
    ordering = (
        'id', 'delivery', 'delivery_cost', 'buyer', 'date_creation', 'date_updated', 'location', 'state', 'payment_type'
    )


@admin.register(FoodOrderItem)
class FoodOrderItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'order', 'get_text_total_weight', 'get_text_item_total', 'date_creation', 'date_updated')
    history_list_display = ('price', 'value', 'actual_value', 'value_per_price', 'trade_margin')
    list_filter = ('order', 'product', 'date_creation', 'date_updated')
    ordering = ('product', 'value', 'actual_value', 'date_creation', 'date_updated')
    readonly_fields = ('price', 'trade_margin', 'text_item_total')

    def get_text_item_total(self, obj):
        return obj.text_item_total

    get_text_item_total.short_description = 'итого'

    def get_text_total_weight(self, obj):
        unit = obj.product.get_unit_display()
        return f'{obj.value} {unit}/ {obj.actual_value or "---"} {unit if obj.actual_value is not None else ""}'

    get_text_total_weight.short_description = "Объем (покуп./факт.)"


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'short_name', 'user', 'location_type', 'city_type', 'city_value', 'city_district', 'street_type',
        'street_value',
        'building', 'porch', 'floor', 'room', 'sort_key'
    )
    list_filter = ('user', 'location_type', 'city_value', 'city_district', 'street_value', 'building', 'sort_key')
    ordering = (
        'location_type', 'city_type', 'city_value', 'city_district', 'street_type', 'street_value', 'building', 'porch',
        'floor', 'room', 'sort_key'
    )


@admin.register(TradeMargin)
class TradeMarginAdmin(SimpleHistoryAdmin):
    list_display = ('get_total', 'backoffice_margin', 'dev_margin')
    history_list_display = ('backoffice_margin', 'dev_margin')
    ordering = ('backoffice_margin', 'dev_margin')

    def get_total(self, obj):
        return obj.total

    get_total.short_description = 'общая наценка, %'


@admin.register(DeliveryCost)
class DeliveryCostAdmin(SimpleHistoryAdmin):
    list_display = ('value',)
    history_list_display = ('value',)
    ordering = ('value',)
