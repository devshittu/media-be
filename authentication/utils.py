from django.utils import timezone
from .models import CustomUser, OTP
from rest_framework_simplejwt.tokens import RefreshToken
from decouple import config


def set_refresh_token_cookie(response, refresh):
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
    return response


def get_valid_user(email):
    user = CustomUser.objects.filter(email=email).first()
    if not user:
        raise ValueError("Invalid email")
    return user


def validate_otp(user, otp_code):
    otp = user.otps.filter(otp=otp_code, is_used=False).first()
    if not otp or not otp.is_valid():
        raise ValueError("Invalid or expired OTP")
    otp.is_used = True
    otp.save()


def activate_user(user):
    user.is_active = True
    user.save()


def generate_jwt_tokens(user):
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    return access_token, refresh


def set_jwt_cookie(response, refresh):
    return set_refresh_token_cookie(response, refresh)


# authentication/utils.py
