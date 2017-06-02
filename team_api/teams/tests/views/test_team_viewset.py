import pytest

from rest_framework import status
from rest_framework.reverse import reverse

from teams import models, serializers


@pytest.mark.django_db
def test_create_team(api_client, user_factory):
    """
    Submitting a valid POST request to the view should create a new
    team.
    """
    user = user_factory()
    api_client.force_authenticate(user=user)

    data = {
        'name': 'Test Team',
    }

    url = reverse('teams:team-list')
    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_201_CREATED

    team = models.Team.objects.get()

    assert team.name == data['name']


def test_delete(api_client, team_factory):
    """
    Submitting a DELETE request to a team's detail view should delete
    the team.
    """
    team = team_factory()

    url = reverse('teams:team-detail', kwargs={'pk': team.pk})
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.data is None

    assert models.Team.objects.count() == 0


def test_list_teams(api_client, serializer_context, team_factory):
    """
    The team list should return a list of serialized teams.
    """
    team_factory(name='Team 1')
    team_factory(name='Team 2')
    team_factory(name='Team 3')

    serializer = serializers.TeamSerializer(
        models.Team.objects.all(),
        context=serializer_context,
        many=True)

    url = reverse('teams:team-list')
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == serializer.data
