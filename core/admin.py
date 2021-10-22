from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import Group

from core.models import GreenUser


@admin.register(GreenUser)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('id', 'email', 'is_superuser', 'is_active', 'date_joined', 'password')
    list_filter = ('is_superuser', 'is_active', 'date_joined')
    fieldsets = (
        ("Личные данные", {'fields': ('email', 'password')}),
        ('Доступы', {'fields': ('is_superuser', 'is_active', 'is_staff')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_superuser'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email', 'is_superuser', 'is_active', 'date_joined')
    filter_horizontal = ()


admin.site.unregister(Group)
