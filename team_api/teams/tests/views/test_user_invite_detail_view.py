from django.contrib.auth.models import AnonymousUser

from rest_framework import status
from rest_framework.test import force_authenticate

from teams import models, views


user_invite_detail_view = views.UserInviteDetailView.as_view()


def test_accept(api_rf, team_invite_factory, user_factory):
    """
    Sending a ``POST`` request to the view should accept the invitation.
    """
    user = user_factory()
    invite = team_invite_factory(email=user.email)

    request = api_rf.post('/')
    request.user = user
    force_authenticate(request, user=user)

    response = user_invite_detail_view(request, pk=invite.pk)

    assert response.status_code == status.HTTP_200_OK
    assert models.TeamMember.objects.count() == 1


def test_accept_as_anonymous(api_rf, team_invite_factory):
    """
    Anonymous users should not be allowed to access the view.
    """
    invite = team_invite_factory()

    request = api_rf.post('/')
    request.user = AnonymousUser()

    response = user_invite_detail_view(request, pk=invite.pk)

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_delete(api_rf, team_invite_factory, user_factory):
    """
    User should be able to decline an invitation by sending a ``DELETE``
    request to the view.
    """
    user = user_factory()
    invite = team_invite_factory(email=user.email)

    request = api_rf.delete('/')
    request.user = user
    force_authenticate(request, user=user)

    response = user_invite_detail_view(request, pk=invite.pk)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert models.TeamInvite.objects.count() == 0


def test_delete_other_member_invite(api_rf, team_invite_factory, user_factory):
    """
    Users should not be able to delete invitations for other users.
    """
    user = user_factory(email='test@example.com')
    invite = team_invite_factory(email='other@example.com')

    request = api_rf.delete('/')
    request.user = user
    force_authenticate(request, user=user)

    response = user_invite_detail_view(request, pk=invite.pk)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert models.TeamInvite.objects.count() == 1
