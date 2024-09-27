from rest_framework import permissions
from rest_framework.exceptions import AuthenticationFailed
from utils.error_codes import ErrorCode


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the object
        return obj.user == request.user


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Object-level permission to only allow owners of an object to edit it
        return obj.user == request.user


class CustomIsAuthenticated(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        header = request.META.get("HTTP_AUTHORIZATION")

        if not header:
            raise AuthenticationFailed(
                {
                    "code": ErrorCode.AUTH_CREDENTIAL_NOT_PROVIDED,
                    "detail": "Authentication credentials were not provided.",
                }
            )

        return super().has_permission(request, view)

# utils/permissions.py
