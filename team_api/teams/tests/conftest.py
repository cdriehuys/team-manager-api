import pytest

from rest_framework.test import APIClient

from teams import factories


@pytest.fixture(scope='session')
def api_client():
    """
    Get an instance of DRF's ``APIClient``.

    Returns:
        An instance of ``rest_framework.test.APIClient``.
    """
    return APIClient()


@pytest.fixture
def team_factory(db):
    """
    Get the factory used for creating teams.

    Returns:
        ``teams.factories.TeamFactory``
    """
    return factories.TeamFactory
