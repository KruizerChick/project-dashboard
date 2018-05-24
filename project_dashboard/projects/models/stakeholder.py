""" Stakeholders models for Project Dashboard """

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField

from ...core.choices import RANK_OPTIONS
from ...core.models import TimeStampedModel
from ...core.permissions.choices import MEMBERS_PERMISSIONS
from ...core.utils.slug import slugify_uniquely
from ..notifications.choices import NotifyLevel

# from .project import Project

User = get_user_model()


# Create your models here.
class Role(models.Model):
    INTERNAL = 'I'
    EXTERNAL = 'E'
    ROLE_TYPE_CHOICES = (
        (INTERNAL, 'Internal'),
        (EXTERNAL, 'External'),
    )
    name = models.CharField(
        max_length=200, null=False, blank=False,
        verbose_name=_('name'))
    slug = models.SlugField(
        max_length=250, null=False, blank=True,
        verbose_name=_('slug'))
    description = models.TextField(
        verbose_name=_('description'),
        null=True, blank=True,
    )
    permissions = ArrayField(
        models.TextField(
            null=False, blank=False, choices=MEMBERS_PERMISSIONS),
        null=True, blank=True, default=[], verbose_name=_('permissions'))
    role_type = models.CharField(
        max_length=1, choices=ROLE_TYPE_CHOICES,
        default=INTERNAL,
        help_text=_('Relative to the project team.')
    )
    order = models.IntegerField(
        default=10, null=False, blank=False,
        verbose_name=_('order'))

    computable = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_uniquely(self.name, self.__class__)

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'role'
        verbose_name_plural = 'roles'
        ordering = ['order', 'slug']
        # unique_together = (('slug', 'project'),)

    def __str__(self):
        return self.name


# On Role object is changed, update all membership related to current role.
@receiver(models.signals.post_save, sender=Role,
          dispatch_uid='role_post_save')
def role_post_save(sender, instance, created, **kwargs):
    # ignore if object is just created
    if created:
        return

    instance.project.update_role_points()


class Stakeholder(TimeStampedModel, models.Model):
    """
    Stores Stakeholder information; related to :model:`Project`;
    can link to :model:`User`, but not required.
    """
    user = models.OneToOneField(
        User, on_delete=models.SET_NULL,
        null=True, blank=True,
        help_text=_('(Optional) Link to User if available')
    )
    slug = models.SlugField(
        max_length=250, null=False, blank=True,
        verbose_name=_('slug'),
        help_text=_('Used for Stakeholder URL.'))

    # If not system User
    first_name = models.CharField(
        max_length=50, blank=True,
    )
    last_name = models.CharField(
        max_length=50, blank=True,
    )

    email_address = models.EmailField(
        max_length=100, null=True, blank=True,
    )

    title = models.CharField(
        max_length=100, blank=True,
    )
    organization = models.CharField(
        max_length=100, blank=True,
        help_text=_('Company, business unit or department.'),
    )
    phone_number = PhoneNumberField(blank=True)

    # Project-specific info
    impact = models.IntegerField(
        choices=RANK_OPTIONS, default=1,
        help_text=_('Impact of this stakeholder on the project: 1 (low) - 5 (high)'),
    )
    influence = models.IntegerField(
        choices=RANK_OPTIONS, default=1,
        help_text=_('Influence of this stakeholder: 1 (low) - 5 (high)'),
    )
    risk_tolerance = models.IntegerField(
        choices=RANK_OPTIONS, default=1,
        help_text=_('Risk tolerance of this stakeholder: 1 (low) - 5 (high)'),
    )
    needs = models.TextField(
        blank=True, null=True,
        help_text=_('Items that are NOT OPTIONAL for this Stakeholder.')
    )
    wants = models.TextField(
        blank=True, null=True,
        help_text=_('Items that are OPTIONAL for this Stakeholder.')
    )
    expectations = models.TextField(
        blank=True, null=True,
        help_text=_('Unusual or emphatic expectations that need to be noted.')
    )
    strategy = models.TextField(
        blank=True, null=True,
        help_text=_('Strategies and tactics to maximize positive influence and minimize negative influence.')
    )

    class Meta:
        ordering = ['-influence', '-impact']
        verbose_name = _('stakeholder')
        # unique_together = (('id', 'projects'),)

    def __str__(self):
        """ Return the full name of the stakeholder """
        return '%s %s' % (self.first_name, self.last_name)

    @property
    def full_name(self):
        """ Returns the person's full name. """
        try:
            return self.user.full_name
        except AttributeError:
            return '%s %s' % (self.first_name, self.last_name)

    def _fill_cached_memberships(self):
        self._cached_memberships = {}
        qs = self.memberships.select_related(
            "stakeholder", "project", "role")
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

    # def contacts_visible_by_user(self, user):
    #     qs = User.objects.filter(is_active=True)
    #     project_ids = services.get_visible_project_ids(self, user)
    #     qs = qs.filter(memberships__project_id__in=project_ids)
    #     qs = qs.exclude(id=self.id)
    #     return qs

    # TODO: Figure out how to save User first_name and last_name into
    #       Stakeholder.first_name and Stakeholder.last_name fields
    # def save(self, *args, **kwargs):
    #     if not self.user:
    #         return
    #     else:
    #         self.first_name = User.first_name
    #         self.last_name = User.last_name
    #         super().save(*args, **kwargs)  # Call the "real" save() method.
