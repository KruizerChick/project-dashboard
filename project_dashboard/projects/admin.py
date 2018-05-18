from django.contrib import admin
from django.db import transaction
from django.shortcuts import reverse
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

from ..core.permissions import permissions
from ..users.admin import RoleInline

from . import models


# Register your models here.
class MembershipAdmin(admin.ModelAdmin):
    list_display = ['project', 'role', 'user']
    list_display_links = list_display
    raw_id_fields = ["project"]

    def has_add_permission(self, request):
        return False

    def get_object(self, *args, **kwargs):
        self.obj = super().get_object(*args, **kwargs)
        return self.obj

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name in ["user", "invited_by"] and getattr(self, 'obj', None):
            kwargs["queryset"] = db_field.related_model.objects.filter(
                    memberships__project=self.obj.project)

        elif db_field.name in ["role"] and getattr(self, 'obj', None):
            kwargs["queryset"] = db_field.related_model.objects.filter(
                                         project=self.obj.project)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class MembershipInline(admin.TabularInline):
    model = models.Membership
    extra = 0

    def get_formset(self, request, obj=None, **kwargs):
        # Hack! Hook parent obj just in time to use in formfield_for_foreignkey
        self.parent_obj = obj
        return super(MembershipInline, self).get_formset(request, obj, **kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if (db_field.name in ["user", "invited_by"]):
            kwargs["queryset"] = db_field.related_model.objects.filter(
                                         memberships__project=self.parent_obj)

        elif (db_field.name in ["role"]):
            kwargs["queryset"] = db_field.related_model.objects.filter(
                                                      project=self.parent_obj)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ProjectAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            "fields": (("name", "slug", ),
                       "description",
                       ("date_created", "date_modified"),
                       'budget',)
        }),
        (_("Privacy"), {
            "fields": (("owner", "is_private",),
                       ("anon_permissions", "public_permissions"),)
        }),
        (_("Modules activated"), {
            "fields": (("is_backlog_activated", "total_milestones",),
                       "is_issues_activated",
                       "is_wiki_activated", ),
        }),
        (_("Default project values"), {
            "classes": ("collapse",),
            "fields": ("default_task_status",
                       ("default_status", "default_priority", "default_severity", "default_issue_type")),
        }),
        (_("Activity"), {
            "classes": ("collapse",),
            "fields": (("total_activity", "total_activity_last_week",
                        "total_activity_last_month", "total_activity_last_year"),),
        }),
    )
    list_display = ["id", "name", "slug", "is_private",
                    "owner_url", ]
    prepopulated_fields = {'slug': ('name', )}
    list_display_links = ["id", "name", "slug"]
    list_filter = ("is_private", )
    # list_editable = ["is_featured", "blocked_code"]
    search_fields = ["id", "name", "slug", "owner__username", "owner__email", "owner__full_name"]
    inlines = [
        RoleInline, MembershipInline,
        # NotifyPolicyInline, LikeInline
        ]

    save_on_top = True
    actions_on_top = True
    actions_on_bottom = True

    def owner_url(self, obj):
        if obj.owner:
            url = reverse('admin:{0}_{1}_change'.format(obj.owner._meta.app_label,
                                                        obj.owner._meta.model_name),
                          args=(obj.owner.pk,))
            return format_html("<a href='{url}' title='{user}'>{user}</a>", url=url, user=obj.owner)
        return ""
    owner_url.short_description = _('owner')

    def get_object(self, *args, **kwargs):
        self.obj = super().get_object(*args, **kwargs)
        return self.obj

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if (db_field.name in ["default_points", "default_us_status", "default_task_status",
                              "default_priority", "default_severity",
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

    # Actions
    actions = [
        "make_public",
        "make_private",
        "delete_selected"
    ]

    @transaction.atomic
    def make_public(self, request, queryset):
        total_updates = 0

        for project in queryset.exclude(is_private=False):
            project.is_private = False

            anon_permissions = list(map(lambda perm: perm[0], permissions.ANON_PERMISSIONS))
            project.anon_permissions = list(set((project.anon_permissions or []) + anon_permissions))
            project.public_permissions = list(set((project.public_permissions or []) + anon_permissions))

            project.save()
            total_updates += 1

        self.message_user(request, _("{count} successfully made public.").format(count=total_updates))
    make_public.short_description = _("Make public")

    @transaction.atomic
    def make_private(self, request, queryset):
        total_updates = 0

        for project in queryset.exclude(is_private=True):
            project.is_private = True
            project.anon_permissions = []
            project.public_permissions = []

            project.save()
            total_updates += 1

        self.message_user(request, _("{count} successfully made private.").format(count=total_updates))
    make_private.short_description = _("Make private")

    def delete_selected(self, request, queryset):
        # NOTE: This must be equal to taiga.projects.models.Project.delete_related_content
        from taiga.events.apps import (connect_events_signals,
                                       disconnect_events_signals)
        from taiga.projects.tasks.apps import (connect_all_tasks_signals,
                                               disconnect_all_tasks_signals)
        from taiga.projects.userstories.apps import (connect_all_userstories_signals,
                                                     disconnect_all_userstories_signals)
        from taiga.projects.issues.apps import (connect_all_issues_signals,
                                                disconnect_all_issues_signals)
        from taiga.projects.apps import (connect_memberships_signals,
                                         disconnect_memberships_signals)

        disconnect_events_signals()
        disconnect_all_issues_signals()
        disconnect_all_tasks_signals()
        disconnect_all_userstories_signals()
        disconnect_memberships_signals()

        r = admin.actions.delete_selected(self, request, queryset)

        connect_events_signals()
        connect_all_issues_signals()
        connect_all_tasks_signals()
        connect_all_userstories_signals()
        connect_memberships_signals()

        return r
    delete_selected.short_description = _("Delete selected %(verbose_name_plural)s")


# Common admins
class SeverityAdmin(admin.ModelAdmin):
    list_display = ["project", "order", "name", "color"]
    list_display_links = ["name"]
    raw_id_fields = ["project"]


class PriorityAdmin(admin.ModelAdmin):
    list_display = ["project", "order", "name", "color"]
    list_display_links = ["name"]
    raw_id_fields = ["project"]


class IssueTypeAdmin(admin.ModelAdmin):
    list_display = ["project", "order", "name", "color"]
    list_display_links = ["name"]
    raw_id_fields = ["project"]


class StatusAdmin(admin.ModelAdmin):
    list_display = ["project", "order", "name", "is_closed", "color"]
    list_display_links = ["name"]
    raw_id_fields = ["project"]


admin.site.register(models.Status, StatusAdmin)
# admin.site.register(models.TaskStatus, TaskStatusAdmin)
# admin.site.register(models.UserStoryStatus, UserStoryStatusAdmin)
# admin.site.register(models.Points, PointsAdmin)
admin.site.register(models.Project, ProjectAdmin)
admin.site.register(models.Membership, MembershipAdmin)
admin.site.register(models.Severity, SeverityAdmin)
admin.site.register(models.Priority, PriorityAdmin)
admin.site.register(models.IssueType, IssueTypeAdmin)
admin.site.register(models.Activity)
# admin.site.register(models.ProjectTemplate, ProjectTemplateAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'project')
    list_filter = ('name', 'project')


admin.site.register(models.Category, CategoryAdmin)


class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'project', 'amount')
    list_filter = ('project', 'title', 'category')


admin.site.register(models.Expense, ExpenseAdmin)
