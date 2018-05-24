""" Models related to Issues """

from django.db import models
from django.utils.translation import ugettext_lazy as _

from ...core.models import TimeStampedModel
from ...core.utils.slug import slugify_uniquely_for_queryset
from ..choices import RANK_OPTIONS
from ..mixins import DueDateMixin

from .. import models as proj_models


class IssueStatus(models.Model):
    """ Available status options for :model:Issue """
    name = models.CharField(
        max_length=100, null=False, blank=False,
        verbose_name=_("name"))
    slug = models.SlugField(
        max_length=100, null=False, blank=True,
        verbose_name=_("slug"))
    order = models.IntegerField(
        default=10, null=False, blank=False,
        verbose_name=_("order"))
    is_closed = models.BooleanField(
        default=False, null=False, blank=True,
        verbose_name=_("is closed"))
    color = models.CharField(
        max_length=20, null=False, blank=False, default="#999999",
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


class IssueProgress(TimeStampedModel, models.Model):
    """ Model containing updates on :model:Issue resolution  """
    issue = models.ForeignKey(
        'Issue', on_delete=models.CASCADE,
        related_name='progress_notes', )
    progress = models.TextField(
        null=True, blank=True,
        help_text=_('Update on issue resolution (may not be edited later).')
    )

    class Meta:
        ordering = ['-created']


class Issue(TimeStampedModel, DueDateMixin, models.Model):
    """ Stores information about an Issue """
    project = models.ForeignKey(
        proj_models.Project, on_delete=models.CASCADE,
        related_name='issues')
    name = models.CharField(
        _('name'), max_length=250, )
    slug = models.SlugField(
        max_length=250, unique=True, blank=True,
        help_text=_('Used to create the Issue URL.'))
    description = models.TextField(
        _('description'),
        help_text=_('Detailed description of issue including effects on project.')
    )
    task = models.ManyToManyField(
        proj_models.Task, related_name='issues',
        help_text=_('Task(s) this issue affects or is related to.')
    )
    category = models.ManyToManyField(
        proj_models.Category, related_name='issues',
        verbose_name=_('categories'))
    impact = models.TextField(
        null=True, blank=True,
        verbose_name=_('project impact'),
        help_text=_('How will the issue impact the scope, schedule and/or cost of the project?')
    )
    importance = models.IntegerField(
        choices=RANK_OPTIONS, default=1,
        help_text=_('How CRITICAL is it to the project?'))
    urgency = models.IntegerField(
        choices=RANK_OPTIONS, default=1,
        help_text=_('How IMMEDIATELY is it needed?'))
    priority = models.IntegerField(
        null=True, help_text=_('(CALCULATED)'))
    status = models.ForeignKey(
        IssueStatus, on_delete=models.CASCADE,
        null=True, blank=True,
        related_name="issues", verbose_name=_("status"))
    owner = models.ForeignKey(
        proj_models.Stakeholder, on_delete=models.SET_NULL,
        null=True, blank=True, default=None,
        related_name='owned_issues', verbose_name=_('business owner'),
        help_text=_('Stakeholder affected by / knowledgeable about this issue.'))
    assigned_to = models.ForeignKey(
        proj_models.Stakeholder, on_delete=models.SET_NULL,
        blank=True, null=True, default=None,
        related_name="issues_assigned_to_me",
        verbose_name=_("assigned to"),
        help_text=_('Person accountable for resolution.'))
    resolution_plan = models.TextField(
        null=True, blank=True,
        help_text=_('Plan to resolve issue.'))
    resolved = models.DateField(
        null=True, blank=True, verbose_name=_('date completed'))

    class Meta:
        """ Issue model Meta """
        ordering = ['priority', 'project', 'name']
