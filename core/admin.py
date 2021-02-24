from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import Group

# from core.models import UserProfile, GreenUser


# @admin.register(GreenUser)
# class UserAdmin(BaseUserAdmin):
#     form = UserChangeForm
#     add_form = UserCreationForm
#
#     list_display = ('email', 'first_name', 'last_name', 'is_superuser', 'is_active', 'date_joined')
#     list_filter = ('is_superuser', 'is_active', 'date_joined')
#     fieldsets = (
#         ("Личные данные", {'fields': ('email', 'password', 'first_name', 'last_name')}),
#         ('Доступы', {'fields': ('is_superuser', 'is_active', 'is_staff')}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'first_name', 'password1', 'password2', 'is_superuser'),
#         }),
#     )
#     search_fields = ('email', 'first_name', 'last_name')
#     ordering = ('email', 'first_name', 'is_superuser', 'is_active', 'date_joined')
#     filter_horizontal = ()
#
#
# admin.site.unregister(Group)


# @admin.register(UserProfile)
# class UserProfileAdmin(admin.ModelAdmin):
#     list_display = ('user', 'user_role', 'date_creation', 'date_updated', 'tg_username', 'office', 'phone', 'notes')
#     list_filter = ('office', 'date_creation', 'date_updated', 'user_role')
#     fieldsets = (
#         ('Техническая информация', {'fields': ('user', 'user_role')}),
#         ('Личная информация', {'fields': ('tg_username', 'office', 'phone', 'notes')}),
#     )
#     search_fields = ('tg_username', 'office', 'notes', 'phone')
#     ordering = ('date_creation', 'user')
#     filter_horizontal = ()
