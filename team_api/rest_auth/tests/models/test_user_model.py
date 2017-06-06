import pytest

from rest_auth.models import User


@pytest.mark.django_db
def test_create():
    """
    Test creating a new user.
    """
    user = User.objects.create(
        email='test@example.com',
        is_staff=True,
        is_superuser=True)
    user.set_password('foo')
    user.save()


def test_get_short_name(user_factory):
    """
    ``get_short_name`` should return the user's email.
    """
    user = user_factory()

    assert user.get_short_name() == user.email


def test_get_username(user_factory):
    """
    ``get_username`` should return the user's email.
    """
    user = user_factory()

    assert user.get_username() == user.email


def test_is_active_default(user_factory):
    """
    By default, users should be active.
    """
    user = user_factory()

    assert user.is_active
