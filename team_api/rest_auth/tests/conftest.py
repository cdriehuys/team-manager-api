import pytest

from rest_framework.test import APIRequestFactory

from rest_auth import factories


@pytest.fixture(scope='session')
def api_rf():
    """
    Return an instance of ``rest_framework.test.APIRequestFactory``.

    Returns:
        An instance of ``rest_framework.test.APIRequestFactory``.
    """
    return APIRequestFactory()


@pytest.fixture
def token_factory(db):
    """
    Return the factory used to create tokens.

    Returns:
        ``rest_auth.factories.TokenFactory``
    """
    return factories.TokenFactory


@pytest.fixture
def user_factory(db):
    """
    Return the factory used to create users.

    Returns:
        ``rest_auth.factories.UserFactory``
    """
    return factories.UserFactory
