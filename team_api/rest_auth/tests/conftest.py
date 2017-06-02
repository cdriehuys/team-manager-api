import pytest

from rest_auth import factories


@pytest.fixture
def user_factory(db):
    """
    Return the factory used to create users.

    Returns:
        ``rest_auth.factories.UserFactory``
    """
    return factories.UserFactory
