from django import forms
from django.apps import apps
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import gettext_lazy as _

from .models import Role, User


# Admin Forms
class MyUserChangeForm(UserChangeForm):
    """ User change form for Admin """
    class Meta(UserChangeForm.Meta):
        """ Meta for User change form """
        model = User


class MyUserCreationForm(UserCreationForm):
    """ User create form for Admin """
    error_message = UserCreationForm.error_messages.update({
        'duplicate_username': 'This username has already been taken.'
    })

    class Meta(UserCreationForm.Meta):
        """ Meta for User create form """
        model = User

    def clean_username(self):
        """ Clean username """
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])


# Inlines
class MembershipsInline(admin.TabularInline):
    model = apps.get_model("projects", "Membership")
    fk_name = "user"
    verbose_name = _("Project Member")
    verbose_name_plural = _("Project Members")
    fields = ("project_id", "project_name", "project_slug", "project_is_private",
              "project_owner", "is_admin")
    readonly_fields = ("project_id", "project_name", "project_slug", "project_is_private",
                       "project_owner", "is_admin")
    show_change_link = True
    extra = 0

    def project_id(self, obj):
        return obj.project.id if obj.project else None
    project_id.short_description = _("id")

    def project_name(self, obj):
        return obj.project.name if obj.project else None
    project_name.short_description = _("name")

    def project_slug(self, obj):
        return obj.project.slug if obj.project else None
    project_slug.short_description = _("slug")

    def project_is_private(self, obj):
        return obj.project.is_private if obj.project else None
    project_is_private.short_description = _("is private")
    project_is_private.boolean = True

    def project_owner(self, obj):
        if obj.project and obj.project.owner:
            return "{} (@{})".format(obj.project.owner.get_full_name(), obj.project.owner.username)
        return None
    project_owner.short_description = _("owner")

    def has_add_permission(self, *args):
        return False

    def has_delete_permission(self, *args):
        return False


class OwnedProjectsInline(admin.TabularInline):
    model = apps.get_model("projects", "Project")
    fk_name = "owner"
    verbose_name = _("Project Ownership")
    verbose_name_plural = _("Project Ownerships")
    fields = ("id", "name", "slug", "is_private")
    readonly_fields = ("id", "name", "slug", "is_private")
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
    list_display = ["name", 'role_type']
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


class MyUserAdmin(AuthUserAdmin):
    """ Custom User Admin form """
    fieldsets = (
        (None, {"fields": (("username", "password"),)}),
        (_("Personal info"), {"fields": ("full_name", "email", "bio", "photo")}),
        (_("Extra info"), {"fields": (("lang", "timezone"), )}),
        (_("Permissions"), {"fields": (("is_active", "is_superuser"), )}),
        (_("Important dates"), {"fields": (("date_joined", "last_login"), )}),
    )
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ("username", "email", "full_name")
    list_filter = ("is_superuser", "is_active")
    search_fields = ("username", "full_name", "email")
    ordering = ("username",)
    filter_horizontal = ()
    inlines = [
        OwnedProjectsInline,
        MembershipsInline
    ]
    save_on_top = True
    actions_on_top = True
    actions_on_bottom = True


admin.site.register(User, MyUserAdmin)
admin.site.register(Role, RoleAdmin)
