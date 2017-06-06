from django.utils.translation import ugettext as _

from rest_framework import generics, status, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from teams import models, permissions, serializers


class TeamInviteListView(generics.ListCreateAPIView):
    """
    List and create team invites.
    """
    serializer_class = serializers.TeamInviteSerializer

    def check_permissions(self, request):
        """
        Get a list of serialized invitations for the given team.

        Args:
            request:
                The request being made.

        Raises:
            PermissionDenied:
                If the user making the request is not an admin for the
                current team.
        """
        super().check_permissions(request)

        if not models.TeamMember.objects.filter(
                is_admin=True,
                team__pk=self.kwargs.get('pk'),
                user=request.user).exists():
            raise PermissionDenied(
                code='admin_required',
                detail=_('This view may only be accessed by team admins.'))

    def get_queryset(self):
        """
        Get a list of team invitations to operate on.

        Returns:
            A queryset containing the invitations belonging to the team
            with the primary key given in the URL.
        """
        return models.TeamInvite.objects.filter(team__pk=self.kwargs.get('pk'))

    def perform_create(self, serializer):
        """
        Create a new team invite.

        We override the creation of the invite so that we can associate
        it with the current team.

        Args:
            serializer:
                An instance of ``TeamInvite.serializer_class`` that has
                been populated with data.

        Returns:
            The created invite.
        """
        pk = self.kwargs.get('pk')
        team = models.Team.objects.get(pk=pk)

        return serializer.save(team=team)


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

        For invites, the ``TeamInviteSerializer`` class should be used.

        If we are listing teams, the ``TeamListSerializer`` class should
        be used. Otherwise we should use the ``TeamSerializer`` class.

        Returns:
            The serializer class to be used for the response.
        """
        if self.action == 'list':
            return serializers.TeamListSerializer

        return serializers.TeamSerializer


class TeamMemberDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View or update a team member's information.
    """
    permission_classes = (permissions.TeamMemberPermission,)
    queryset = models.TeamMember.objects.all()
    serializer_class = serializers.TeamMemberSerializer
