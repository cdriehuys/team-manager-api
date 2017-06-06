from rest_framework import permissions


class TeamMemberPermission(permissions.IsAuthenticatedOrReadOnly):
    """
    Permission for allowing access to ``TeamMember`` instances.

    Read operations (``GET``, ``HEAD``, or ``OPTIONS``) are allowed by
    anyone, but write operations (``PATCH`` or ``PUT``) are only allowed
    for team admins and the team member themself.
    """

    def has_object_permission(self, request, view, team_member):
        """
        Determine if the current user has permission to perform the
        requested action for the given team member.

        Args:
            request:
                The request to check permissions for.
            view:
                The view being accessed.
            team_member:
                The team member that is being acted upon.

        Returns:
            If the request method is a read operation, we return
            ``True``. If the user making the request is an admin of the
            team member's team, or the requesting user is the team
            member themself then we also return ``True``. If neither of
            those checks succeeds, ``False`` is returned.
        """
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user == team_member.user:
            return True

        return team_member.team.members.filter(
            is_admin=True,
            user=request.user).exists()


class TeamPermission(permissions.BasePermission):
    """
    Permission for allowing access to ``Team`` instances.

    Read operations (``GET``, ``HEAD``, ``OPTIONS``) are always
    permitted. Users are allowed to create a team (``POST``) as long as
    they are authenticated. Updates (``PATCH``, ``PUT``) are only
    permitted from admin users.
    """

    def has_object_permission(self, request, view, team):
        """
        Determine if the current user has permission to access the view.

        This check specifically applies to detail views.

        Args:
            request:
                The request to check permissions for.
            view:
                The view being accessed.
            team:
                The team being retrieved.

        Returns:
            ``True`` if the method is in ``permissions.SAFE_METHODS`` or
            the user is an admin for the current team. ``False``
            otherwise.
        """
        if request.method in permissions.SAFE_METHODS:
            return True

        # Any other actions require the current user to be an admin for
        # the team being checked.
        return team.members.filter(is_admin=True, user=request.user).exists()

    def has_permission(self, request, view):
        """
        Determine if the user has permission to access the view.

        Args:
            request:
                The request to check permissions for.
            view:
                The view being accessed.

        Returns:
            ``True`` if the operation is in ``permissions.SAFE_METHODS``
            or the user is authenticated. Otherwise ``False`` is
            returned.
        """
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_authenticated()
