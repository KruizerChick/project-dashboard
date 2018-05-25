""" Admin for project Task model """

from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class TaskAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Task'), {
            'fields': (
                ('name', 'slug'), 'project', 'is_milestone',
                'description', 'status', 'process', 'resources', 'order'
            ),
        }),
        (_('Related Tasks'), {
            'fields': (('parent', 'predecessor', 'successor'), ),
        }),
    )
    list_display = ['name', 'project', 'status', 'is_milestone']
    list_filter = ['project', 'is_milestone', 'status', 'process']
    search_fields = ['name', 'project', 'description', 'resources']
    save_on_top = True
