from rest_framework import status
from rest_framework.test import force_authenticate

from teams import models, views


user_invite_detail_view = views.UserInviteDetailView.as_view()


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
