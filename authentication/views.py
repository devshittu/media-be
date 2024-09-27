import jwt
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
from .tasks import send_otp_verification_email, send_link_verification_email, send_password_reset_email
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from .serializers import CustomUserRegistrationSerializer
from common.serializers import CustomUserSerializer, AuthUserSerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError, AccessToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from django.utils.crypto import get_random_string
from decouple import config
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from .utils import (
    get_valid_user,
    validate_otp,
    activate_user,
    generate_jwt_tokens,
    set_jwt_cookie,
    perform_login
)
from utils.error_codes import ErrorCode
from utils.exceptions import CustomBadRequest
from rest_framework.exceptions import ValidationError
import logging


# Set up logging
logger = logging.getLogger('app_logger')
# from users.models import UserSetting


class ObtainTokensView(APIView):
    def post(self, request):
        logger.info("ObtainTokensView: Beginning token verification")
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
        user = authenticate(
            request, username=username_or_email, password=password)

        # If authentication fails, raise an error
        if user is None:
            logger.warning("ObtainTokensView: Invalid login credentials")
            raise AuthenticationFailed(
                {
                    "code": ErrorCode.AUTHENTICATION_FAILED,
                    "detail": "Invalid login credentials",
                }
            )

        # Attach the user to the request (this makes is_authenticated work in future requests)
        request.user = user  # Ensure request.user is set after login

        # Generate tokens for the authenticated user
        # Assuming user is your authenticated user
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        # Decode the access token to get the token ID
        decoded_access_token = jwt.decode(
            access_token, settings.SECRET_KEY, algorithms=["HS256"]
        )
        token_id = decoded_access_token.get("jti")

        # Calculate expiration times
        access_token_expires_at = timezone.now() + refresh.access_token.lifetime
        access_token_expires_at_timestamp = int(
            access_token_expires_at.timestamp())
        refresh_token_expires_at_timestamp = int(
            refresh.access_token.lifetime.total_seconds())

        logger.info(f"ObtainTokensView: Token generated for user {user.id}")
        response = Response(
            {
                "access_token": access_token,
                "access_token_expires_at": access_token_expires_at_timestamp,
                "refresh_token": str(refresh),
                "refresh_token_expires_at": refresh_token_expires_at_timestamp,
                "token_id": token_id,
            }
        )

        return response


class TokenVerifyView(APIView):
    def post(self, request):
        logger.info("TokenVerifyView: Beginning token verification")
        token = request.data.get("token")

        logger.info(f"Request Body: {request.data}")

        if not token:
            logger.warning("TokenVerifyView: No token provided")
            raise AuthenticationFailed(
                {
                    "code": ErrorCode.TOKEN_NOT_PROVIDED,
                    "detail": "No token provided",
                }
            )

        try:
            AccessToken(token)  # This will validate the token
            logger.info("TokenVerifyView: Token is valid")
            # Explicitly return the expected response data
            return Response({"status": "success", "token": "valid"})

        except TokenError:
            logger.warning("TokenVerifyView: Invalid or expired access token")
            raise AuthenticationFailed(
                {
                    "code": ErrorCode.INVALID_ACCESS_TOKEN,
                    "detail": "Invalid access token or token has expired",
                }
            )


class RefreshTokenView(APIView):
    def post(self, request):
        logger.info("RefreshTokenView: log beginning token verification")

        logger.debug("This is a debug message")
        logger.info("This is an info message")
        logger.warning("This is a warning message")
        logger.error("This is an error message")

        # refresh_token = request.COOKIES.get("refresh_token")
        refresh_token = request.data.get("refresh_token")

        # Get the refresh token from the Authorization header
        # auth_header = request.headers.get("Authorization")
        # if auth_header and auth_header.startswith("Bearer "):
        #     refresh_token = auth_header.split(" ")[1]
        # else:
        #     refresh_token = None

        if not refresh_token:
            logger.warning("RefreshTokenView: No refresh token provided")
            raise AuthenticationFailed(
                {
                    "code": ErrorCode.TOKEN_NOT_PROVIDED,
                    "detail": "Refresh token not provided",
                }
            )

        # Check if the token is blacklisted
        if BlacklistedToken.objects.filter(token=refresh_token).exists():
            logger.warning("RefreshTokenView: Blacklisted refresh token used")
            raise AuthenticationFailed(
                {
                    "code": ErrorCode.BLACKLISTED_REFRESH_TOKEN,
                    "detail": "Refresh token is no longer usable",
                }
            )

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            logger.info("RefreshTokenView: New access token generated")
        except Exception as e:
            logger.error(
                f"RefreshTokenView: Error generating access token: {e}")
            raise AuthenticationFailed(
                {
                    "code": ErrorCode.INVALID_REFRESH_TOKEN,
                    "detail": "Invalid refresh token",
                }
            )

        # Calculate expiration times
        access_token_expires_at = timezone.now() + refresh.access_token.lifetime
        access_token_expires_at_timestamp = int(
            access_token_expires_at.timestamp())
        # refresh_token_expires_at_timestamp = int(
        #     refresh.access_token.lifetime.total_seconds())

        return Response(
            {
                "access_token": access_token,
                "access_token_expires_at": access_token_expires_at_timestamp,
                # "refresh_token": str(refresh),
                # "refresh_token_expires_at": refresh_token_expires_at_timestamp,
            }
        )


class PasswordResetRequestView(APIView):
    def post(self, request):
        logger.info("PasswordResetRequestView: Password reset request received")
        serializer = PasswordResetRequestSerializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            logger.warning(
                f"PasswordResetRequestView: Validation error - {str(e)}")
            raise CustomBadRequest(
                {"code": ErrorCode.INVALID_DATA, "detail": e})
            # raise CustomBadRequest(
            #     {"code": ErrorCode.INVALID_DATA, "detail": str(e)})

        email = serializer.validated_data["email"]

        user = CustomUser.objects.filter(email=email).first()
        if not user:
            logger.warning(
                f"PasswordResetRequestView: Email not found {email}")
            return Response(
                {"code": ErrorCode.EMAIL_NOT_FOUND, "detail": "Email not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Generate a token and save it
        token = get_random_string(length=32)
        PasswordResetToken.objects.create(user=user, token=token)

        # Send an email to the user with the reset link
        reset_link = f"{config('APP_FRONTEND_DOMAIN', default='http://127.0.0.1:3000/', cast=str)}auth/reset-password/{token}"

        # Send an email to the user with the reset link using the template messaging system
        # context = {"UserInfo": user, "ResetLink": reset_link}

        # Create a context with serializable data
        context = {
            "UserInfo": {
                "email": user.email,
                "display_name": user.display_name,
            },
            "UserName": user.display_name,
            "ResetLink": reset_link,
        }

        # Send an email to the user with the reset link using Celery
        send_password_reset_email.delay(user.email, context)
        logger.info(
            f"PasswordResetRequestView: Password reset email task sent to Celery for {email}")

        logger.info(
            f"PasswordResetRequestView: Password reset link sent to {email}")
        return Response({"detail": "Password reset link sent to email"})


class PasswordResetConfirmView(APIView):
    def post(self, request):
        logger.info(
            "PasswordResetConfirmView: Password reset confirmation received")

        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data["token"]
        password = serializer.validated_data["password"]

        reset_token = PasswordResetToken.objects.filter(token=token).first()
        if not reset_token or not reset_token.is_valid():
            logger.warning(
                "PasswordResetConfirmView: Invalid or expired token")
            return Response(
                {
                    "code": ErrorCode.INVALID_OR_EXPIRED_RESET_TOKEN,
                    "detail": "Invalid or expired token",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        # Set the new password for the user
        user = reset_token.user
        user.set_password(password)
        user.save()

        # Delete the token
        reset_token.delete()
        logger.info(
            f"PasswordResetConfirmView: Password reset successful for user {user.id}")

        return Response({"detail": "Password reset successful"})


class ValidateResetTokenView(APIView):
    def post(self, request):
        token = request.data.get("token")
        logger.info(f"Validating token for password reset: {token}")

        reset_token = PasswordResetToken.objects.filter(token=token).first()
        if not reset_token or not reset_token.is_valid():
            logger.warning(
                f"Invalid or expired token for password reset: {token}")
            return Response(
                {
                    "code": ErrorCode.INVALID_OR_EXPIRED_RESET_TOKEN,
                    "detail": "Invalid or expired token",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        logger.info(f"Token is valid for password reset: {token}")
        return Response(
            {"detail": "Token is valid."},
            status=status.HTTP_200_OK,
        )


class AccountActivationWithOTPView(APIView):
    """
    Ensures that the user login.
    """

    def post(self, request):
        logger.info(
            "AccountActivationWithOTPView: OTP verification request received")
        otp_code = request.data.get("otp")
        email = request.data.get("email")

        try:
            user = get_valid_user(email)
            validate_otp(user, otp_code)
            activate_user(user)

            # Perform login and get the response
            response = perform_login(user)

            logger.info(
                f"AccountActivationWithOTPView: Account activated for user {user.id}")
            return response

        except ValueError as e:
            logger.warning(
                f"AccountActivationWithOTPView: Invalid OTP for user {user.id} - {e}")
            raise CustomBadRequest(
                {"code": ErrorCode.INVALID_OTP, "detail": [str(e)]})
            # raise CustomBadRequest(detail={"otp": [str(e)]})


class PasswordlessLoginView(APIView):
    def post(self, request):
        logger.info(
            "PasswordlessLoginView: Token verification request received for login")
        otp_code = request.data.get("otp")
        email = request.data.get("email")

        try:
            user = get_valid_user(email)
            # Just verifies the token, no other action
            validate_otp(user, otp_code)
            access_token, refresh_token = generate_jwt_tokens(user)
            logger.info(
                f"PasswordlessLoginView: JWT tokens generated for user {user.id}")

            response = Response({"access_token": access_token})
            return set_jwt_cookie(response, refresh_token)

        except ValueError as e:
            logger.warning(
                f"PasswordlessLoginView: Invalid token for user {user.id} - {e}")
            raise CustomBadRequest(
                {"code": ErrorCode.INVALID_OTP, "detail": str(e)})


class OTPVerificationOnlyView(APIView):
    def post(self, request):
        logger.info(
            "OTPVerificationOnlyView: OTP verification request received")
        otp_code = request.data.get("otp")
        email = request.data.get("email")

        try:
            user = get_valid_user(email)
            validate_otp(user, otp_code)
            logger.info(
                f"OTPVerificationOnlyView: Token verified for user {user.id}")

            # This is where the frontend would redirect the user to the password reset page
            return Response({"message": "Token verified successfully!"})

        except ValueError as e:
            logger.warning(
                f"OTPVerificationOnlyView: Invalid OTP for user {user.id} - {e}")
            raise CustomBadRequest(
                {"code": ErrorCode.INVALID_OTP, "detail": str(e)})


class ResendOTPView(APIView):
    def post(self, request):
        logger.info("ResendOTPView: Resend OTP request received")
        email = request.data.get("email")

        # Fetch the user with the provided email
        user = CustomUser.objects.filter(email=email).first()
        if not user:
            logger.warning(f"ResendOTPView: Invalid email {email}")
            return Response(
                {"code": ErrorCode.INVALID_EMAIL, "detail": "Invalid email"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check if there's a recent OTP that hasn't expired
        recent_otp = user.otps.filter(
            expires_at__gt=timezone.now(), is_used=False
        ).first()
        if recent_otp:
            logger.warning(
                f"ResendOTPView: Recent OTP still valid for user {user.id}")

            return Response(
                {
                    "code": ErrorCode.RECENT_OTP_STILL_VALID,
                    "detail": "Please wait for the previous OTP to expire before requesting a new one.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

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
        send_otp_verification_email.delay(
            user.id, context)  # Trigger the Celery task
        logger.info(f"ResendOTPView: New OTP sent to user {user.id}")

        return Response({"detail": "A new OTP has been sent to your email."})


class AccountVerificationView(APIView):
    serializer_class = VerificationTokenSerializer

    def get(self, request, token):
        logger.info(
            "AccountVerificationView: Account verification request received")
        verification_token = VerificationToken.objects.filter(
            token=token).first()
        if not verification_token or not verification_token.is_valid():
            logger.warning(
                "AccountVerificationView: Invalid or expired verification link")
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
        logger.info(
            f"AccountVerificationView: Account activated for user {user.id}")
        return Response({"detail": "Account activated successfully"})


class ResendVerificationLinkView(APIView):
    def post(self, request):
        logger.info(
            "ResendVerificationLinkView: Resend verification link request received")
        email = request.data.get("email")
        user = CustomUser.objects.filter(email=email).first()

        if not user:
            logger.warning(
                f"ResendVerificationLinkView: Invalid email {email}")
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
            logger.warning(
                f"ResendVerificationLinkView: Recent verification link still valid for user {user.id}")
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
        send_link_verification_email.delay(
            user.id, context)  # Trigger the Celery task
        logger.info(
            f"ResendVerificationLinkView: Verification link sent to user {user.id}")

        return Response({"detail": "Verification link sent to email"})


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        logger.info("RegisterView: User registration request received")
        serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        if not serializer.is_valid():
            logger.warning(
                "RegisterView: User registration failed due to invalid data")
            return Response(
                {
                    "code": ErrorCode.USER_REGISTRATION_FAILED,
                    "detail": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        logger.info(
            f"RegisterView: User registration successful for user {user.id}")
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer):
        return serializer.save()


class UserListView(generics.ListCreateAPIView):
    """
    API endpoint that allows users to be viewed or created.
    """

    logger.debug('Initializing UserListView')
    queryset = get_user_model().objects.all()
    serializer_class = CustomUserSerializer


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that allows a single user to be viewed, edited, or deleted.
    """

    logger.debug('Initializing UserDetailView')
    queryset = get_user_model().objects.all()
    serializer_class = CustomUserSerializer


class CompleteSetupView(generics.UpdateAPIView):
    """
    API endpoint to mark the user's setup as complete.
    """
    logger.debug('Initializing CompleteSetupView')
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        logger.info(
            f"CompleteSetupView: Marking setup as complete for user {request.user.id}")
        user = request.user
        user.has_completed_setup = True
        user.save()
        return Response({"status": "Account setup marked as complete."})


class AuthUserView(generics.RetrieveAPIView):
    """
    View to retrieve the authenticated user's information and settings.
    """
    logger.debug('Initializing AuthUserView')
    serializer_class = AuthUserSerializer
    # permission_classes = [CustomIsAuthenticated]
    permission_classes = [CustomIsAuthenticated]

    def get_object(self):
        # Ensure the user's settings exist
        # UserSetting.objects.get_or_create(user=self.request.user)
        logger.info(
            f"AuthUserView: Retrieving authenticated user {self.request.user.id}")
        return self.request.user


class UpdatePasswordView(generics.UpdateAPIView):
    serializer_class = UpdatePasswordSerializer
    model = CustomUser
    permission_classes = [CustomIsAuthenticated]

    def get_object(self, queryset=None):
        return self.request.user

    def update(self, request, *args, **kwargs):
        logger.info(
            f"UpdatePasswordView: Password update request received for user {request.user.id}")
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Set the new password
            self.object = serializer.save()
            logger.info(
                f"UpdatePasswordView: Password updated successfully for user {request.user.id}")
            return Response(
                {"status": "success", "message": "Password updated successfully"},
                status=status.HTTP_200_OK,
            )

        logger.warning(
            f"UpdatePasswordView: Password update failed for user {request.user.id}")
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
        logger.info(
            f"LogoutView: Logout request received for user {request.user.id}")
        # Get the refresh token from the request's cookies
        refresh_token = request.COOKIES.get("refresh_token")

        # Check if the refresh_token exists
        if not refresh_token:
            logger.warning("LogoutView: Refresh token not found")
            return Response(
                {"code": ErrorCode.LOGOUT_FAILED,
                    "detail": "Refresh token not found."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # Blacklist the token
        BlacklistedToken.objects.create(token=refresh_token)

        # Clear the refresh token cookie
        response = Response({"detail": "Successfully logged out."})
        response.delete_cookie("refresh_token")
        logger.info(
            f"LogoutView: User {request.user.id} logged out successfully")

        return response


# authentication/views.py
