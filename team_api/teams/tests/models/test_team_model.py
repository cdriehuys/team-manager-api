import pytest

from teams.models import Team


@pytest.mark.django_db
def test_create():
    """
    Test creating a team.
    """
    Team.objects.create(name='Test Team')


def test_string_conversion(team_factory):
    """
    Converting a team to a string should return the team's name.
    """
    team = team_factory()

    assert str(team) == team.name
