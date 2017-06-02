import pytest

from rest_framework.test import APIClient, APIRequestFactory

from teams import factories


@pytest.fixture(scope='session')
def api_client():
    """
    Get an instance of DRF's ``APIClient``.

    Returns:
        An instance of ``rest_framework.test.APIClient``.
    """
    return APIClient()


@pytest.fixture(scope='session')
def api_rf():
    """
    Get an instance of DRF's ``APIRequestFactory``.

    Returns:
        An instance of ``rest_framework.test.APIRequestFactory``.
    """
    return APIRequestFactory()


@pytest.fixture(scope='session')
def serializer_context(api_rf):
    """
    Dummy context for serializers that require request context.

    Returns:
        A dictionary containing dummy context for use in a serializer.
    """
    return {
        'request': api_rf.get('/'),
    }


@pytest.fixture
def team_factory(db):
    """
    Get the factory used for creating teams.

    Returns:
        ``teams.factories.TeamFactory``
    """
    return factories.TeamFactory
