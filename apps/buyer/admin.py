from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.utils.translation import gettext_lazy as _
from django_summernote.admin import SummernoteModelAdmin


class FlatPageNewAdmin(FlatPageAdmin, SummernoteModelAdmin):
    summernote_fields = '__all__'
    fieldsets = (
        (None, {'fields': ('url', 'title', 'content', 'sites')}),
        (_('Advanced options'), {
            'classes': ('collapse',),
            'fields': (
                'enable_comments',
                'registration_required',
                'template_name',
            ),
        }),
    )
    list_display = ('url', 'title', 'template_name')
    list_filter = ('sites', 'registration_required')
    search_fields = ('url', 'title')


admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageNewAdmin)
