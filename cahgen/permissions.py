from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to access it.
    """

    def has_object_permission(self, request, view, obj):
        # TODO POST is allowed for any authorized user
        # All permissions are only allowed to the owner of the object
        return obj.owner == request.user
