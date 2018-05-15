import uuid

from django.contrib.auth.models import UserManager, AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

# from django_pglocks import advisory_lock

from ..core.permissions.choices import MEMBERS_PERMISSIONS
from ..core.utils.files import get_file_path
from ..core.utils.slug import slugify_uniquely
# from ..core.utils.time import timestamp_ms
from ..core.utils.tokens import get_token_for_user
from ..projects.notifications.choices import NotifyLevel


# Models defined here
def get_user_file_path(instance, filename):
    return get_file_path(instance, filename, "user")


class PermissionsMixin(models.Model):
    """
    A mixin class that adds the fields and methods necessary to support
    Django"s Permission model using the ModelBackend.
    """
    is_superuser = models.BooleanField(
        _("superuser status"), default=False,
        help_text=_("Designates that this user has all permissions without "
                    "explicitly assigning them."))

    class Meta:
        abstract = True

    def has_perm(self, perm, obj=None):
        """ Returns True if the user is superadmin and is active """
        return self.is_active and self.is_superuser

    def has_perms(self, perm_list, obj=None):
        """ Returns True if the user is superadmin and is active """
        return self.is_active and self.is_superuser

    def has_module_perms(self, app_label):
        """ Returns True if the user is superadmin and is active """
        return self.is_active and self.is_superuser

    @property
    def is_staff(self):
        return self.is_superuser


def get_default_uuid():
    return uuid.uuid4().hex


class User(AbstractUser):
    """ Extends User model, related to :model: 'auth.User' """
    full_name = models.CharField(
        _("full name"), max_length=256, blank=True,
        help_text=_('If different from First Name + Last Name'))
    bio = models.TextField(
        null=False, blank=True, default="", verbose_name=_("biography"))
    photo = models.FileField(
        upload_to=get_user_file_path,
        max_length=500, null=True, blank=True,
        verbose_name=_("photo"))
    date_joined = models.DateTimeField(
        _("date joined"), default=timezone.now)
    lang = models.CharField(
        max_length=20, null=True, blank=True, default="",
        verbose_name=_("default language"))
    timezone = models.CharField(
        max_length=20, null=True, blank=True, default="",
        verbose_name=_("default timezone"))

    is_system = models.BooleanField(
        null=False, blank=False, default=False)

    objects = UserManager()

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
        ordering = ["username"]

    def __str__(self):
        return self.get_full_name()

    def _fill_cached_memberships(self):
        self._cached_memberships = {}
        qs = self.memberships.select_related("user", "project", "role")
        for membership in qs.all():
            self._cached_memberships[membership.project.id] = membership

    @property
    def cached_memberships(self):
        if self._cached_memberships is None:
            self._fill_cached_memberships()

        return self._cached_memberships.values()

    def cached_membership_for_project(self, project):
        if self._cached_memberships is None:
            self._fill_cached_memberships()

        return self._cached_memberships.get(project.id, None)

    def get_absolute_url(self):
        """ Redirects to User detail page """
        return reverse('users:detail', kwargs={'username': self.username})

    def is_watcher(self, obj):
        if self._cached_watched_ids is None:
            self._cached_watched_ids = set()
            for watched in self.watched.select_related("content_type").all():
                watched_id = "{}-{}".format(watched.content_type.id, watched.object_id)
                self._cached_watched_ids.add(watched_id)

            notify_policies = self.notify_policies.select_related("project")\
                .exclude(notify_level=NotifyLevel.none)

            for notify_policy in notify_policies:
                obj_type = ContentType.objects.get_for_model(notify_policy.project)
                watched_id = "{}-{}".format(obj_type.id, notify_policy.project.id)
                self._cached_watched_ids.add(watched_id)

        obj_type = ContentType.objects.get_for_model(obj)
        obj_id = "{}-{}".format(obj_type.id, obj.id)
        return obj_id in self._cached_watched_ids

    def get_notify_level(self, project):
        if self._cached_notify_levels is None:
            self._cached_notify_levels = {}
            for notify_policy in self.notify_policies.select_related("project"):
                self._cached_notify_levels[notify_policy.project.id] = notify_policy.notify_level

        return self._cached_notify_levels.get(project.id, None)

    def get_short_name(self):
        "Returns the short name for the user."
        return self.username

    def get_full_name(self):
        return self.full_name or self.username or self.email

    # def contacts_visible_by_user(self, user):
    #     qs = User.objects.filter(is_active=True)
    #     project_ids = services.get_visible_project_ids(self, user)
    #     qs = qs.filter(memberships__project_id__in=project_ids)
    #     qs = qs.exclude(id=self.id)
    #     return qs

    def save(self, *args, **kwargs):
        get_token_for_user(self, "cancel_account")
        super().save(*args, **kwargs)

    # def cancel(self):
    #     with advisory_lock("delete-user"):
    #         deleted_user_prefix = "deleted-user-{}".format(timestamp_ms())
    #         self.username = slugify_uniquely(deleted_user_prefix, User, slugfield="username")
    #         self.email = "{}@kruizer.com".format(self.username)
    #         self.is_active = False
    #         self.full_name = "Deleted user"
    #         self.color = ""
    #         self.bio = ""
    #         self.lang = ""
    #         self.theme = ""
    #         self.timezone = ""
    #         self.colorize_tags = True
    #         self.token = None
    #         self.set_unusable_password()
    #         self.photo = None
    #         self.save()
    #     self.auth_data.all().delete()

    #     # # Blocking all owned projects
    #     # self.owned_projects.update(blocked_code=BLOCKED_BY_OWNER_LEAVING)

    #     # Remove all memberships
    #     self.memberships.all().delete()


class Role(models.Model):
    name = models.CharField(
        max_length=200, null=False, blank=False,
        verbose_name=_("name"))
    slug = models.SlugField(
        max_length=250, null=False, blank=True,
        verbose_name=_("slug"))
    permissions = ArrayField(
        models.TextField(null=False, blank=False, choices=MEMBERS_PERMISSIONS),
        null=True, blank=True, default=[], verbose_name=_("permissions"))
    order = models.IntegerField(
        default=10, null=False, blank=False,
        verbose_name=_("order"))
    # null=True is for make work django 1.7 migrations. project
    # field causes some circular dependencies, and due to this
    # it can not be serialized in one transactional migration.
    project = models.ForeignKey(
        "projects.Project", on_delete=models.CASCADE,
        null=True, blank=False,
        related_name="roles", verbose_name=_("project"))
    computable = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_uniquely(self.name, self.__class__)

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "role"
        verbose_name_plural = "roles"
        ordering = ["order", "slug"]
        unique_together = (("slug", "project"),)

    def __str__(self):
        return self.name


# On Role object is changed, update all membership
# related to current role.
@receiver(models.signals.post_save, sender=Role,
          dispatch_uid="role_post_save")
def role_post_save(sender, instance, created, **kwargs):
    # ignore if object is just created
    if created:
        return

    instance.project.update_role_points()
