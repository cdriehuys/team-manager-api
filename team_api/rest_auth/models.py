from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import ugettext_lazy as _

from rest_auth import managers


class User(PermissionsMixin, AbstractBaseUser):
    """
    Represents a single user.

    This differs from Django's default user model in that ``email`` is
    the identifying field, and a username is not required.
    """
    email = models.EmailField(
        unique=True,
        verbose_name=_('Email'))
    is_staff = models.BooleanField(
        default=False,
        help_text=_('Staff users are allowed to login to the admin site.'),
        verbose_name=_('Is staff'))

    # Tell Django which fields are special
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'

    # Use custom manager
    objects = managers.UserManager()
