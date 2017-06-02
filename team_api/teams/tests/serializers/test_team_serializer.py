import pytest

from rest_framework.reverse import reverse

from teams import models
from teams.serializers import TeamSerializer


@pytest.mark.django_db
def test_create(serializer_context, user_factory):
    """
    Saving a team serializer with valid data should create a new team.
    """
    user = user_factory()

    data = {
        'name': 'Test Team',
    }

    serializer = TeamSerializer(data=data, context=serializer_context)
    assert serializer.is_valid()

    team = serializer.save(user=user)

    assert models.Team.objects.count() == 1
    assert team.name == data['name']

    assert models.TeamMember.objects.count() == 1

    member = models.TeamMember.objects.get()

    assert member.is_admin
    assert member.team == team
    assert member.user == user


def test_serialize(serializer_context, team_factory):
    """
    Test serializing a team.
    """
    team = team_factory()
    serializer = TeamSerializer(team, context=serializer_context)

    expected = {
        'url': reverse(
            'teams:team-detail',
            kwargs={'pk': team.pk},
            request=serializer_context['request']),
        'name': team.name,
    }

    assert serializer.data == expected


def test_update(serializer_context, team_factory):
    """
    Passing data to a serializer already associated with an instance
    should allow that instance to be updated.
    """
    team = team_factory(name='Old Name')
    data = {'name': 'New Name'}

    serializer = TeamSerializer(team, data=data, context=serializer_context)
    assert serializer.is_valid()

    team = serializer.save()

    assert models.Team.objects.count() == 1
    assert team.name == data['name']
