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
        'team': reverse(
            'teams:team-detail',
            kwargs={'pk': member.team.pk},
            request=serializer_context['request']),
        'member_type': member.member_type,
        'member_type_name': member.get_member_type_display(),
        'is_admin': member.is_admin,
    }

    assert serializer.data == expected
