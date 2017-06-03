from rest_framework import permissions


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
