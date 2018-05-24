from django.db import models
from django.utils.translation import ugettext_lazy as _


# Create your models here.
class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides selfupdating
    "created" and "modified" fields.
    """
    created = models.DateTimeField(
        auto_now_add=True, verbose_name=_('created'))
    modified = models.DateTimeField(
        auto_now=True, verbose_name=_('modified'))

    class Meta:
        abstract = True
