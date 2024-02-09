from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import (
    TokenError,
    InvalidToken,
)  # Import the exceptions
from rest_framework.exceptions import AuthenticationFailed
from utils.error_codes import ErrorCode

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        try:
            return super().authenticate(request)
        except TokenError as e:
            # Check for token expiration message
            if "token_not_valid" in str(e) or "Token is invalid or expired" in str(e):
                raise AuthenticationFailed(
                    {
                        "code": ErrorCode.INVALID_ACCESS_TOKEN,
                        "detail": "Access token has expired.",
                    }
                )
            else:
                raise AuthenticationFailed(
                    {
                        "code": ErrorCode.INVALID_ACCESS_TOKEN,
                        "detail": "Invalid or expired access token.",
                    }
                )
        except InvalidToken as e:
            # Extract error details from the exception
            error_code = getattr(e, "code", ErrorCode.TOKEN_NOT_PROVIDED)
            error_detail = getattr(e, "detail", str(e))
            raise AuthenticationFailed({"code": error_code, "detail": error_detail})


    def authenticate_header(self, request):
        header = super().authenticate_header(request)
        if header is None:
            # When the header is missing or does not contain the required token
            raise AuthenticationFailed(
                {
                    "code": ErrorCode.AUTH_CREDENTIAL_NOT_PROVIDED,
                    "detail": "Authentication credentials were not provided.",
                }
            )
        return header


# utils/custom_jwt_authentication.py
