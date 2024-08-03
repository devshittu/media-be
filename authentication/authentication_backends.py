import logging
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

# Set up the logger for this module
logger = logging.getLogger('app_logger')


class EmailOrUsernameModelBackend(ModelBackend):
    """
    Custom authentication backend that allows users to log in using either
    their email or username.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        logger.debug('Authenticating user with username/email: %s', username)
        UserModel = get_user_model()
        try:
            # Check if the provided identifier matches either an
            # email or a username in the database
            user = UserModel.objects.get(
                Q(email=username) | Q(username=username))
            logger.info('User found for username/email: %s', username)

        except UserModel.DoesNotExist:
            logger.warning(
                'User does not exist for username/email: %s', username)
            return None

        # If a user was found and the password is correct, return the user
        if user.check_password(password):
            logger.info('Password correct for user: %s', username)
            return user

        logger.warning('Password incorrect for user: %s', username)
        return None

# authentication/authentication_backends.py
