from rest_framework import status
from rest_framework.test import force_authenticate

from teams import serializers, views


team_invite_list_view = views.TeamInviteListView.as_view()


def test_list_invites(api_rf, team_invite_factory, team_member_factory):
    """
    Sending a GET request should return a list of pending invites for
    that team.
    """
    admin = team_member_factory(is_admin=True)

    team_invite_factory(team=admin.team)
    team_invite_factory(team=admin.team)

    serializer = serializers.TeamInviteSerializer(
        admin.team.teaminvite_set.all(),
        many=True)

    request = api_rf.get('/')
    request.user = admin.user
    force_authenticate(request, user=admin.user)

    response = team_invite_list_view(request, pk=admin.team.pk)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == serializer.data


def test_list_invites_non_admin(
        api_rf,
        team_invite_factory,
        team_member_factory):
    """
    Non admin users should not be able to view a team's invites.
    """
    member = team_member_factory()

    request = api_rf.get('/')
    request.user = member.user
    force_authenticate(request, user=member.user)

    response = team_invite_list_view(request, pk=member.team.pk)

    assert response.status_code == status.HTTP_403_FORBIDDEN
