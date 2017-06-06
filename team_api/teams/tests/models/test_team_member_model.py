from django.db.utils import IntegrityError

import pytest

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


def test_unique_team_and_user(team_member_factory):
    """
    Team members should be unique with respect to user and team.

    Regression test for #14
    """
    member = team_member_factory()

    with pytest.raises(IntegrityError):
        team_member_factory(team=member.team, user=member.user)
