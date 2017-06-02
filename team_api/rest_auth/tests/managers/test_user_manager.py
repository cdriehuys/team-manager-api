from django.core.exceptions import ValidationError

import pytest

from rest_auth.models import User


@pytest.mark.django_db
def test_create_superuser():
    """
    Creating a superuser should do the same thing as ``create_user``
    except ``is_staff`` and ``is_superuser`` should automatically be set
    to ``True``.
    """
    user = User.objects.create_superuser('test@example.com', password='foo')

    assert user.email == 'test@example.com'
    assert user.check_password('foo')
    assert user.is_staff
    assert user.is_superuser


@pytest.mark.django_db
def test_create_user():
    """
    Creating a user should do the same thing as ``create``, but it
    should set the user's password correctly.
    """
    user = User.objects.create_user('test@example.com', password='foo')

    assert user.email == 'test@example.com'
    assert user.check_password('foo')


def test_create_user_no_email():
    """
    If no email is passed to ``create_user``, a ``ValidationError``
    should be raised.
    """
    with pytest.raises(ValidationError):
        User.objects.create_user(email='', password='foo')
