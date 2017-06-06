from rest_framework.reverse import reverse

from teams.serializers import TeamMemberListSerializer


def test_serialize(serializer_context, team_member_factory):
    """
    Test serializing a team member.
    """
    member = team_member_factory()
    serializer = TeamMemberListSerializer(
        member,
        context=serializer_context)

    expected = {
        'name': member.user.get_short_name(),
        'url': reverse(
            'teams:member-detail',
            kwargs={'pk': member.pk},
            request=serializer_context['request']),
        'member_type_name': member.get_member_type_display(),
    }

    assert serializer.data == expected
