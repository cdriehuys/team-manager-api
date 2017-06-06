import pytest

from rest_framework.test import APIClient, APIRequestFactory

from rest_auth.factories import UserFactory

from teams import factories


@pytest.fixture
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


@pytest.fixture
def team_invite_factory(db):
    """
    Get the factory used for creating team invites.

    Returns:
        ``teams.factories.TeamInviteFactory``
    """
    return factories.TeamInviteFactory


@pytest.fixture
def team_member_factory(db):
    """
    Get the factory used for creating team members.

    Returns:
        ``teams.factories.TeamMemberFactory``
    """
    return factories.TeamMemberFactory


@pytest.fixture
def user_factory(db):
    """
    Get the factory used for creating users.

    Returns:
        ``rest_auth.factories.UserFactory``
    """
    return UserFactory
