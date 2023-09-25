from django.urls import path
from users.views import UserSettingView
from rest_framework_simplejwt.views import (
    TokenVerifyView,
)
from .views import (
    RegisterView,
    CompleteSetupView,
    AuthUserView,
    ObtainTokensView,
    RefreshTokenView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
    AccountVerificationView,
    OTPVerificationWithTokenView,
    ResendOTPView,
    ResendVerificationLinkView,
    OTPVerificationOnlyView,
)


urlpatterns = [
    # Custom user auth views
    path("register/", RegisterView.as_view(), name="register"),
    path("complete_setup/", CompleteSetupView.as_view(), name="complete-setup"),
    path("me/", AuthUserView.as_view(), name="me"),
    path("me/settings/", UserSettingView.as_view(), name="user-settings"),
    path("token/", ObtainTokensView.as_view(), name="token_obtain"),
    path("token/refresh/", RefreshTokenView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path(
        "password-reset/",
        PasswordResetRequestView.as_view(),
        name="password-reset-request",
    ),
    path(
        "password-reset-confirm/",
        PasswordResetConfirmView.as_view(),
        name="password-reset-confirm",
    ),
    path("verify-otp/", OTPVerificationOnlyView.as_view(), name="verify-otp-only"),
    path(
        "verify-otp-auth/",
        OTPVerificationWithTokenView.as_view(),
        name="verify-otp-auth",
    ),
    path("resend-otp/", ResendOTPView.as_view(), name="resend-otp"),
    path(
        "verify-account/<str:token>/",
        AccountVerificationView.as_view(),
        name="verify-account",
    ),
    path(
        "resend-verification-link/",
        ResendVerificationLinkView.as_view(),
        name="resend-verification-link",
    ),
]

# authentication/urls.py
