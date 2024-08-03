import logging
from django.utils import timezone
from .models import CustomUser, OTP
from rest_framework_simplejwt.tokens import RefreshToken
from decouple import config

# Set up the logger for this module
logger = logging.getLogger('app_logger')


def set_refresh_token_cookie(response, refresh):
    """
    Set the refresh token cookie with appropriate attributes.
    """
    logger.debug('Setting refresh token cookie')
    # max_age = 3600 * 24 * 14  # 2 weeks
    # Calculate max_age from the refresh token's lifetime (in seconds)
    max_age = int(refresh.lifetime.total_seconds())

    # Get DJANGO_DEBUG from .env file
    debug_mode = config("DJANGO_DEBUG", default=True, cast=bool)

    # If DJANGO_DEBUG is True, secure_cookie should be False and vice-versa
    secure_cookie = not debug_mode

    # Set samesite and domain attributes based on debug_mode
    samesite_attr = "Lax" if debug_mode else "Strict"
    domain_attr = (
        None if debug_mode else "127.0.0.1"
    )  # Set to None in debug mode to use default domain

    response.set_cookie(
        "refresh_token",
        str(refresh),
        max_age=max_age,
        secure=secure_cookie,
        httponly=True,
        samesite=samesite_attr,
        domain=domain_attr,  # Explicitly set the domain based on debug_mode
        path="/",  # Make it available for all paths
    )
    logger.info('Refresh token cookie set successfully')
    return response


def get_valid_user(email):
    """
    Retrieve a valid user based on email.
    """
    logger.debug(f'Retrieving user with email: {email}')
    user = CustomUser.objects.filter(email=email).first()
    if not user:
        logger.error(f'Invalid email: {email}')
        raise ValueError("Invalid email")
    logger.info(f'User retrieved: {user.id}')
    return user


def validate_otp(user, otp_code):
    """
    Validate the provided OTP code for the user.
    """
    logger.debug(f'Validating OTP for user {user.id}')
    otp = user.otps.filter(otp=otp_code, is_used=False).first()
    if not otp or not otp.is_valid():
        logger.warning(f'Invalid or expired OTP for user {user.id}')
        raise ValueError("Invalid or expired OTP")
    otp.is_used = True
    otp.save()
    logger.info(f'OTP validated and marked as used for user {user.id}')


def activate_user(user):
    """
    Activate the user account.
    """
    logger.debug(f'Activating user {user.id}')
    user.is_active = True
    user.save()
    logger.info(f'User {user.id} activated')


def generate_jwt_tokens(user):
    """
    Generate JWT access and refresh tokens for the user.
    """
    logger.debug(f'Generating JWT tokens for user {user.id}')
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    logger.info(f'JWT tokens generated for user {user.id}')
    return access_token, refresh


def set_jwt_cookie(response, refresh):
    """
    Set the JWT refresh token cookie.
    """
    logger.debug('Setting JWT refresh token cookie')
    return set_refresh_token_cookie(response, refresh)


# authentication/utils.py
