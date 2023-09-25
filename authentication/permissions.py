from rest_framework import permissions

class IsActiveUser(permissions.BasePermission):
    """
    Custom permission to only allow access to active users.
    """
    message = "User is not active."

    def has_permission(self, request, view):
        return request.user and request.user.is_active

class IsStaffUser(permissions.BasePermission):
    """
    Custom permission to only allow access to staff users.
    """
    message = "User is not a staff member."

    def has_permission(self, request, view):
        return request.user and request.user.is_staff

class HasCompletedSetup(permissions.BasePermission):
    """
    Custom permission to only allow access to users who have completed their setup.
    """
    message = "User has not completed their account setup."

    def has_permission(self, request, view):
        return request.user and request.user.has_completed_setup

class HasRoleReader(permissions.BasePermission):
    """
    Custom permission to only allow access to users with the 'reader' role.
    """
    message = "User does not have the 'reader' role."

    def has_permission(self, request, view):
        return request.user and 'reader' in request.user.roles

class HasRoleWriter(permissions.BasePermission):
    """
    Custom permission to only allow access to users with the 'writer' role.
    """
    message = "User does not have the 'writer' role."

    def has_permission(self, request, view):
        return request.user and 'writer' in request.user.roles

class HasRoleEditor(permissions.BasePermission):
    """
    Custom permission to only allow access to users with the 'editor' role.
    """
    message = "User does not have the 'editor' role."

    def has_permission(self, request, view):
        return request.user and 'editor' in request.user.roles

class HasRoleReviewer(permissions.BasePermission):
    """
    Custom permission to only allow access to users with the 'reviewer' role.
    """
    message = "User does not have the 'reviewer' role."

    def has_permission(self, request, view):
        return request.user and 'reviewer' in request.user.roles

class HasRolePublisher(permissions.BasePermission):
    """
    Custom permission to only allow access to users with the 'publisher' role.
    """
    message = "User does not have the 'publisher' role."

    def has_permission(self, request, view):
        return request.user and 'publisher' in request.user.roles

# To be used as
# from rest_framework.permissions import IsAuthenticated
# from .permissions import IsActiveUser, IsStaffUser, HasRoleReader

# class SomeView(APIView):
#     permission_classes = [IsAuthenticated, IsActiveUser, HasRoleReader]
    

# authentication/permissions.py