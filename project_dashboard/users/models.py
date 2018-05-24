import uuid

from django.contrib.auth.models import UserManager, AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from ..core.utils.files import get_file_path
from ..core.utils.tokens import get_token_for_user


# Models defined here
def get_user_file_path(instance, filename):
    return get_file_path(instance, filename, "user")


class PermissionsMixin(models.Model):
    """
    A mixin class that adds the fields and methods necessary to support
    Django"s Permission model using the ModelBackend.
    """
    is_superuser = models.BooleanField(
        _("superuser status"), default=False,
        help_text=_("Designates that this user has all permissions without "
                    "explicitly assigning them."))

    class Meta:
        abstract = True

    def has_perm(self, perm, obj=None):
        """ Returns True if the user is superadmin and is active """
        return self.is_active and self.is_superuser

    def has_perms(self, perm_list, obj=None):
        """ Returns True if the user is superadmin and is active """
        return self.is_active and self.is_superuser

    def has_module_perms(self, app_label):
        """ Returns True if the user is superadmin and is active """
        return self.is_active and self.is_superuser

    @property
    def is_staff(self):
        return self.is_superuser


def get_default_uuid():
    return uuid.uuid4().hex


class User(AbstractUser):
    """ Extends User model, related to :model: 'auth.User' """
    bio = models.TextField(
        null=False, blank=True, default="", verbose_name=_("biography"))
    photo = models.FileField(
        upload_to=get_user_file_path,
        max_length=500, null=True, blank=True,
        verbose_name=_("photo"))
    date_joined = models.DateTimeField(
        _("date joined"), default=timezone.now)
    lang = models.CharField(
        max_length=20, null=True, blank=True, default="",
        verbose_name=_("default language"))
    timezone = models.CharField(
        max_length=20, null=True, blank=True, default="",
        verbose_name=_("default timezone"))

    is_system = models.BooleanField(
        null=False, blank=False, default=False)

    objects = UserManager()

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
        ordering = ["username"]

    def __str__(self):
        # return self.username
        return '%s %s' % (self.first_name, self.last_name)

    @property
    def full_name(self):
        """ Returns the person's full name. """
        return '%s %s' % (self.first_name, self.last_name)

    def save(self, *args, **kwargs):
        get_token_for_user(self, "cancel_account")
        super().save(*args, **kwargs)
