from rest_framework import permissions

from base_auth.constants import ADMIN, FACULTY, STUDENT


class StacPermission(permissions.BasePermission):
    """
    Permission to restrict access to views based on user role
    """

    def has_permission(self, request, view):
        user = request.user
        role = user.get_role()
        allowed_roles = [ADMIN, FACULTY, STUDENT]

        if role not in allowed_roles:
            return False

        if view.action in ['list', 'retrieve']:
            return True

        elif view.action in ['create', 'retrieve', 'partial_update']:
            return role == STUDENT

        return False


class IsAdminOrIsFaculty(permissions.BasePermission):
    """
    Permission to restrict access to users with Admin or Faculty role only
    """

    def has_permission(self, request, view):
        user = request.user
        role = user.get_role()
        allowed_roles = [ADMIN, FACULTY]

        if role in allowed_roles:
            return True

        return False
