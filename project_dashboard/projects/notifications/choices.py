# -*- coding: utf-8 -*-
import enum
from django.utils.translation import ugettext_lazy as _


class NotifyLevel(enum.IntEnum):
    involved = 1
    all = 2
    none = 3


NOTIFY_LEVEL_CHOICES = (
    (NotifyLevel.involved, _("Involved")),
    (NotifyLevel.all, _("All")),
    (NotifyLevel.none, _("None")),
)
