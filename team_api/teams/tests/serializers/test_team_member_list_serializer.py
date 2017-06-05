from teams.serializers import TeamMemberListSerializer


def test_serialize(team_member_factory):
    """
    Test serializing a team member.
    """
    member = team_member_factory()
    serializer = TeamMemberListSerializer(member)

    expected = {
        'name': member.user.get_short_name(),
        'member_type_name': member.get_member_type_display(),
    }

    assert serializer.data == expected
