from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _


class UserManager(BaseUserManager):
    """
    Manager for the ``rest_auth.User`` model.
    """

    def create_superuser(self, email, password=None, **kwargs):
        """
        Create a new superuser.

        Superusers are granted access to the admin site by default and
        are automatically given all permissions.

        Args:
            email:
                The user's email address.
            password:
                The user's password.
            kwargs;
                Additional keyword arguments to pass to the user.

        Returns:
            A new instance of ``rest_auth.User`` with ``is_staff`` and
            ``is_superuser`` marked as ``True``.
        """
        user = self.create_user(email, password=password, **kwargs)
        user.is_staff = True
        user.is_superuser = True
        user.save()

        return user

    def create_user(self, email, password=None, **kwargs):
        """
        Create a new user.

        Args:
            email:
                The user's email address.
            password:
                The user's password.
            kwargs:
                Additional keyword arguments to pass to the user.

        Returns:
            A new instance of ``rest_auth.User`` with the given
            attributes.
        """
        if not email:
            raise ValidationError(_('Users must have an email address.'))

        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)

        return user
