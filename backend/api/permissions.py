from rest_framework import permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class OwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
                request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
            )

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class CustomPermissions(permissions.BasePermission):
    def get_permissions(self):
        if self.action == 'put' or self.action == 'delete':
            permission_classes = [OwnerOrReadOnly]
        else:
            permission_classes = [IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]
