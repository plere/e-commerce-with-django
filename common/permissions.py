from rest_framework import permissions

from common.models import User


class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return isinstance(request.user, User)
