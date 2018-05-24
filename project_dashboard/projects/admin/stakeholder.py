from django.contrib import admin
from django.utils.translation import gettext_lazy as _

# from ..models.stakeholder import Role


# Register your models here.
# class RoleInline(admin.TabularInline):
#     model = Role
#     extra = 0


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
    list_display = ['name', 'role_type']
    list_filter = ('role_type', )
    prepopulated_fields = {'slug': ('name', )}
    # filter_horizontal = ("permissions",)

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
    readonly_fields = ('full_name', 'cached_memberships')
    list_display = ['id', 'slug', 'full_name', 'organization']
    list_filter = ['title', 'organization', ]
    search_fields = ['title', 'organization', 'cached_memberships']
    prepopulated_fields = {'slug': ('user', 'first_name', 'last_name')}
