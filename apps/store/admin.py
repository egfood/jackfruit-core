from django.contrib import admin

from apps.store.models import *


@admin.register(FoodProduct)
class FoodPriceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'weight_per_price', 'min_weight', 'packaging', 'supplier_id', 'is_visible',
                    'date_creation', 'date_updated')
    list_filter = ('is_visible', 'packaging', 'date_creation', 'date_updated', 'supplier_id')
    search_fields = ('name', 'packaging')
    ordering = ('name', 'is_visible', 'min_weight', 'packaging', 'supplier_id')


@admin.register(FoodDelivery)
class FoodDeliveryAdmin(admin.ModelAdmin):
    list_display = ('date', 'date_creation', 'date_updated', 'delivery_state_message')
    list_filter = ('date', 'date_creation', 'date_updated')
    ordering = ('date',)


@admin.register(FoodOfficeOrder)
class FoodOfficeOrderAdmin(admin.ModelAdmin):
    list_display = ('delivery', 'user', 'date_creation', 'date_updated', 'office', 'state')
    list_filter = ('delivery', 'user', 'date_creation', 'date_updated', 'office', 'state')
    ordering = ('delivery', 'user', 'date_creation', 'date_updated', 'office', 'state')


@admin.register(FoodHomeOrder)
class FoodHomeOrderAdmin(admin.ModelAdmin):
    list_display = ('delivery', 'user', 'date_creation', 'date_updated', 'home', 'state')
    list_filter = ('delivery', 'user', 'date_creation', 'date_updated', 'home', 'state')
    ordering = ('delivery', 'user', 'date_creation', 'date_updated', 'home', 'state')

    def street(self, obj):
        h = obj.home
        return f'{h.get_street_type_value()} {h.street_value}'

    def city_district(self, obj):
        return obj.home.get_city_district_value()


@admin.register(FoodOfficeOrderItem)
class FoodOfficeOrderItemAdmin(admin.ModelAdmin):
    list_display = ('office_order', 'product', 'value', 'actual_value', 'date_creation', 'date_updated')
    list_filter = ('product', 'date_creation', 'date_updated')
    ordering = ('office_order', 'product', 'value', 'actual_value', 'date_creation', 'date_updated')


@admin.register(FoodHomeOrderItem)
class FoodOrderHomeItemAdmin(admin.ModelAdmin):
    list_display = ('home_order', 'product', 'value', 'actual_value', 'date_creation', 'date_updated')
    list_filter = ('product', 'date_creation', 'date_updated')
    ordering = ('home_order', 'product', 'value', 'actual_value', 'date_creation', 'date_updated')


@admin.register(HomeLocation)
class HomeLocationAdmin(admin.ModelAdmin):
    list_display = (
        'city_type', 'city_value', 'city_district', 'street_type', 'street_value', 'building', 'porch', 'floor', 'room',
        'sort_key')
    list_filter = ('city_value', 'city_district', 'street_value', 'building', 'sort_key')
    ordering = (
        'city_type', 'city_value', 'city_district', 'street_type', 'street_value', 'building', 'porch', 'floor', 'room',
        'sort_key')


@admin.register(OfficeLocation)
class OfficeLocationAdmin(admin.ModelAdmin):
    list_display = (
        'city_type', 'city_value', 'city_district', 'street_type', 'street_value', 'building', 'short_name', 'sort_key')
    list_filter = ('city_value', 'city_district', 'street_value', 'building', 'sort_key')
    ordering = (
        'city_type', 'city_value', 'city_district', 'street_type', 'street_value', 'building', 'short_name', 'sort_key')
