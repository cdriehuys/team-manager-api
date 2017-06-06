from django.contrib.auth.models import AnonymousUser

from rest_framework import status
from rest_framework.test import force_authenticate

from teams import models, serializers, views


team_invite_list_view = views.TeamInviteListView.as_view()


def test_create_invite(api_rf, team_member_factory):
    """
    Admins should be able to create invitations for other users.
    """
    admin = team_member_factory(is_admin=True)
    data = {
        'email': 'newuser@example.com',
        'invite_accept_url': 'http://example.com/invites',
        'signup_url': 'http://example.com/signup',
        'team': admin.team.pk,
    }

    request = api_rf.post('/', data)
    request.user = admin.user
    force_authenticate(request, user=admin.user)

    response = team_invite_list_view(request, pk=admin.team.pk)

    invite = models.TeamInvite.objects.get()
    serializer = serializers.TeamInviteSerializer(invite)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data == serializer.data


def test_create_invite_non_admin(api_rf, team_member_factory):
    """
    Non-admin members should not be able to invite other users.
    """
    member = team_member_factory()
    data = {
        'email': 'newuser@example.com',
        'invite_accept_url': 'http://example.com/invites',
        'signup_url': 'http://example.com/signup',
        'team': member.team.pk,
    }

    request = api_rf.post('/', data)
    request.user = member.user
    force_authenticate(request, user=member.user)

    response = team_invite_list_view(request, pk=member.team.pk)

    assert response.status_code == status.HTTP_403_FORBIDDEN


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


def test_list_invites_anonymous_user(api_rf, team_factory):
    """
    Anonymous users should not be able to access a team's pending
    invites.

    Regression test for #12
    """
    team = team_factory()

    request = api_rf.get('/')
    request.user = AnonymousUser()

    response = team_invite_list_view(request, pk=team.pk)

    assert response.status_code == status.HTTP_403_FORBIDDEN


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
