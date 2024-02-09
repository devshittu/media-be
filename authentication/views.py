from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from utils.permissions import CustomIsAuthenticated
from .models import (
    CustomUser,
    PasswordResetToken,
    OTP,
    VerificationToken,
    BlacklistedToken,
)
from .serializers import (
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
    VerificationTokenSerializer,
    UpdatePasswordSerializer,
    UpdateUserSerializer,
)
from .utils import set_refresh_token_cookie
from .tasks import send_otp_verification_email, send_link_verification_email
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import CustomUserRegistrationSerializer
from common.serializers import CustomUserSerializer, AuthUserSerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError, AccessToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from system_messaging.utils import send_message
from django.utils.crypto import get_random_string
from decouple import config
from datetime import timedelta
from django.utils import timezone
from .utils import (
    get_valid_user,
    validate_otp,
    activate_user,
    generate_jwt_tokens,
    set_jwt_cookie,
)
from utils.error_codes import ErrorCode
from utils.exceptions import CustomBadRequest
import logging

# Set up logging
# logger = logging.getLogger(__name__)

logger = logging.getLogger("media_be")  # Use the logger defined in settings.py

# from users.models import UserSetting


class ObtainTokensView(APIView):
    def post(self, request):
        # logger.info(f"ObtainTokensView: log beginning token verification")
        # # Get the origin of the request
        # origin = request.headers.get("Origin")
        # logger.info(f"Request origin: {origin}")

        # # Log request method and path
        # logger.info(f"Request Method: {request.method}")
        # logger.info(f"Request Path: {request.path}")

        # # Log request headers
        # for header, value in request.headers.items():
        #     logger.info(f"Request Header: {header} - Value: {value}")

        # # Log request body data (be cautious with sensitive data like passwords)
        # logger.info(f"Request Body: {request.data}")

        # Extract username (or email) and password from the request data
        username_or_email = request.data.get("username_or_email")
        password = request.data.get("password")

        # Use the custom backend to authenticate the user
        user = authenticate(request, username=username_or_email, password=password)

        # If authentication fails, raise an error
        if user is None:
            raise AuthenticationFailed(
                {
                    "code": ErrorCode.AUTHENTICATION_FAILED,
                    "detail": "Invalid login credentials",
                }
            )

        # Generate tokens for the authenticated user
        refresh = RefreshToken.for_user(
            user
        )  # Assuming user is your authenticated user
        access_token = str(refresh.access_token)

        # Calculate expiration times
        access_token_expires_at = timezone.now() + refresh.access_token.lifetime
        access_token_expires_at_timestamp = int(access_token_expires_at.timestamp())

        response = Response(
            {
                "access_token": access_token,
                "access_token_expires_at": access_token_expires_at_timestamp,
            }
        )

        # Set refresh token as HttpOnly cookie
        response = set_refresh_token_cookie(response, refresh)
        return response


class TokenVerifyView(APIView):
    def post(self, request):
        logger.info(f"TokenVerifyView: log beginning token verification")
        token = request.data.get("token")

        logger.info(f"Request Body: {request.data}")

        if not token:
            raise AuthenticationFailed(
                {
                    "code": ErrorCode.TOKEN_NOT_PROVIDED,
                    "detail": "No token provided",
                }
            )

        try:
            AccessToken(token)  # This will validate the token
            # Explicitly return the expected response data
            return Response({"status": "success", "token": "valid"})

        except TokenError:
            raise AuthenticationFailed(
                {
                    "code": ErrorCode.INVALID_ACCESS_TOKEN,
                    "detail": "Invalid access token or token has expired",
                }
            )


class RefreshTokenView(APIView):
    def post(self, request):
        logger.info(f"RefreshTokenView: log beginning token verification")
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            raise AuthenticationFailed(
                {
                    "code": ErrorCode.TOKEN_NOT_PROVIDED,
                    "detail": "Refresh token not provided",
                }
            )

        # Check if the token is blacklisted
        if BlacklistedToken.objects.filter(token=refresh_token).exists():
            raise AuthenticationFailed(
                {
                    "code": ErrorCode.BLACKLISTED_REFRESH_TOKEN,
                    "detail": "Refresh token is no longer usable",
                }
            )

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
        except Exception as e:
            raise AuthenticationFailed(
                {
                    "code": ErrorCode.INVALID_REFRESH_TOKEN,
                    "detail": "Invalid refresh token",
                }
            )

        # Calculate expiration times
        access_token_expires_at = timezone.now() + refresh.access_token.lifetime
        access_token_expires_at_timestamp = int(access_token_expires_at.timestamp())

        return Response(
            {
                "access_token": access_token,
                "access_token_expires_at": access_token_expires_at_timestamp,
            }
        )


class PasswordResetRequestView(APIView):
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]

        user = CustomUser.objects.filter(email=email).first()
        if not user:
            return Response(
                {"code": ErrorCode.EMAIL_NOT_FOUND, "detail": "Email not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )
            # return Response(
            #     {"detail": "Email not found"}, status=status.HTTP_400_BAD_REQUEST
            # )

        # Generate a token and save it
        token = get_random_string(length=32)
        PasswordResetToken.objects.create(user=user, token=token)

        # Send an email to the user with the reset link
        reset_link = f"{config('APP_FRONTEND_DOMAIN', default='http://127.0.0.1:3000/', cast=str)}reset-password/{token}"

        # Send an email to the user with the reset link using the template messaging system
        context = {"UserInfo": user, "ResetLink": reset_link}
        send_message(
            "password_reset", context, user.email
        )  # Assuming 'password_reset' is the code for your template

        return Response({"detail": "Password reset link sent to email"})


class PasswordResetConfirmView(APIView):
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data["token"]
        password = serializer.validated_data["password"]

        reset_token = PasswordResetToken.objects.filter(token=token).first()
        if not reset_token or not reset_token.is_valid():
            return Response(
                {
                    "code": ErrorCode.INVALID_OR_EXPIRED_RESET_TOKEN,
                    "detail": "Invalid or expired token",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
            # return Response(
            #     {"detail": "Invalid or expired token"},
            #     status=status.HTTP_400_BAD_REQUEST,
            # )

        # Set the new password for the user
        user = reset_token.user
        user.set_password(password)
        user.save()

        # Delete the token
        reset_token.delete()

        return Response({"detail": "Password reset successful"})


class OTPVerificationWithTokenView(APIView):
    def post(self, request):
        otp_code = request.data.get("otp")
        email = request.data.get("email")

        try:
            user = get_valid_user(email)
            validate_otp(user, otp_code)
            activate_user(user)
            access_token, refresh = generate_jwt_tokens(user)

            response = Response(
                {
                    "access_token": access_token,
                    "message": "Account activated successfully!",
                }
            )

            response = set_jwt_cookie(response, refresh)
            return response

        except ValueError as e:
            raise CustomBadRequest({"code": ErrorCode.INVALID_OTP, "detail": [str(e)]})
            # raise CustomBadRequest(detail={"otp": [str(e)]})


class OTPVerificationOnlyView(APIView):
    def post(self, request):
        otp_code = request.data.get("otp")
        email = request.data.get("email")

        try:
            user = get_valid_user(email)
            validate_otp(user, otp_code)
            activate_user(user)

            return Response({"message": "Account activated successfully!"})

        except ValueError as e:
            raise CustomBadRequest({"code": ErrorCode.INVALID_OTP, "detail": str(e)})
            # return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ResendOTPView(APIView):
    def post(self, request):
        email = request.data.get("email")

        # Fetch the user with the provided email
        user = CustomUser.objects.filter(email=email).first()
        if not user:
            return Response(
                {"code": ErrorCode.INVALID_EMAIL, "detail": "Invalid email"},
                status=status.HTTP_400_BAD_REQUEST,
            )
            # return Response(
            #     {"detail": "Invalid email"}, status=status.HTTP_400_BAD_REQUEST
            # )

        # Check if there's a recent OTP that hasn't expired
        recent_otp = user.otps.filter(
            expires_at__gt=timezone.now(), is_used=False
        ).first()
        if recent_otp:
            return Response(
                {
                    "code": ErrorCode.RECENT_OTP_STILL_VALID,
                    "detail": "Please wait for the previous OTP to expire before requesting a new one.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
            # return Response(
            #     {
            #         "detail": "Please wait for the previous OTP to expire before requesting a new one."
            #     },
            #     status=status.HTTP_400_BAD_REQUEST,
            # )

        # Generate new OTP
        otp_code = get_random_string(length=6, allowed_chars="0123456789")
        otp = OTP.objects.create(
            user=user,
            otp=otp_code,
            expires_at=timezone.now()
            + timedelta(minutes=10),  # OTP valid for 10 minutes
        )

        # Send OTP to user's email
        context = {
            "UserName": user.display_name,
            "OTP_CODE": otp.otp,
            "PlatformName": config("APP_NAME", default="App Name", cast=str),
        }
        send_otp_verification_email.delay(user.id, context)  # Trigger the Celery task

        return Response({"detail": "A new OTP has been sent to your email."})


class AccountVerificationView(APIView):
    serializer_class = VerificationTokenSerializer

    def get(self, request, token):
        verification_token = VerificationToken.objects.filter(token=token).first()
        if not verification_token or not verification_token.is_valid():
            return Response(
                {
                    "code": ErrorCode.INVALID_VERIFICATION_LINK,
                    "detail": "Invalid or expired verification link",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
            # return Response(
            #     {"detail": "Invalid or expired verification link"},
            #     status=status.HTTP_400_BAD_REQUEST,
            # )

        # Activate user
        user = verification_token.user
        user.is_active = True
        user.save()

        # Delete the token
        verification_token.delete()

        return Response({"detail": "Account activated successfully"})


class ResendVerificationLinkView(APIView):
    def post(self, request):
        email = request.data.get("email")
        user = CustomUser.objects.filter(email=email).first()

        if not user:
            return Response(
                {"code": ErrorCode.INVALID_EMAIL, "detail": "Invalid email"},
                status=status.HTTP_400_BAD_REQUEST,
            )
            # return Response(
            #     {"detail": "Invalid email"}, status=status.HTTP_400_BAD_REQUEST
            # )

        # Check if there's a recent verification token that hasn't expired
        recent_token = VerificationToken.objects.filter(
            user=user, expires_at__gt=timezone.now()
        ).first()

        if recent_token:
            return Response(
                {
                    "code": ErrorCode.RECENT_OTP_STILL_VALID,
                    "detail": "Please wait for the previous verification link to expire before requesting a new one.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
            # return Response(
            #     {
            #         "detail": "Please wait for the previous verification link to expire before requesting a new one."
            #     },
            #     status=status.HTTP_400_BAD_REQUEST,
            # )

        # Generate a new verification token and save it
        token = get_random_string(length=32)
        verification_token = VerificationToken.objects.create(
            user=user,
            token=token,
            expires_at=timezone.now()
            + timedelta(hours=24),  # Token is valid for 24 hours
        )

        # Send an email to the user with the verification link
        verification_link = f"{config('APP_FRONTEND_DOMAIN', default='http://127.0.0.1:3000/', cast=str)}verify-account/{token}"

        context = {
            "UserName": user.display_name,
            "VerificationLink": verification_link,
            "PlatformName": config("APP_NAME", default="App Name", cast=str),
        }
        send_link_verification_email.delay(user.id, context)  # Trigger the Celery task

        return Response({"detail": "Verification link sent to email"})


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        if not serializer.is_valid():
            return Response(
                {
                    "code": ErrorCode.USER_REGISTRATION_FAILED,
                    "detail": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer):
        return serializer.save()


class UserListView(generics.ListCreateAPIView):
    """
    API endpoint that allows users to be viewed or created.
    """

    queryset = get_user_model().objects.all()
    serializer_class = CustomUserSerializer


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that allows a single user to be viewed, edited, or deleted.
    """

    queryset = get_user_model().objects.all()
    serializer_class = CustomUserSerializer


class CompleteSetupView(generics.UpdateAPIView):
    """
    API endpoint to mark the user's setup as complete.
    """

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        user = request.user
        user.has_completed_setup = True
        user.save()
        return Response({"status": "Account setup marked as complete."})


class AuthUserView(generics.RetrieveAPIView):
    """
    View to retrieve the authenticated user's information and settings.
    """

    serializer_class = AuthUserSerializer
    # permission_classes = [CustomIsAuthenticated]
    permission_classes = [CustomIsAuthenticated]

    def get_object(self):
        # Ensure the user's settings exist
        # UserSetting.objects.get_or_create(user=self.request.user)
        return self.request.user


class UpdatePasswordView(generics.UpdateAPIView):
    serializer_class = UpdatePasswordSerializer
    model = CustomUser
    permission_classes = [CustomIsAuthenticated]

    def get_object(self, queryset=None):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Set the new password
            self.object = serializer.save()
            return Response(
                {"status": "success", "message": "Password updated successfully"},
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateUserView(generics.UpdateAPIView):
    serializer_class = UpdateUserSerializer
    model = CustomUser
    permission_classes = [CustomIsAuthenticated]

    def get_object(self):
        return self.request.user


class LogoutView(APIView):
    permission_classes = [CustomIsAuthenticated]

    def post(self, request):
        # Get the refresh token from the request's cookies
        refresh_token = request.COOKIES.get("refresh_token")

        # Check if the refresh_token exists
        if not refresh_token:
            return Response(
                {"code": ErrorCode.LOGOUT_FAILED, "detail": "Refresh token not found."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # Blacklist the token
        BlacklistedToken.objects.create(token=refresh_token)

        # Clear the refresh token cookie
        response = Response({"detail": "Successfully logged out."})
        response.delete_cookie("refresh_token")

        return response


# authentication/views.py
