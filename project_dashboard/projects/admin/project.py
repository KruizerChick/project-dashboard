""" Admin config for Project models """
# from itertools import chain
# from django.apps import apps
from django.contrib import admin
# from django.contrib.staticfiles.storage import staticfiles_storage
# from django.db import transaction
# from django.forms import Media
# from django.shortcuts import reverse
# from django.utils.encoding import force_text
# from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

# from ..core.permissions import permissions
from ..models.project import Membership, Project
# from .stakeholder import RoleInline


# Inlines
class MembershipsInline(admin.TabularInline):
    model = Membership
    # fk_name = 'stakeholder'
    verbose_name = _('Project Member')
    verbose_name_plural = _('Project Members')
    fields = ('project_id', 'project_name', 'project_slug',
              'project_owner', 'is_admin')
    readonly_fields = ('project_id', 'project_name', 'project_slug',
                       'project_owner', 'is_admin')
    show_change_link = True
    extra = 0

    def project_id(self, obj):
        return obj.project.id if obj.project else None
    project_id.short_description = _('id')

    def project_name(self, obj):
        return obj.project.name if obj.project else None
    project_name.short_description = _('name')

    def project_slug(self, obj):
        return obj.project.slug if obj.project else None
    project_slug.short_description = _('slug')

    def project_owner(self, obj):
        if obj.project and obj.project.owner:
            return '(@{})'.format(obj.project.owner.username)
        return None
    project_owner.short_description = _('owner')

    def has_add_permission(self, *args):
        return False

    def has_delete_permission(self, *args):
        return False


class OwnedProjectsInline(admin.TabularInline):
    model = Project
    # fk_name = 'owner'
    verbose_name = _('Project Ownership')
    verbose_name_plural = _('Project Ownerships')
    fields = ('id', 'name', 'slug', )
    readonly_fields = ('id', 'name', 'slug', )
    show_change_link = True
    extra = 0

    def has_add_permission(self, *args):
        return False

    def has_delete_permission(self, *args):
        return False


class ProjectAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Project Info'), {
            'fields': (('name', 'slug', ),
                       'description', ('is_closed', 'is_phased'), )
        }),
        (_('Privacy'), {
            'classes': ('collapse', ),
            'fields': (('login_required', 'password'),
                       ('anon_permissions', 'public_permissions'),)
        }),
        (_('Related Projects'), {
            'classes': ('collapse', ),
            'fields': ('predecessors', 'successors', 'related', ),
        }),
    )
    list_display = ['name', 'id', 'slug', 'owner', 'is_closed', ]
    prepopulated_fields = {'slug': ('name', )}
    list_display_links = ['id', 'name', 'slug']
    list_filter = ('is_closed', )
    # list_editable = ['is_featured', 'blocked_code']
    search_fields = [
        'id', 'name', 'slug',
        'owner__username', 'owner__email',
        ]
    inlines = [
        MembershipsInline,
        # RoleInline,
        # NotifyPolicyInline, LikeInline
        ]

    save_on_top = True
    actions_on_top = True
    actions_on_bottom = True
#     def owner_url(self, obj):
#         if obj.owner:
#             url = reverse(
#                 'admin:{0}_{1}_change'.format(
#                     obj.owner._meta.app_label, obj.owner._meta.model_name),
#                 args=(obj.owner.pk, ))
#             return format_html(
#                 '<a href='{url}' title='{user}'>{user}</a>', url=url, user=obj.owner)
#         return ''
#     owner_url.short_description = _('owner')

    def get_object(self, *args, **kwargs):
        self.obj = super().get_object(*args, **kwargs)
        return self.obj
