from rest_framework import status
from rest_framework.test import force_authenticate

from teams import models, serializers, views


team_member_detail_view = views.TeamMemberDetailView.as_view()


def test_delete_as_admin(api_rf, team_member_factory):
    """
    Team admins should be able to remove other members.
    """
    admin = team_member_factory(is_admin=True)
    member = team_member_factory(team=admin.team)

    request = api_rf.delete('/')
    request.user = admin.user
    force_authenticate(request, user=admin.user)

    response = team_member_detail_view(request, pk=member.pk)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not models.TeamMember.objects.filter(pk=member.pk).exists()


def test_delete_as_other_member(api_rf, team_member_factory):
    """
    Team members who are not admins should not be able to remove other
    members.
    """
    member = team_member_factory()
    other_member = team_member_factory(team=member.team)

    request = api_rf.delete('/')
    request.suer = member.user
    force_authenticate(request, user=member.user)

    response = team_member_detail_view(request, pk=other_member.pk)

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_delete_as_self(api_rf, team_member_factory):
    """
    A user should be able to remove themself from a team.
    """
    member = team_member_factory()

    request = api_rf.delete('/')
    request.user = member.user
    force_authenticate(request, user=member.user)

    response = team_member_detail_view(request, pk=member.pk)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert models.TeamMember.objects.count() == 0


def test_get(api_rf, serializer_context, team_member_factory):
    """
    Sending a GET request to the view should return the team member's
    details.
    """
    member = team_member_factory()
    serializer = serializers.TeamMemberSerializer(
        member,
        context=serializer_context)

    request = api_rf.get('/')

    response = team_member_detail_view(request, pk=member.pk)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == serializer.data


def test_update_as_admin(api_rf, team_member_factory):
    """
    Admins should be able to update other members' information.
    """
    admin = team_member_factory(is_admin=True)
    member = team_member_factory(team=admin.team)

    data = {
        'pk': member.pk,
        'member_type': models.TeamMember.COACH,
    }

    request = api_rf.patch('/', data)
    request.user = admin.user
    force_authenticate(request, user=admin.user)

    response = team_member_detail_view(request, pk=member.pk)

    assert response.status_code == status.HTTP_200_OK, response.data

    member.refresh_from_db()

    assert member.member_type == data['member_type']


def test_update_as_other_member(api_rf, team_member_factory):
    """
    A non-admin member should not be able to update another member's
    informatin.
    """
    member = team_member_factory()
    other_member = team_member_factory(team=member.team)

    data = {
        'pk': other_member.pk,
        'member_type': models.TeamMember.COACH,
    }

    request = api_rf.patch('/', data)
    request.user = member.user
    force_authenticate(request, user=member.user)

    response = team_member_detail_view(request, pk=other_member.pk)

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_update_as_self(api_rf, team_member_factory):
    """
    Admins should be able to update other members' information.
    """
    member = team_member_factory()

    data = {
        'pk': member.pk,
        'member_type': models.TeamMember.COACH,
    }

    request = api_rf.patch('/', data)
    request.user = member.user
    force_authenticate(request, user=member.user)

    response = team_member_detail_view(request, pk=member.pk)

    assert response.status_code == status.HTTP_200_OK

    member.refresh_from_db()

    assert member.member_type == data['member_type']
