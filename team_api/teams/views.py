from rest_framework import viewsets

from teams import models, serializers


class TeamListViewSet(viewsets.ModelViewSet):
    """
    list:
    List all teams.

    create:
    Create a new team.

    read:
    Retrieve a team's details.

    update:
    Update a team's information.

    partial_update:
    Update part of a team's information.

    delete:
    Delete a team.
    """
    queryset = models.Team.objects.all()
    serializer_class = serializers.TeamSerializer
