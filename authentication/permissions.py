import logging
from rest_framework import permissions

# Set up the logger for this module
logger = logging.getLogger('app_logger')


class IsActiveUser(permissions.BasePermission):
    """
    Custom permission to only allow access to active users.
    """
    message = "User is not active."

    def has_permission(self, request, view):
        if request.user and request.user.is_active:
            logger.debug(
                f"Permission granted: User {request.user.id} is active.")
            return True
        else:
            logger.warning(
                f"Permission denied: User {request.user.id} is not active.")
            return False


class IsStaffUser(permissions.BasePermission):
    """
    Custom permission to only allow access to staff users.
    """
    message = "User is not a staff member."

    def has_permission(self, request, view):
        if request.user and request.user.is_staff:
            logger.debug(
                f"Permission granted: User {request.user.id} is a staff member.")
            return True
        else:
            logger.warning(
                f"Permission denied: User {request.user.id} is not a staff member.")
            return False


class HasCompletedSetup(permissions.BasePermission):
    """
    Custom permission to only allow access to users who have completed their setup.
    """
    message = "User have not completed their account setup."

    def has_permission(self, request, view):
        if request.user and request.user.has_completed_setup:
            logger.debug(
                f"Permission granted: User {request.user.id} have completed setup.")
            return True
        else:
            logger.warning(
                f"Permission denied: User {request.user.id} have not completed setup.")
            return False


class HasRoleReader(permissions.BasePermission):
    """
    Custom permission to only allow access to users with the 'reader' role.
    """
    message = "User does not have the 'reader' role."

    def has_permission(self, request, view):
        if request.user and 'reader' in request.user.roles:
            logger.debug(
                f"Permission granted: User {request.user.id} has 'reader' role.")
            return True
        else:
            logger.warning(
                f"Permission denied: User {request.user.id} does not have 'reader' role.")
            return False


class HasRoleWriter(permissions.BasePermission):
    """
    Custom permission to only allow access to users with the 'writer' role.
    """
    message = "User does not have the 'writer' role."

    def has_permission(self, request, view):
        if request.user and 'writer' in request.user.roles:
            logger.debug(
                f"Permission granted: User {request.user.id} has 'writer' role.")
            return True
        else:
            logger.warning(
                f"Permission denied: User {request.user.id} does not have 'writer' role.")
            return False


class HasRoleEditor(permissions.BasePermission):
    """
    Custom permission to only allow access to users with the 'editor' role.
    """
    message = "User does not have the 'editor' role."

    def has_permission(self, request, view):
        if request.user and 'editor' in request.user.roles:
            logger.debug(
                f"Permission granted: User {request.user.id} has 'editor' role.")
            return True
        else:
            logger.warning(
                f"Permission denied: User {request.user.id} does not have 'editor' role.")
            return False


class HasRoleReviewer(permissions.BasePermission):
    """
    Custom permission to only allow access to users with the 'reviewer' role.
    """
    message = "User does not have the 'reviewer' role."

    def has_permission(self, request, view):
        if request.user and 'reviewer' in request.user.roles:
            logger.debug(
                f"Permission granted: User {request.user.id} has 'reviewer' role.")
            return True
        else:
            logger.warning(
                f"Permission denied: User {request.user.id} does not have 'reviewer' role.")
            return False


class HasRolePublisher(permissions.BasePermission):
    """
    Custom permission to only allow access to users with the 'publisher' role.
    """
    message = "User does not have the 'publisher' role."

    def has_permission(self, request, view):
        if request.user and 'publisher' in request.user.roles:
            logger.debug(
                f"Permission granted: User {request.user.id} has 'publisher' role.")
            return True
        else:
            logger.warning(
                f"Permission denied: User {request.user.id} does not have 'publisher' role.")
            return False

# To be used as
# from rest_framework.permissions import IsAuthenticated
# from .permissions import IsActiveUser, IsStaffUser, HasRoleReader

# class SomeView(APIView):
#     permission_classes = [IsAuthenticated, IsActiveUser, HasRoleReader]


# authentication/permissions.py
