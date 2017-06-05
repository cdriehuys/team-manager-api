from rest_framework import status, viewsets
from rest_framework.response import Response

from teams import models, permissions, serializers


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
    permission_classes = (permissions.TeamPermission,)
    queryset = models.Team.objects.all()

    def create(self, request):
        """
        Create a new team.

        Args:
            request:
                The request containing the team's information.

        Returns:
            The serialized version of the created team.
        """
        serializer = self.get_serializer(data=request.POST)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_serializer_class(self):
        """
        Get the appropriate serializer for the action being performed.

        If we are listing teams, the ``TeamListSerializer`` class should
        be used. Otherwise we should use the ``TeamSerializer`` class.

        Returns:
            The serializer class to be used for the response.
        """
        if self.action == 'list':
            return serializers.TeamListSerializer

        return serializers.TeamSerializer
