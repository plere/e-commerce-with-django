from rest_framework import permissions

from shopping.models import Store


class IsOwnerStore(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user == obj.store:
            return True
        return False


class IsStore(permissions.BasePermission):
    def has_permission(self, request, view):
        return isinstance(request.user, Store)