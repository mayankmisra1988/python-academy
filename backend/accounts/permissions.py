from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
    Allows users to access only their own data.
    """

    def has_object_permission(self, request, view, obj):
        return obj == request.user