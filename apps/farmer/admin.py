from django.contrib import admin

from apps.farmer.models.profile import FarmerProfile
from apps.farmer.models.product import FarmerProduct
from apps.farmer.models.feedback import FarmerFeedback


@admin.register(FarmerProfile)
class FarmerProfileAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'user', 'photo', 'phone', 'name', 'region')
    # list_display = ('user', 'user_role', 'date_creation', 'date_updated', 'tg_username', 'office', 'phone', 'notes')
    # list_filter = ('office', 'date_creation', 'date_updated', 'user_role')
    # fieldsets = (
    #     ('Техническая информация', {'fields': ('user', 'user_role')}),
    #     ('Личная информация', {'fields': ('tg_username', 'office', 'phone', 'notes')}),
    # )
    # search_fields = ('tg_username', 'office', 'notes', 'phone')
    # ordering = ('date_creation', 'user')
    # filter_horizontal = ()


@admin.register(FarmerProduct)
class FarmerProductAdmin(admin.ModelAdmin):
    list_display = ('farmer', 'value', 'unit', 'size', 'price')


@admin.register(FarmerFeedback)
class FarmerFeedbackAdmin(admin.ModelAdmin):
    list_display = ('order_item', 'rating', 'feedback')