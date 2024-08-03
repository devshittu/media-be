import logging
from django.contrib import admin
from .models import (CustomUser, PasswordResetToken, OTP,
                     VerificationToken, BlacklistedToken,)


# Set up the logger for this module
logger = logging.getLogger('app_logger')


class CustomUserAdmin(admin.ModelAdmin):
    logger.debug('Initializing CustomUserAdmin class')
    # Fields to be displayed in the list view
    list_display = (
        "email",
        "display_name",
        "username",
        "date_of_birth",
        "last_activity",
        "is_active",
        "is_staff",
        "has_completed_setup",
    )

    # Fields that will be used for searching
    search_fields = ("email", "display_name", "username")

    # Fields that can be used for filtering the list view
    list_filter = ("is_active", "is_staff", "roles",
                   "date_of_birth", "last_activity")

    # Fields to be used for editing in the list view itself
    list_editable = ("is_active", "is_staff")

    # Fields to be grouped in the form view
    fieldsets = (
        (None, {"fields": ("email", "display_name", "username", "password")}),
        (
            "Personal Info",
            {
                "fields": (
                    "date_of_birth",
                    "bio",
                    "phone_number",
                    "avatar_url",
                    "display_picture",
                )
            },
        ),
        ("Permissions", {"fields": ("is_active", "is_staff", "roles")}),
        ("Activity", {"fields": ("last_activity",)}),
    )

    def save_model(self, request, obj, form, change):
        if change:
            logger.info(
                f'Updating CustomUser {obj.id} by admin {request.user.id}')
        else:
            logger.info(f'Creating new CustomUser by admin {request.user.id}')
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        logger.warning(
            f'Deleting CustomUser {obj.id} by admin {request.user.id}')
        super().delete_model(request, obj)

    def get_queryset(self, request):
        logger.debug(f'Admin {request.user.id} is querying CustomUser list')
        return super().get_queryset(request)


class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ("user", "token", "created_at")
    search_fields = ("user__email", "token")
    list_filter = ("created_at",)


class OTPAdmin(admin.ModelAdmin):
    list_display = ("user", "otp", "expires_at", "is_used", "created_at")
    search_fields = ("user__email", "otp")
    list_filter = ("is_used", "expires_at", "created_at")


class VerificationTokenAdmin(admin.ModelAdmin):
    list_display = ("user", "token", "expires_at", "created_at")
    search_fields = ("user__email", "token")
    list_filter = ("expires_at", "created_at")


class BlacklistedTokenAdmin(admin.ModelAdmin):
    list_display = ("token", "blacklisted_at")
    search_fields = ("token",)
    list_filter = ("blacklisted_at",)


# Register the models with the custom admin views
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(PasswordResetToken, PasswordResetTokenAdmin)
admin.site.register(OTP, OTPAdmin)
admin.site.register(VerificationToken, VerificationTokenAdmin)
admin.site.register(BlacklistedToken, BlacklistedTokenAdmin)

# authentication/admin.py
