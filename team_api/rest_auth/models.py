from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import ugettext_lazy as _


class User(PermissionsMixin, AbstractBaseUser):
    """
    Represents a single user.
    """
    email = models.EmailField(
        unique=True,
        verbose_name=_('Email'))
    is_staff = models.BooleanField(
        default=False,
        help_text=_('Staff users are allowed to login to the admin site.'),
        verbose_name=_('Is staff'))

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
