""" CategoryAdmin for Projects """
from django.contrib import admin
from django.urls import NoReverseMatch
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

from ..forms import CategoryAdminForm


class CategoryAdmin(admin.ModelAdmin):
    """ Admin for Category model. """
    form = CategoryAdminForm
    fields = (('name', 'slug'), 'parent', 'description', )
    list_display = ('name', 'slug', 'get_tree_path', 'description')
    prepopulated_fields = {'slug': ('name', )}
    search_fields = ('name', 'description')
    list_filter = ('parent',)

    def __init__(self, model, admin_site):
        self.form.admin_site = admin_site
        super(CategoryAdmin, self).__init__(model, admin_site)

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
