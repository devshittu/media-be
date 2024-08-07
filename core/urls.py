"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings # type: ignore
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/",
        include(
            [
                path(
                    "auth/", include("authentication.urls")
                ),  # Include the authentication app's URLs
                path("", include("stories.urls")),
                path("users/", include("users.urls")),
                path("analytics/", include("analytics.urls")),
                path("feedbacks/", include("feedback.urls")),
                path("support/", include("support.urls")),
            ]
        ),
    ),
    # path('auth/', include('rest_auth.urls')),  # URLs for dj-rest-auth
    # path('auth/registration/', include('rest_auth.registration.urls')),  # URLs for registration
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# core/urls.py
