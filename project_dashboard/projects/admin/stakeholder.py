from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from ..models.stakeholder import Role
from ..models.project import Membership, Project


# Register your models here.
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


class RoleInline(admin.TabularInline):
    model = Role
    extra = 0


# Admin panels
class RoleAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            "fields": (
                ("name", "slug"), 'description',
                ('role_type', 'order', 'computable'),
                'permissions')
            }),
    )
    list_display = ['name', 'order', 'project', 'category']
    list_filter = ('role_type', 'project', 'category')
    prepopulated_fields = {'slug': ('name', )}

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        if db_field.name == "permissions":
            qs = kwargs.get("queryset", db_field.rel.to.objects)
            # Avoid a major performance hit resolving permission names which
            # triggers a content_type load:
            kwargs["queryset"] = qs.select_related("content_type")
        return super().formfield_for_manytomany(
            db_field, request=request, **kwargs)


class StakeholderAdmin(admin.ModelAdmin):
    """ Admin class for Stakeholder model """
    fieldsets = (
        (_('Stakeholder'), {
            'fields': (('full_name', 'slug'), )
        }),
        (_('User (preferred)'), {
            'fields': ('user', )
        }),
        (_('Stakeholder Info (if no User)'), {
            'fields': (('first_name', 'last_name'), 'email_address',),
            'classes': ('collapse', 'collapse-closed')
        }),
        (_('Contact Info'), {
            'fields': (('organization', 'title'), 'phone_number', )
        }),
        (_('Project Info'), {
            'fields': ('cached_memberships', )
        }),
    )
    readonly_fields = ['cached_memberships']
    list_display = ['full_name', 'slug', 'organization']
    list_filter = ['title', 'organization', ]
    filter_horizontal = ()
    search_fields = ['title', 'organization', 'cached_memberships']
    prepopulated_fields = {'slug': ('user', 'full_name')}
    inlines = [
        OwnedProjectsInline,
        MembershipsInline,
    ]
