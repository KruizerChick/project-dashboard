""" Managers for Projects app """
from django.db import models
# from django.utils import timezone

# from .settings import SEARCH_FIELDS


# Project managers
def projects_open(queryset):
    """ Return only open projects """
    return queryset.filter(is_closed=False)


class ProjectOpenManager(models.Manager):
    """ Manager to retrieve open projects. """

    def get_queryset(self):
        """ Return open projects. """
        return projects_open(
            super(ProjectOpenManager, self).get_queryset())

    # def basic_search(self, pattern):
    #     """ Basic search on projects. """
    #     lookup = None
    #     for pattern in pattern.split():
    #         query_part = models.Q()
    #         for field in SEARCH_FIELDS:
    #             query_part |= models.Q(**{'%s__icontains' % field: pattern})
    #         if lookup is None:
    #             lookup = query_part
    #         else:
    #             lookup |= query_part

    #     return self.get_queryset().filter(lookup)


class ProjectRelatedOpenManager(models.Manager):
    """ Manager to retrieve objects associated with open projects. """

    def get_queryset(self):
        """ Return a queryset containing open projects. """
        # now = timezone.now()
        return super(
            ProjectRelatedOpenManager, self).get_queryset().filter(
            projects__is_closed=False).distinct()
