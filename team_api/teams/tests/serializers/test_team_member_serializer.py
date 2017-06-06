from rest_framework.reverse import reverse

from teams import serializers


def test_serialize(serializer_context, team_member_factory):
    """
    Test serializing a team member.
    """
    member = team_member_factory()
    serializer = serializers.TeamMemberSerializer(
        member,
        context=serializer_context)

    expected = {
        'name': member.user.get_short_name(),
        'team': member.team.pk,
        'team_url': reverse(
            'teams:team-detail',
            kwargs={'pk': member.team.pk},
            request=serializer_context['request']),
        'member_type': member.member_type,
        'member_type_name': member.get_member_type_display(),
        'is_admin': member.is_admin,
    }

    assert serializer.data == expected


def test_update(serializer_context, team_factory, team_member_factory):
    """
    Passing data to a serializer associated with a team member should
    allow for updating that team member's informatin.
    """
    member = team_member_factory()
    team = team_factory()

    data = {
        'pk': member.pk,
        'team': team.pk,
    }

    serializer = serializers.TeamMemberSerializer(
        member,
        context=serializer_context,
        data=data)
    assert serializer.is_valid(), serializer.errors
