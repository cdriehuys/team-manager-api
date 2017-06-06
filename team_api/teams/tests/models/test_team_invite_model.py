from teams import models


def test_create(team_factory):
    """
    Test creating a new team invitation.
    """
    models.TeamInvite.objects.create(
        email='test@example.com',
        team=team_factory())
