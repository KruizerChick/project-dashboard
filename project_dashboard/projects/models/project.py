from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

from ...core.models import TimeStampedModel
from ...core.permissions.choices import ANON_PERMISSIONS, MEMBERS_PERMISSIONS
from ...core.utils.time import timestamp_ms

from .stakeholder import Role, Stakeholder
from .category import Category


USER = get_user_model()


# Models
class Membership(TimeStampedModel, models.Model):
    """
    This model stores all project memberships. Also stores invitations
    to memberships that does not have assigned user.
    """
    stakeholder = models.ForeignKey(
        Stakeholder, on_delete=models.SET_NULL,
        null=True, blank=True, default=None,
        related_name="memberships")
    project = models.ForeignKey(
        "Project", on_delete=models.CASCADE,
        null=False, blank=False,
        related_name="memberships")
    role = models.ForeignKey(
        Role, on_delete=models.CASCADE,
        null=False, blank=False,
        related_name="memberships")
    is_admin = models.BooleanField(
        default=False, null=False, blank=False)

    # Invitation metadata
    email = models.EmailField(
        max_length=255, default=None, null=True, blank=True,
        verbose_name=_("email"))
    token = models.CharField(
        max_length=60,
        blank=True, null=True, default=None,
        verbose_name=_("token"))

    invited_by = models.ForeignKey(
        USER, on_delete=models.SET_NULL,
        related_name="ihaveinvited+",
        null=True, blank=True)

    invitation_extra_text = models.TextField(
        null=True, blank=True,
        verbose_name=_("invitation extra text"))

    user_order = models.BigIntegerField(
        default=timestamp_ms, null=False, blank=False,
        verbose_name=_("user order"))

    class Meta:
        verbose_name = "membership"
        verbose_name_plural = "memberships"
        unique_together = ("stakeholder", "project",)
        ordering = ["project", "stakeholder__full_name", "stakeholder__user", "stakeholder__email_address"]

    def get_related_people(self):
        related_people = get_user_model().objects.filter(id=self.user.id)
        return related_people

    def clean(self):
        # TODO: Review and do it more robust
        memberships = Membership.objects.filter(user=self.user, project=self.project)
        if self.user and memberships.count() > 0 and memberships[0].id != self.id:
            raise ValidationError(_('The user is already member of the project'))


class CoreProject(TimeStampedModel, models.Model):
    """
    Abstract core project model storing basic information
    about a single project.
    """
    name = models.CharField(
        max_length=250, verbose_name=_('project'))
    slug = models.SlugField(
        max_length=250, unique=True, blank=True,
        help_text=_('Used to create the project URL.'))
    description = models.TextField(
        null=False, blank=False,
        verbose_name=_('description'))
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="owned_projects", verbose_name=_("owner"))
    is_closed = models.BooleanField(
        default=False, null=False, blank=True,
        verbose_name=_('closed'))
    is_phased = models.BooleanField(
        default=False, null=False, blank=True,
        verbose_name=_('phased'))
    anon_permissions = ArrayField(
        models.TextField(null=False, blank=False, choices=ANON_PERMISSIONS),
        null=True, blank=True, default=[],
        verbose_name=_("anonymous permissions"))
    public_permissions = ArrayField(
        models.TextField(null=False, blank=False, choices=MEMBERS_PERMISSIONS),
        null=True, blank=True, default=[],
        verbose_name=_("user permissions"))

    objects = models.Manager()

    class Meta:
        """ CoreProject meta information. """
        abstract = True
        verbose_name = _('project')
        verbose_name_plural = _('projects')
        ordering = ['name', 'id']
        index_together = [['name', 'id'], ]

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<Project {0}>".format(self.id)

    # TODO: Do we need this with the TimeStampedModel?
    # def save(self, *args, **kwargs):
    #     """
    #     Overrides the save method to update the
    #     the modified field.
    #     """
    #     self.last_update = timezone.now()
    #     super(CoreProject, self).save(*args, **kwargs)


class RelatedProject(models.Model):
    """
    Abstract model class for making manual relations
    between the differents projects.
    """
    related = models.ManyToManyField(
        'self', blank=True,
        verbose_name=_('related projects'),
        help_text=_('Projects that are similar (but NOT dependent upon) this one.'))
    predecessors = models.ManyToManyField(
        'self', blank=True,
        verbose_name=_('predecessor projects'),
        help_text=_('Projects that MUST be completed beforehand.'))
    successors = models.ManyToManyField(
        'self', blank=True,
        verbose_name=_('successor projects'),
        help_text=_('Projects that depend on this one to complete.'))

    class Meta:
        abstract = True


class StakeholderProject(models.Model):
    """
    Abstract model class for making manual relations
    among different stakeholders projects.
    """
    stakeholder = models.ManyToManyField(
        Stakeholder, blank=True,
        related_name='projects',
        verbose_name=_('stakeholder'))
    role = models.ManyToManyField(
        Role, blank=True,
        related_name='projects',
        verbose_name=_('role'))

    class Meta:
        abstract = True


class CategoriesProject(models.Model):
    """ Abstract model class to categorize the entries. """
    categories = models.ManyToManyField(
        Category, blank=True,
        related_name='projects',
        verbose_name=_('categories'))

    class Meta:
        abstract = True


class LoginRequiredProject(models.Model):
    """
    Abstract model class to restrict the display
    of the project on authenticated users.
    """
    login_required = models.BooleanField(
        _('login required'), default=False,
        help_text=_('Only authenticated users can view the project.'))

    class Meta:
        abstract = True


class PasswordRequiredProject(models.Model):
    """
    Abstract model class to restrict the display
    of the project to users knowing the password.
    """
    password = models.CharField(
        _('password'), max_length=50, blank=True,
        help_text=_('Protects the project with a password.'))

    class Meta:
        abstract = True


class AbstractProject(
        CoreProject,
        RelatedProject,
        StakeholderProject,
        CategoriesProject,
        LoginRequiredProject,
        PasswordRequiredProject):
    """
    Final abstract entry model class assembling
    all the abstract entry model classes into a single one.

    In this manner we can override some fields without
    reimplemting all the AbstractProject.
    """

    class Meta(CoreProject.Meta):
        abstract = True


class Project(AbstractProject):
    """
    The final Project model based on inheritence.
    """
