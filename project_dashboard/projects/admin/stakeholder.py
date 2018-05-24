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
        (_('User Info (optional)'), {
            'fields': (('user', 'slug'), )
        }),
        (_('Stakeholder Info (if no User)'), {
            'fields': (
                ('first_name', 'last_name'), 'full_name', )
        }),
        (_('Contact Info'), {
            'fields': ('title', 'organization', 'email_address',
                       'phone_number',)
        }),
    )
    list_display = ['id', 'get_full_name']
    list_filter = ['full_name', 'title', 'organization', ]
    search_fields = ['full_name', 'title', 'organization', ]
    # prepopulated_fields = {'slug': ('get_full_name', )}
