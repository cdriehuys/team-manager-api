from django.contrib.auth.models import AnonymousUser

from rest_framework import status
from rest_framework.test import force_authenticate

from teams import models, serializers, views


user_invite_list_view = views.UserInviteListView.as_view()


def test_list_invites(api_rf, team_invite_factory, user_factory):
    """
    Sending a GET request to the view should return a serialized list of
    the user's invites.
    """
    user = user_factory()

    team_invite_factory(email=user.email)
    team_invite_factory(email=user.email)
    team_invite_factory(email='other@example.com')

    serializer = serializers.TeamInviteSerializer(
        models.TeamInvite.objects.filter(email=user.email),
        many=True)

    request = api_rf.get('/')
    request.user = user
    force_authenticate(request, user=user)

    response = user_invite_list_view(request)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == serializer.data


def test_list_invites_anonymous(api_rf):
    """
    Anonymous users should not be able to access this view.
    """
    request = api_rf.get('/')
    request.user = AnonymousUser()

    response = user_invite_list_view(request)

    assert response.status_code == status.HTTP_403_FORBIDDEN
