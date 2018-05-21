from django.db import models
from django.utils.translation import ugettext_lazy as _


# Create your models here.
class ProcessGroup(models.Model):
    """ Define how project management processes are organized. """
    name = models.CharField(_('name'), max_length=100)
    description = models.TextField(_('description'), blank=True)

    def __str__(self):
        return self.name


class KnowledgeArea(models.Model):
    """
    Areas of specialization that are commonly employed or set of processes
    associated with a particular topic when managing projects.
    """
    name = models.CharField(_('name'), max_length=100)
    description = models.TextField(_('description'), blank=True)

    def __str__(self):
        return self.name


class Process(models.Model):
    """ Project management processes used to meet project objectives. """
    name = models.CharField(_('name'), max_length=100)
    slug = models.SlugField(
        _('slug'), unique=True, max_length=100,
        help_text=_("Used to build the process' URL."))
    order = models.CharField(
        _('PMBOK ID'), max_length=10,
        help_text=_('Process ID from the PMBOK Guide.'))
    description = models.TextField(_('description'), blank=True)

    process_group = models.ForeignKey(
        ProcessGroup, on_delete=models.CASCADE,
        null=False, blank=False, verbose_name='process group',
        related_name='processes')

    knowledge_area = models.ForeignKey(
        KnowledgeArea, on_delete=models.CASCADE,
        null=False, blank=False, verbose_name='knowledge area',
        related_name='processes')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order']
        verbose_name = 'Process'
        verbose_name_plural = 'Processes'
