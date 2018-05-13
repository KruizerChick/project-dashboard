from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    """ Extends User model, related to :model: 'auth.User' """
    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_('Name of User'),
        blank=True, max_length=255,
        help_text='If different from First Name + Last Name')

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        """ Redirects to User detail page """
        return reverse('users:detail', kwargs={'username': self.username})
