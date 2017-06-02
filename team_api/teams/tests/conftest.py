import pytest

from teams import factories


@pytest.fixture
def team_factory(db):
    """
    Get the factory used for creating teams.

    Returns:
        ``teams.factories.TeamFactory``
    """
    return factories.TeamFactory
