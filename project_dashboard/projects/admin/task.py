""" Admin for project Task model """
from django.contrib import admin
from django.urls import NoReverseMatch
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

from ..forms import TaskAdminForm


class TaskAdmin(admin.ModelAdmin):
    form = TaskAdminForm
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
    list_filter = ['project', 'is_milestone', 'status']
    filter_horizontal = ('resources', )
    search_fields = ['name', 'project', 'description', 'resources']
    save_on_top = True

    def get_tree_path(self, category):
        """
        Return the category's tree path in HTML.
        """
        try:
            return format_html(
                '<a href="{}" target="blank">/{}/</a>',
                category.get_absolute_url(), category.tree_path)
        except NoReverseMatch:
            return '/%s/' % category.tree_path
    get_tree_path.short_description = _('tree path')
