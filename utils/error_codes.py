# utils/error_codes.py


class ErrorCode:
    AUTHENTICATION_FAILED = "authentication_failed"
    TOKEN_BLACKLISTED = "token_blacklisted"
    TOKEN_NOT_PROVIDED = "token_not_provided"
    AUTH_CREDENTIAL_NOT_PROVIDED = "auth_credential_not_provided"
    INVALID_ACCESS_TOKEN = "invalid_access_token"
    BLACKLISTED_REFRESH_TOKEN = "blacklisted_refresh_token"
    INVALID_REFRESH_TOKEN = "invalid_refresh_token"
    EMAIL_NOT_FOUND = "email_not_found"
    INVALID_OR_EXPIRED_TOKEN = "invalid_or_expired_token"
    INVALID_OTP = "invalid_otp"
    INVALID_EMAIL = "invalid_email"
    OTP_ALREADY_SENT = "otp_already_sent"
    INVALID_VERIFICATION_LINK = "invalid_verification_link"
    PASSWORD_UPDATE_FAILED = "password_update_failed"
    USER_UPDATE_FAILED = "user_update_failed"
    USER_REGISTRATION_FAILED = "user_registration_failed"
    LOGOUT_FAILED = "logout_failed"
    INVALID_OR_EXPIRED_RESET_TOKEN = "invalid_or_expired_reset_token"
    RECENT_OTP_STILL_VALID = "recent_otp_still_valid"
    TOKEN_NOT_VALID = "token_not_valid"

    SETTINGS_NOT_FOUND = "settings_not_found"
    SETTINGS_UPDATE_FAILED = "settings_update_failed"
    # Add more as needed


# utils/error_codes.py
