import pytest

from teams import models
from teams.serializers import TeamSerializer


@pytest.mark.django_db
def test_create():
    """
    Saving a team serializer with valid data should create a new team.
    """
    data = {
        'name': 'Test Team',
    }

    serializer = TeamSerializer(data=data)
    assert serializer.is_valid()

    team = serializer.save()

    assert models.Team.objects.count() == 1
    assert team.name == data['name']


def test_serialize(team_factory):
    """
    Test serializing a team.
    """
    team = team_factory()
    serializer = TeamSerializer(team)

    expected = {
        'id': team.id,
        'name': team.name,
    }

    assert serializer.data == expected


def test_update(team_factory):
    """
    Passing data to a serializer already associated with an instance
    should allow that instance to be updated.
    """
    team = team_factory(name='Old Name')
    data = {'name': 'New Name'}

    serializer = TeamSerializer(team, data=data)
    assert serializer.is_valid()

    team = serializer.save()

    assert models.Team.objects.count() == 1
    assert team.name == data['name']
