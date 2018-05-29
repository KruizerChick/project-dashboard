""" Admin config for Project models """
from django.contrib import admin
from django.shortcuts import reverse
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

# from ...core.permissions import permissions
from ..models.project import Membership
# from .stakeholder import RoleInline


# Inlines
class MembershipInline(admin.TabularInline):
    model = Membership
    extra = 0

    def get_formset(self, request, obj=None, **kwargs):
        # Hack! Hook parent obj just in time to use in formfield_for_foreignkey
        self.parent_obj = obj
        return super(MembershipInline, self).get_formset(
            request, obj, **kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if (db_field.name in ["stakeholder", "invited_by"]):
            kwargs["queryset"] = db_field.related_model.objects.filter(
                memberships__project=self.parent_obj)

        elif (db_field.name in ["role"]):
            kwargs["queryset"] = db_field.related_model.objects.filter(
                project=self.parent_obj)

        return super().formfield_for_foreignkey(
            db_field, request, **kwargs)


# Admin panels
class MembershipAdmin(admin.ModelAdmin):
    list_display = ['project', 'role', 'stakeholder']
    list_display_links = list_display
    raw_id_fields = ["project"]

    def has_add_permission(self, request):
        return False

    def get_object(self, *args, **kwargs):
        self.obj = super().get_object(*args, **kwargs)
        return self.obj

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name in ["stakeholder", "invited_by"] and getattr(self, 'obj', None):
            kwargs["queryset"] = db_field.related_model.objects.filter(
                    memberships__project=self.obj.project)

        elif db_field.name in ["role"] and getattr(self, 'obj', None):
            kwargs["queryset"] = db_field.related_model.objects.filter(
                                         project=self.obj.project)

        return super().formfield_for_foreignkey(
            db_field, request, **kwargs)


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
        # RoleInline,
        # MembershipInline,
        # NotifyPolicyInline,
        ]

    save_on_top = True
    actions_on_top = True
    actions_on_bottom = True

    def owner_url(self, obj):
        if obj.owner:
            url = reverse(
                'admin:{0}_{1}_change'.format(
                    obj.owner._meta.app_label, obj.owner._meta.model_name),
                args=(obj.owner.pk, ))
            return format_html(
                "<a href='{url}' title='{stakeholder}'>{stakeholder}</a>", url=url, stakeholder=obj.owner)
        return ''
    owner_url.short_description = _('owner')

    def get_object(self, *args, **kwargs):
        self.obj = super().get_object(*args, **kwargs)
        return self.obj

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if (db_field.name in ["default_task_status", "default_priority", "default_severity",
                              "default_issue_status", "default_issue_type"]):
            if getattr(self, 'obj', None):
                kwargs["queryset"] = db_field.related_model.objects.filter(
                                                          project=self.obj)
            else:
                kwargs["queryset"] = db_field.related_model.objects.none()

        elif (db_field.name in ["owner"]
                and getattr(self, 'obj', None)):
            kwargs["queryset"] = db_field.related_model.objects.filter(
                                         memberships__project=self.obj.project)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def delete_model(self, request, obj):
        obj.delete_related_content()
        super().delete_model(request, obj)
