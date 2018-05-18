""" Core or common features used by multiple apps within the project """
from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'project_dashboard.core'
    label = 'core'
