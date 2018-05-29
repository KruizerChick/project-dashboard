""" Settings of Projects """

from django.conf import settings

SEARCH_FIELDS = getattr(
    settings, 'PROJECTS_SEARCH_FIELDS',
    ['name', 'description', 'categories', ])
