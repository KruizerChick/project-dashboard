from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin as BaseFlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.utils.translation import gettext_lazy as _


# Customize Admin Site
admin.sites.AdminSite.site_header = 'Project Tracking Admin'
admin.sites.AdminSite.site_title = 'Project Tracking Admin'


# Register your models here.
class FlatPageAdmin(BaseFlatPageAdmin):
    """ Define a new FlatPageAdmin  """
    fieldsets = (
        (None, {'fields': ('url', 'title', 'content', 'sites')}),
        (_('Advanced options'), {
            'classes': ('collapse', ),
            'fields': (
                'enable_comments',
                'registration_required',
                'template_name',
            ),
        }),
    )


admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)
