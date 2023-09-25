from django.utils import timezone
from .models import CustomUser, OTP
from rest_framework_simplejwt.tokens import RefreshToken

def set_refresh_token_cookie(response, refresh):
    max_age = 3600 * 24 * 14  # 2 weeks
    response.set_cookie(
        'refresh_token', 
        str(refresh), 
        max_age=max_age, 
        secure=True, 
        httponly=True, 
        samesite='Strict'
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