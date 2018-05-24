""" Models related to Tasks """
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from mptt.managers import TreeManager
from mptt.models import MPTTModel, TreeForeignKey

from ...core.models import TimeStampedModel
from ...core.utils.slug import slugify_uniquely, slugify_uniquely_for_queryset
from ...pmi.models import Process
from .project import Project
from .stakeholder import Stakeholder


# Models
class Task(TimeStampedModel, MPTTModel):
    """
    Defines the activities of the Work Breakdown Structure (WBS). The WBS is
    the process of subdividing project deliverables and project work into
    smaller, more manageable components.
    """
    NEW = 0
    STARTED = 1
    CLOSED = 2

    TASK_STATUS_CHOICES = [
        (NEW, 'Not Started'),
        (STARTED, 'In Progress'),
        (CLOSED, 'Completed'),
    ]

    name = models.CharField(
        max_length=255, null=False, blank=False,
        verbose_name=_("name"))
    slug = models.SlugField(
        max_length=255, null=False, blank=True,
        verbose_name=_("slug"))
    description = models.TextField(
        _('description'), blank=True,
        help_text=_('Description of activity or task.'))

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE,
        null=False, blank=False,
        related_name="tasks", verbose_name=_("project"))

    resources = models.ManyToManyField(
        Stakeholder, blank=False,
        related_name="tasks",
        verbose_name=_("resources"))

    process = models.ForeignKey(
        Process, on_delete=models.SET_NULL,
        null=True, blank=True,
        help_text=_('PMI process for this task.')
    )

    # Related activities
    parent = TreeForeignKey(
        'self',
        related_name='children',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_('parent activity'))

    predecessor = TreeForeignKey(
        'self',
        related_name='predecessors',
        null=True, blank=True,
        on_delete=models.SET_NULL)

    successor = TreeForeignKey(
        'self',
        related_name='successors',
        null=True, blank=True,
        on_delete=models.SET_NULL)

    order = models.IntegerField(
        default=10, null=False, blank=False,
        verbose_name=_("order"))

    # Task status
    status = models.CharField(
        max_length=7,
        null=True, blank=True,
        choices=TASK_STATUS_CHOICES,
        default=NEW,
    )
    is_milestone = models.BooleanField(
        default=False, null=False, blank=True,
        verbose_name=_("is milestone"))

    objects = TreeManager()

    class Meta:
        """ Category's meta informations. """
        verbose_name = "task"
        ordering = ["project", "order", "name"]
        unique_together = (("project", "name"), ("project", "slug"))
        ordering = ["project", "created"]
        permissions = (
            ("view_milestone", "Can view milestone"),
        )

    class MPTTMeta:
        """ Category MPTT's meta informations. """
        order_insertion_by = ['name']

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<Milestone {0}>".format(self.id)

    def clean(self):
        # Don't allow draft entries to have a pub_date.
        if self.estimated_start and self.estimated_finish and self.estimated_start > self.estimated_finish:
            raise ValidationError(_('The estimated start must be previous to the estimated finish.'))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_uniquely(self.name, self.__class__)
        qs = self.project.tasks
        if self.id:
            qs = qs.exclude(id=self.id)

        self.slug = slugify_uniquely_for_queryset(self.name, qs)
        return super().save(*args, **kwargs)

    @property
    def tree_path(self):
        """
        Returns activity's tree path
        by concatening the slug of its ancestors.
        """
        if self.parent_id:
            return '/'.join(
                [ancestor.slug for ancestor in self.get_ancestors()] +
                [self.slug])
        return self.slug

    def get_absolute_url(self):
        """
        Builds and returns the activity's URL
        based on its tree path.
        """
        return reverse('projects:task_detail', args=(self.tree_path,))
