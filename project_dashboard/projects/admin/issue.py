""" Admin form for Project Issue model """

from django.contrib import admin
from django.urls import NoReverseMatch
from django.utils.html import conditional_escape
from django.utils.html import format_html_join
from django.utils.translation import gettext_lazy as _

from ..forms import IssueAdminForm
from ..models.issue import IssueProgress


class IssueProgressInline(admin.TabularInline):
    """ Inline model for IssueProgress admin """
    model = IssueProgress
    readonly_fields = ('created', )
    fields = ('created', 'progress')
    extra = 1


class IssueAdmin(admin.ModelAdmin):
    form = IssueAdminForm
    fieldsets = (
        (_('Issue Info'), {
            'fields': (('name', 'slug'), 'description', )
        }),
        (_('Project'), {
            'fields': (('project', 'impact'), 'task', )
        }),
        (_('Issue Meta'), {
            'fields': (('importance', 'urgency', 'priority'),
                       'owner', 'assigned_to', 'category')
        }),
        (_('Resolution'), {
            'fields': (('resolution_plan', 'due_date'), 'resolved')
        }),
    )
    list_display = ['name', 'id', 'project', 'priority', 'get_categories']
    list_filter = ['project', 'task', 'priority', 'status', ]
    inlines = [IssueProgressInline]
    save_on_top = True

    def __init__(self, model, admin_site):
        self.form.admin_site = admin_site
        super(IssueAdmin, self).__init__(model, admin_site)

    def get_categories(self, issue):
        """ Return the categories linked in HTML. """
        try:
            return format_html_join(
                ', ', '<a href="{}" target="blank">{}</a>',
                [(category.get_absolute_url(), category.name)
                 for category in issue.categories.all()])
        except NoReverseMatch:
            return ', '.join([conditional_escape(category.name)
                              for category in issue.categories.all()])
    get_categories.short_description = _('categories')
