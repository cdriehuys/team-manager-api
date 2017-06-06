import pytest

from rest_framework.reverse import reverse

from teams import models, serializers


@pytest.mark.django_db
def test_create(serializer_context, user_factory):
    """
    Saving a team serializer with valid data should create a new team.
    """
    user = user_factory()

    data = {
        'name': 'Test Team',
    }

    serializer = serializers.TeamSerializer(
        data=data,
        context=serializer_context)
    assert serializer.is_valid()

    team = serializer.save(user=user)

    assert models.Team.objects.count() == 1
    assert team.name == data['name']

    assert models.TeamMember.objects.count() == 1

    member = models.TeamMember.objects.get()

    assert member.is_admin
    assert member.team == team
    assert member.user == user


def test_serialize(serializer_context, team_factory, team_member_factory):
    """
    Test serializing a team.
    """
    team = team_factory()

    team_member_factory(team=team)
    team_member_factory(team=team)

    member_serializer = serializers.TeamMemberListSerializer(
        team.members.all(),
        context=serializer_context,
        many=True)

    serializer = serializers.TeamSerializer(team, context=serializer_context)

    expected = {
        'name': team.name,
        'invites': reverse(
            'teams:team-invites',
            kwargs={'pk': team.pk},
            request=serializer_context['request']),
        'members': member_serializer.data,
    }

    assert serializer.data == expected


def test_update(serializer_context, team_factory):
    """
    Passing data to a serializer already associated with an instance
    should allow that instance to be updated.
    """
    team = team_factory(name='Old Name')
    data = {'name': 'New Name'}

    serializer = serializers.TeamSerializer(
        team,
        data=data,
        context=serializer_context)
    assert serializer.is_valid()

    team = serializer.save()

    assert models.Team.objects.count() == 1
    assert team.name == data['name']
