from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'project_dashboard.users'
    label = 'users'
    verbose_name = "Users"

    def ready(self):
        """Override this to put in:
            Users system checks
            Users signal registration
        """
        try:
            import users.signals  # noqa F401
        except ImportError:
            pass
