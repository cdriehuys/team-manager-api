from teams.models import TeamMember


def test_create(team_factory, user_factory):
    """
    Test creating a team member.
    """
    TeamMember.objects.create(
        is_admin=True,
        member_type=TeamMember.PLAYER,
        team=team_factory(),
        user=user_factory())
