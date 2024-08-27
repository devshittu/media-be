from django.urls import path
from users.views import UserSettingView
from .views import (
    RegisterView,
    CompleteSetupView,
    AuthUserView,
    ObtainTokensView,
    RefreshTokenView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
    ValidateResetTokenView,
    AccountVerificationView,
    AccountActivationWithOTPView,
    PasswordlessLoginView,
    ResendOTPView,
    ResendVerificationLinkView,
    OTPVerificationOnlyView,
    LogoutView,
    TokenVerifyView,
)


urlpatterns = [
    # Custom user auth views
    path("register/", RegisterView.as_view(), name="register"),
    path("complete_setup/", CompleteSetupView.as_view(), name="complete-setup"),
    path("me/", AuthUserView.as_view(), name="me"),
    path("me/settings/", UserSettingView.as_view(), name="user-settings"),
    path("logout/", LogoutView.as_view(), name="logout"),
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
    path('validate-reset-token/',
         ValidateResetTokenView.as_view(), name='validate-reset-token'),

    # Activate account using OTP
    path("otp/activate-account/", AccountActivationWithOTPView.as_view(),
         name="otp-activate-account"),

    # Login without password using OTP
    path("otp/login/", PasswordlessLoginView.as_view(), name="otp-login"),

    # General OTP verification (for password reset, etc.)
    path("otp/verify/", OTPVerificationOnlyView.as_view(), name="otp-verify"),

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
