from django.contrib import admin
from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    # Fields to be displayed in the list view
    list_display = (
        "email",
        "name",
        "username",
        "date_of_birth",
        "last_activity",
        "is_active",
        "is_staff",
    )

    # Fields that will be used for searching
    search_fields = ("email", "name", "username")

    # Fields that can be used for filtering the list view
    list_filter = ("is_active", "is_staff", "roles", "date_of_birth", "last_activity")

    # Fields to be used for editing in the list view itself
    list_editable = ("is_active", "is_staff")

    # Fields to be grouped in the form view
    fieldsets = (
        (None, {"fields": ("email", "name", "username", "password")}),
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


# Register the model with the custom admin view
admin.site.register(CustomUser, CustomUserAdmin)
