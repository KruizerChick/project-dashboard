# from dateutil.relativedelta import relativedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField, JSONField
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.apps import apps
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

# from django_pglocks import advisory_lock

from ..core.permissions.choices import ANON_PERMISSIONS, MEMBERS_PERMISSIONS
from ..core.utils.slug import slugify_uniquely, slugify_uniquely_for_queryset
from ..core.utils.time import timestamp_ms
from .notifications.choices import NotifyLevel


# Create your models here.
class Membership(models.Model):
    """
    This model stores all project memberships. Also
    stores invitations to memberships that does not have
    assigned user.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        null=True, blank=True,
        default=None, related_name="memberships")
    project = models.ForeignKey(
        "Project", on_delete=models.CASCADE,
        null=False, blank=False,
        related_name="memberships")
    role = models.ForeignKey(
        "users.Role", on_delete=models.CASCADE,
        null=False, blank=False,
        related_name="memberships")
    is_admin = models.BooleanField(
        default=False, null=False, blank=False)

    # Invitation metadata
    email = models.EmailField(
        max_length=255, default=None,
        null=True, blank=True,
        verbose_name=_("email"))
    created_at = models.DateTimeField(
        default=timezone.now, verbose_name=_("create at"))
    token = models.CharField(
        max_length=60, blank=True, null=True,
        default=None, verbose_name=_("token"))

    invited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name="ihaveinvited+",
        null=True, blank=True)

    invitation_extra_text = models.TextField(
        null=True, blank=True,
        verbose_name=_("invitation extra text"))

    user_order = models.BigIntegerField(
        default=timestamp_ms,
        null=False, blank=False,
        verbose_name=_("user order"))

    class Meta:
        verbose_name = "membership"
        verbose_name_plural = "memberships"
        unique_together = ("user", "project",)
        ordering = ["project", "user__full_name", "user__username", "user__email", "email"]

    def get_related_people(self):
        related_people = get_user_model().objects.filter(id=self.user.id)
        return related_people

    def clean(self):
        # TODO: Review and do it more robust
        memberships = Membership.objects.filter(user=self.user, project=self.project)
        if self.user and memberships.count() > 0 and memberships[0].id != self.id:
            raise ValidationError(_('The user is already member of the project'))


class ProjectDefaults(models.Model):
    default_task_status = models.OneToOneField(
        "projects.TaskStatus", on_delete=models.SET_NULL,
        related_name="+", null=True, blank=True,
        verbose_name=_("default task status"))
    default_priority = models.OneToOneField(
        "projects.Priority", on_delete=models.SET_NULL,
        related_name="+", null=True, blank=True,
        verbose_name=_("default priority"))
    default_severity = models.OneToOneField(
        "projects.Severity", on_delete=models.SET_NULL,
        related_name="+", null=True, blank=True,
        verbose_name=_("default severity"))
    default_issue_status = models.OneToOneField(
        "projects.IssueStatus", on_delete=models.SET_NULL, related_name="+",
        null=True, blank=True, verbose_name=_("default issue status"))
    default_issue_type = models.OneToOneField(
        "projects.IssueType", on_delete=models.SET_NULL, related_name="+",
        null=True, blank=True, verbose_name=_("default issue type"))

    class Meta:
        abstract = True


class Project(ProjectDefaults, models.Model):
    """
    Project model
    Project(id, name, slug, budget)
    """
    name = models.CharField(
        max_length=250, verbose_name='project')
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    description = models.TextField(
        null=False, blank=False,
        verbose_name=_('description'))
    date_created = models.DateTimeField(
        null=False, blank=False,
        verbose_name=_('date created'),
        default=timezone.now)
    date_modified = models.DateTimeField(
        null=False, blank=False,
        verbose_name=_('date modified'),
        default=timezone.now)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="owned_projects", verbose_name=_("owner"))
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="projects",
        through="Membership", verbose_name=_("members"),
        through_fields=("project", "user"))
    total_milestones = models.IntegerField(
        null=True, blank=True,
        verbose_name=_("total of milestones"))

    creation_template = models.ForeignKey(
        "projects.ProjectTemplate", on_delete=models.SET_NULL,
        null=True, blank=True, default=None,
        related_name="projects",
        verbose_name=_("creation template"))

    is_contact_activated = models.BooleanField(
        default=True, null=False, blank=True,
        verbose_name=_("active contact"))
    is_backlog_activated = models.BooleanField(
        default=True, null=False, blank=True,
        verbose_name=_("active backlog panel"))
    is_kanban_activated = models.BooleanField(
        default=False, null=False, blank=True,
        verbose_name=_("active kanban panel"))
    is_wiki_activated = models.BooleanField(
        default=True, null=False, blank=True,
        verbose_name=_("active wiki panel"))
    is_issues_activated = models.BooleanField(
        default=True, null=False, blank=True,
        verbose_name=_("active issues panel"))
    is_private = models.BooleanField(
        default=True, null=False, blank=True,
        verbose_name=_("is private"))
    anon_permissions = ArrayField(
        models.TextField(null=False, blank=False, choices=ANON_PERMISSIONS),
        null=True, blank=True, default=[],
        verbose_name=_("anonymous permissions"))
    public_permissions = ArrayField(
        models.TextField(null=False, blank=False, choices=MEMBERS_PERMISSIONS),
        null=True, blank=True, default=[],
        verbose_name=_("user permissions"))
    tasks_csv_uuid = models.CharField(
        max_length=32, editable=False, null=True,
        blank=True, default=None, db_index=True)
    issues_csv_uuid = models.CharField(
        max_length=32, editable=False,
        null=True, blank=True, default=None,
        db_index=True)

    # Totals:
    totals_updated_datetime = models.DateTimeField(
        null=False, blank=False, default=timezone.now,
        verbose_name=_("updated date time"), db_index=True)

    total_activity = models.PositiveIntegerField(
        null=False, blank=False, default=0,
        verbose_name=_("count"),
        db_index=True)

    total_activity_last_week = models.PositiveIntegerField(
        null=False, blank=False, default=0,
        verbose_name=_("activity last week"), db_index=True)

    total_activity_last_month = models.PositiveIntegerField(
        null=False, blank=False, default=0,
        verbose_name=_("activity last month"), db_index=True)

    total_activity_last_year = models.PositiveIntegerField(
        null=False, blank=False, default=0,
        verbose_name=_("activity last year"), db_index=True)

    budget = models.IntegerField(
        verbose_name=_("budget"),
        help_text='Amount allocated to this project.'
    )

    _importing = None

    class Meta:
        verbose_name = "project"
        verbose_name_plural = "projects"
        ordering = ["name", "id"]
        index_together = [
            ["name", "id"],
        ]

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<Project {0}>".format(self.id)

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.name)
    #     super(Project, self).save(*args, **kwargs)

    def save(self, *args, **kwargs):
        if not self._importing or not self.modified_date:
            self.modified_date = timezone.now()

        if not self.is_backlog_activated:
            self.total_milestones = None

        if self.anon_permissions is None:
            self.anon_permissions = []

        if self.public_permissions is None:
            self.public_permissions = []

        # if not self.slug:
        #     with advisory_lock("project-creation"):
        #         base_slug = "{}-{}".format(self.owner.username, self.name)
        #         self.slug = slugify_uniquely(base_slug, self.__class__)
        #         super().save(*args, **kwargs)
        if not self.slug:
            base_slug = "{}-{}".format(self.owner.username, self.name)
            self.slug = slugify_uniquely(base_slug, self.__class__)
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)

    # def refresh_totals(self, save=True):
    #     now = timezone.now()
    #     self.totals_updated_datetime = now

    #     Like = apps.get_model("likes", "Like")
    #     content_type = apps.get_model("contenttypes", "ContentType").objects.get_for_model(Project)
    #     qs = Like.objects.filter(content_type=content_type, object_id=self.id)

    #     self.total_fans = qs.count()

    #     qs_week = qs.filter(created_date__gte=now - relativedelta(weeks=1))
    #     self.total_fans_last_week = qs_week.count()

    #     qs_month = qs.filter(created_date__gte=now - relativedelta(months=1))
    #     self.total_fans_last_month = qs_month.count()

    #     qs_year = qs.filter(created_date__gte=now - relativedelta(years=1))
    #     self.total_fans_last_year = qs_year.count()

    #     # tl_model = apps.get_model("timeline", "Timeline")
    #     # namespace = build_project_namespace(self)

    #     qs = tl_model.objects.filter(namespace=namespace)
    #     self.total_activity = qs.count()

    #     qs_week = qs.filter(created__gte=now - relativedelta(weeks=1))
    #     self.total_activity_last_week = qs_week.count()

    #     qs_month = qs.filter(created__gte=now - relativedelta(months=1))
    #     self.total_activity_last_month = qs_month.count()

    #     qs_year = qs.filter(created__gte=now - relativedelta(years=1))
    #     self.total_activity_last_year = qs_year.count()

    #     if save:
    #         self.save(update_fields=[
    #             'totals_updated_datetime',
    #             'total_fans',
    #             'total_fans_last_week',
    #             'total_fans_last_month',
    #             'total_fans_last_year',
    #             'total_activity',
    #             'total_activity_last_week',
    #             'total_activity_last_month',
    #             'total_activity_last_year',
    #         ])

    @cached_property
    def cached_user_stories(self):
        return list(self.user_stories.all())

    @cached_property
    def cached_notify_policies(self):
        return {np.user.id: np for np in self.notify_policies.select_related("user", "project")}

    def cached_notify_policy_for_user(self, user):
        """
        Get notification level for specified project and user.
        """
        policy = self.cached_notify_policies.get(user.id, None)
        if policy is None:
            model_cls = apps.get_model("notifications", "NotifyPolicy")
            policy = model_cls.objects.create(
                project=self,
                user=user,
                notify_level=NotifyLevel.involved)

            del self.cached_notify_policies

        return policy

    @cached_property
    def cached_memberships(self):
        return {
            m.user.id: m for m in self.memberships.exclude(
                user__isnull=True).select_related(
                    "user", "project", "role")}

    def cached_memberships_for_user(self, user):
        return self.cached_memberships.get(user.id, None)

    def get_roles(self):
        return self.roles.all()

    def get_users(self, with_admin_privileges=None):
        user_model = get_user_model()
        members = self.memberships.all()
        if with_admin_privileges is not None:
            members = members.filter(Q(is_admin=True) | Q(user__id=self.owner.id))
        members = members.values_list("user", flat=True)
        return user_model.objects.filter(id__in=list(members))

    @property
    def project(self):
        return self

    def _get_q_watchers(self):
        return Q(notify_policies__project_id=self.id) & ~Q(notify_policies__notify_level=NotifyLevel.none)

    def get_watchers(self):
        return get_user_model().objects.filter(self._get_q_watchers())

    def get_related_people(self):
        related_people_q = Q()

        # - Owner
        if self.owner_id:
            related_people_q.add(Q(id=self.owner_id), Q.OR)

        # - Watchers
        related_people_q.add(self._get_q_watchers(), Q.OR)

        # - Apply filters
        related_people = get_user_model().objects.filter(related_people_q)

        # - Exclude inactive and system users and remove duplicate
        related_people = related_people.exclude(is_active=False)
        related_people = related_people.exclude(is_system=True)
        related_people = related_people.distinct()
        return related_people

    # def add_watcher(self, user, notify_level=NotifyLevel.all):
    #     notify_policy = create_notify_policy_if_not_exists(self, user)
    #     set_notify_policy_level(notify_policy, notify_level)

    # def remove_watcher(self, user):
    #     notify_policy = self.cached_notify_policy_for_user(user)
    #     set_notify_policy_level_to_ignore(notify_policy)

    # def delete_related_content(self):
    #     # NOTE: Remember to update code in taiga.projects.admin.ProjectAdmin.delete_selected
    #     from taiga.events.apps import (connect_events_signals,
    #                                    disconnect_events_signals)
    #     from taiga.projects.epics.apps import (connect_all_epics_signals,
    #                                          disconnect_all_epics_signals)
    #     from taiga.projects.tasks.apps import (connect_all_tasks_signals,
    #                                            disconnect_all_tasks_signals)
    #     from taiga.projects.userstories.apps import (connect_all_userstories_signals,
    #                                                  disconnect_all_userstories_signals)
    #     from taiga.projects.issues.apps import (connect_all_issues_signals,
    #                                             disconnect_all_issues_signals)
    #     from taiga.projects.apps import (connect_memberships_signals,
    #                                      disconnect_memberships_signals)

    #     disconnect_events_signals()
    #     disconnect_all_epics_signals()
    #     disconnect_all_issues_signals()
    #     disconnect_all_tasks_signals()
    #     disconnect_all_userstories_signals()
    #     disconnect_memberships_signals()

    #     try:
    #         self.epics.all().delete()
    #         self.tasks.all().delete()
    #         self.user_stories.all().delete()
    #         self.issues.all().delete()
    #         self.memberships.all().delete()
    #         self.roles.all().delete()
    #     finally:
    #         connect_events_signals()
    #         connect_all_issues_signals()
    #         connect_all_tasks_signals()
    #         connect_all_userstories_signals()
    #         connect_all_epics_signals()
    #         connect_memberships_signals()

    def budget_left(self):
        """ Budget amount left after expenses """
        expense_list = Expense.objects.filter(project=self)
        total_expense_amount = 0
        for expense in expense_list:
            total_expense_amount += expense.amount

        return self.budget - total_expense_amount

    def total_transactions(self):
        """ Count of total transactions for Project """
        expense_list = Expense.objects.filter(project=self)
        return len(expense_list)


# Tasks common models
class TaskStatus(models.Model):
    name = models.CharField(
        max_length=255, null=False, blank=False,
        verbose_name=_("name"))
    slug = models.SlugField(
        max_length=255, null=False, blank=True,
        verbose_name=_("slug"))
    order = models.IntegerField(
        default=10, null=False, blank=False,
        verbose_name=_("order"))
    is_closed = models.BooleanField(
        default=False, null=False, blank=True,
        verbose_name=_("is closed"))
    color = models.CharField(
        max_length=20, null=False,
        blank=False, default="#999999",
        verbose_name=_("color"))
    project = models.ForeignKey(
        "Project", on_delete=models.CASCADE,
        null=False, blank=False,
        related_name="task_statuses", verbose_name=_("project"))

    class Meta:
        verbose_name = "task status"
        verbose_name_plural = "task statuses"
        ordering = ["project", "order", "name"]
        unique_together = (("project", "name"), ("project", "slug"))

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        qs = self.project.task_statuses
        if self.id:
            qs = qs.exclude(id=self.id)

        self.slug = slugify_uniquely_for_queryset(self.name, qs)
        return super().save(*args, **kwargs)


# Issue common Models
class Priority(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False,
                            verbose_name=_("name"))
    order = models.IntegerField(default=10, null=False, blank=False,
                                verbose_name=_("order"))
    color = models.CharField(max_length=20, null=False, blank=False, default="#999999",
                             verbose_name=_("color"))
    project = models.ForeignKey(
        "Project", on_delete=models.CASCADE,
        null=False, blank=False,
        related_name="priorities", verbose_name=_("project"))

    class Meta:
        verbose_name = "priority"
        verbose_name_plural = "priorities"
        ordering = ["project", "order", "name"]
        unique_together = ("project", "name")

    def __str__(self):
        return self.name


class Severity(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False,
                            verbose_name=_("name"))
    order = models.IntegerField(default=10, null=False, blank=False,
                                verbose_name=_("order"))
    color = models.CharField(max_length=20, null=False, blank=False, default="#999999",
                             verbose_name=_("color"))
    project = models.ForeignKey(
        "Project", on_delete=models.CASCADE,
        null=False, blank=False,
        related_name="severities", verbose_name=_("project"))

    class Meta:
        verbose_name = "severity"
        verbose_name_plural = "severities"
        ordering = ["project", "order", "name"]
        unique_together = ("project", "name")

    def __str__(self):
        return self.name


class IssueStatus(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False,
                            verbose_name=_("name"))
    slug = models.SlugField(max_length=255, null=False, blank=True,
                            verbose_name=_("slug"))
    order = models.IntegerField(default=10, null=False, blank=False,
                                verbose_name=_("order"))
    is_closed = models.BooleanField(default=False, null=False, blank=True,
                                    verbose_name=_("is closed"))
    color = models.CharField(max_length=20, null=False, blank=False, default="#999999",
                             verbose_name=_("color"))
    project = models.ForeignKey(
        "Project", on_delete=models.CASCADE,
        null=False, blank=False,
        related_name="issue_statuses", verbose_name=_("project"))

    class Meta:
        verbose_name = "issue status"
        verbose_name_plural = "issue statuses"
        ordering = ["project", "order", "name"]
        unique_together = (("project", "name"), ("project", "slug"))

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        qs = self.project.issue_statuses
        if self.id:
            qs = qs.exclude(id=self.id)

        self.slug = slugify_uniquely_for_queryset(self.name, qs)
        return super().save(*args, **kwargs)


class IssueType(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False,
                            verbose_name=_("name"))
    order = models.IntegerField(default=10, null=False, blank=False,
                                verbose_name=_("order"))
    color = models.CharField(max_length=20, null=False, blank=False, default="#999999",
                             verbose_name=_("color"))
    project = models.ForeignKey(
        "Project", on_delete=models.CASCADE,
        null=False, blank=False,
        related_name="issue_types", verbose_name=_("project"))

    class Meta:
        verbose_name = "issue type"
        verbose_name_plural = "issue types"
        ordering = ["project", "order", "name"]
        unique_together = ("project", "name")

    def __str__(self):
        return self.name


class Category(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE,
        related_name='categories')
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Expense(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE,
        related_name='expenses')
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-amount', )


class ProjectTemplate(models.Model):
    name = models.CharField(max_length=250, null=False, blank=False,
                            verbose_name=_("name"))
    slug = models.SlugField(max_length=250, null=False, blank=True,
                            verbose_name=_("slug"), unique=True)
    description = models.TextField(null=False, blank=False,
                                   verbose_name=_("description"))
    order = models.BigIntegerField(default=timestamp_ms, null=False, blank=False,
                                   verbose_name=_("user order"))
    created_date = models.DateTimeField(null=False, blank=False,
                                        verbose_name=_("created date"),
                                        default=timezone.now)
    modified_date = models.DateTimeField(null=False, blank=False,
                                         verbose_name=_("modified date"))
    default_owner_role = models.CharField(max_length=50, null=False,
                                          blank=False,
                                          verbose_name=_("default owner's role"))
    is_contact_activated = models.BooleanField(default=True, null=False, blank=True,
                                               verbose_name=_("active contact"))
    is_backlog_activated = models.BooleanField(default=True, null=False, blank=True,
                                               verbose_name=_("active backlog panel"))
    is_kanban_activated = models.BooleanField(default=False, null=False, blank=True,
                                              verbose_name=_("active kanban panel"))
    is_wiki_activated = models.BooleanField(default=True, null=False, blank=True,
                                            verbose_name=_("active wiki panel"))
    is_issues_activated = models.BooleanField(default=True, null=False, blank=True,
                                              verbose_name=_("active issues panel"))

    default_options = JSONField(null=True, blank=True, verbose_name=_("default options"))
    epic_statuses = JSONField(null=True, blank=True, verbose_name=_("epic statuses"))
    us_statuses = JSONField(null=True, blank=True, verbose_name=_("us statuses"))
    points = JSONField(null=True, blank=True, verbose_name=_("points"))
    task_statuses = JSONField(null=True, blank=True, verbose_name=_("task statuses"))
    issue_statuses = JSONField(null=True, blank=True, verbose_name=_("issue statuses"))
    issue_types = JSONField(null=True, blank=True, verbose_name=_("issue types"))
    priorities = JSONField(null=True, blank=True, verbose_name=_("priorities"))
    severities = JSONField(null=True, blank=True, verbose_name=_("severities"))
    roles = JSONField(null=True, blank=True, verbose_name=_("roles"))
    epic_custom_attributes = JSONField(null=True, blank=True, verbose_name=_("epic custom attributes"))
    us_custom_attributes = JSONField(null=True, blank=True, verbose_name=_("us custom attributes"))
    task_custom_attributes = JSONField(null=True, blank=True, verbose_name=_("task custom attributes"))
    issue_custom_attributes = JSONField(null=True, blank=True, verbose_name=_("issue custom attributes"))

    _importing = None

    class Meta:
        verbose_name = "project template"
        verbose_name_plural = "project templates"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<Project Template {0}>".format(self.slug)

    def save(self, *args, **kwargs):
        if not self._importing or not self.modified_date:
            self.modified_date = timezone.now()
        if not self.slug:
            self.slug = slugify_uniquely(self.name, self.__class__)
        super().save(*args, **kwargs)

    def load_data_from_project(self, project):
        self.is_contact_activated = project.is_contact_activated
        self.is_epics_activated = project.is_epics_activated
        self.is_backlog_activated = project.is_backlog_activated
        self.is_kanban_activated = project.is_kanban_activated
        self.is_wiki_activated = project.is_wiki_activated
        self.is_issues_activated = project.is_issues_activated
        self.videoconferences = project.videoconferences
        self.videoconferences_extra_data = project.videoconferences_extra_data

        self.default_options = {
            "points": getattr(project.default_points, "name", None),
            "epic_status": getattr(project.default_epic_status, "name", None),
            "us_status": getattr(project.default_us_status, "name", None),
            "task_status": getattr(project.default_task_status, "name", None),
            "issue_status": getattr(project.default_issue_status, "name", None),
            "issue_type": getattr(project.default_issue_type, "name", None),
            "priority": getattr(project.default_priority, "name", None),
            "severity": getattr(project.default_severity, "name", None)
        }

        self.epic_statuses = []
        for epic_status in project.epic_statuses.all():
            self.epic_statuses.append({
                "name": epic_status.name,
                "slug": epic_status.slug,
                "is_closed": epic_status.is_closed,
                "color": epic_status.color,
                "order": epic_status.order,
            })

        self.us_statuses = []
        for us_status in project.us_statuses.all():
            self.us_statuses.append({
                "name": us_status.name,
                "slug": us_status.slug,
                "is_closed": us_status.is_closed,
                "is_archived": us_status.is_archived,
                "color": us_status.color,
                "wip_limit": us_status.wip_limit,
                "order": us_status.order,
            })

        self.points = []
        for us_point in project.points.all():
            self.points.append({
                "name": us_point.name,
                "value": us_point.value,
                "order": us_point.order,
            })

        self.task_statuses = []
        for task_status in project.task_statuses.all():
            self.task_statuses.append({
                "name": task_status.name,
                "slug": task_status.slug,
                "is_closed": task_status.is_closed,
                "color": task_status.color,
                "order": task_status.order,
            })

        self.issue_statuses = []
        for issue_status in project.issue_statuses.all():
            self.issue_statuses.append({
                "name": issue_status.name,
                "slug": issue_status.slug,
                "is_closed": issue_status.is_closed,
                "color": issue_status.color,
                "order": issue_status.order,
            })

        self.issue_types = []
        for issue_type in project.issue_types.all():
            self.issue_types.append({
                "name": issue_type.name,
                "color": issue_type.color,
                "order": issue_type.order,
            })

        self.priorities = []
        for priority in project.priorities.all():
            self.priorities.append({
                "name": priority.name,
                "color": priority.color,
                "order": priority.order,
            })

        self.severities = []
        for severity in project.severities.all():
            self.severities.append({
                "name": severity.name,
                "color": severity.color,
                "order": severity.order,
            })

        self.roles = []
        for role in project.roles.all():
            self.roles.append({
                "name": role.name,
                "slug": role.slug,
                "permissions": role.permissions,
                "order": role.order,
                "computable": role.computable
            })

        self.epic_custom_attributes = []
        for ca in project.epiccustomattributes.all():
            self.epic_custom_attributes.append({
                "name": ca.name,
                "description": ca.description,
                "type": ca.type,
                "order": ca.order
            })

        self.us_custom_attributes = []
        for ca in project.userstorycustomattributes.all():
            self.us_custom_attributes.append({
                "name": ca.name,
                "description": ca.description,
                "type": ca.type,
                "order": ca.order
            })

        self.task_custom_attributes = []
        for ca in project.taskcustomattributes.all():
            self.task_custom_attributes.append({
                "name": ca.name,
                "description": ca.description,
                "type": ca.type,
                "order": ca.order
            })

        self.issue_custom_attributes = []
        for ca in project.issuecustomattributes.all():
            self.issue_custom_attributes.append({
                "name": ca.name,
                "description": ca.description,
                "type": ca.type,
                "order": ca.order
            })

        try:
            owner_membership = Membership.objects.get(project=project, user=project.owner)
            self.default_owner_role = owner_membership.role.slug
        except Membership.DoesNotExist:
            self.default_owner_role = self.roles[0].get("slug", None)

        self.tags = project.tags
        self.tags_colors = project.tags_colors
        self.is_looking_for_people = project.is_looking_for_people
        self.looking_for_people_note = project.looking_for_people_note

    def apply_to_project(self, project):
        Role = apps.get_model("users", "Role")

        if project.id is None:
            raise Exception("Project need an id (must be a saved project)")

        project.creation_template = self
        project.is_contact_activated = self.is_contact_activated
        project.is_epics_activated = self.is_epics_activated
        project.is_backlog_activated = self.is_backlog_activated
        project.is_kanban_activated = self.is_kanban_activated
        project.is_wiki_activated = self.is_wiki_activated
        project.is_issues_activated = self.is_issues_activated
        project.videoconferences = self.videoconferences
        project.videoconferences_extra_data = self.videoconferences_extra_data

        for task_status in self.task_statuses:
            TaskStatus.objects.create(
                name=task_status["name"],
                slug=task_status["slug"],
                is_closed=task_status["is_closed"],
                color=task_status["color"],
                order=task_status["order"],
                project=project
            )

        for issue_status in self.issue_statuses:
            IssueStatus.objects.create(
                name=issue_status["name"],
                slug=issue_status["slug"],
                is_closed=issue_status["is_closed"],
                color=issue_status["color"],
                order=issue_status["order"],
                project=project
            )

        for issue_type in self.issue_types:
            IssueType.objects.create(
                name=issue_type["name"],
                color=issue_type["color"],
                order=issue_type["order"],
                project=project
            )

        for priority in self.priorities:
            Priority.objects.create(
                name=priority["name"],
                color=priority["color"],
                order=priority["order"],
                project=project
            )

        for severity in self.severities:
            Severity.objects.create(
                name=severity["name"],
                color=severity["color"],
                order=severity["order"],
                project=project
            )

        for role in self.roles:
            Role.objects.create(
                name=role["name"],
                slug=role["slug"],
                order=role["order"],
                computable=role["computable"],
                project=project,
                permissions=role['permissions']
            )

        if self.task_statuses:
            project.default_task_status = TaskStatus.objects.get(name=self.default_options["task_status"],
                                                                 project=project)
        if self.issue_statuses:
            project.default_issue_status = IssueStatus.objects.get(name=self.default_options["issue_status"],
                                                                   project=project)

        if self.issue_types:
            project.default_issue_type = IssueType.objects.get(name=self.default_options["issue_type"],
                                                               project=project)

        if self.priorities:
            project.default_priority = Priority.objects.get(name=self.default_options["priority"],
                                                            project=project)

        if self.severities:
            project.default_severity = Severity.objects.get(name=self.default_options["severity"],
                                                            project=project)

        # for ca in self.task_custom_attributes:
        #     TaskCustomAttribute.objects.create(
        #         name=ca["name"],
        #         description=ca["description"],
        #         type=ca["type"],
        #         order=ca["order"],
        #         project=project
        #     )

        # for ca in self.issue_custom_attributes:
        #     IssueCustomAttribute.objects.create(
        #         name=ca["name"],
        #         description=ca["description"],
        #         type=ca["type"],
        #         order=ca["order"],
        #         project=project
        #     )

        project.tags = self.tags
        project.tags_colors = self.tags_colors
        project.is_looking_for_people = self.is_looking_for_people
        project.looking_for_people_note = self.looking_for_people_note

        return project