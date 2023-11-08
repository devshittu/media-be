from django.urls import path
from . import views

urlpatterns = [
    # Categories
    path(
        "categories/",
        views.CategoryViewSet.as_view({"get": "list", "post": "create"}),
        name="category-list",
    ),
    path(
        "categories/<int:pk>/",
        views.CategoryViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="category-detail",
    ),
    # Tickets
    path(
        "tickets/",
        views.TicketViewSet.as_view({"get": "list", "post": "create"}),
        name="ticket-list",
    ),
    path(
        "tickets/<int:pk>/",
        views.TicketViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="ticket-detail",
    ),
    # Ticket Responses
    path(
        "ticket-responses/",
        views.TicketResponseViewSet.as_view({"get": "list", "post": "create"}),
        name="ticketresponse-list",
    ),
    path(
        "ticket-responses/<int:pk>/",
        views.TicketResponseViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="ticketresponse-detail",
    ),
    # Tags
    path(
        "tags/",
        views.TagViewSet.as_view({"get": "list", "post": "create"}),
        name="tag-list",
    ),
    path(
        "tags/<int:pk>/",
        views.TagViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="tag-detail",
    ),
    # App Versions
    path(
        "app-versions/",
        views.AppVersionViewSet.as_view({"get": "list", "post": "create"}),
        name="appversion-list",
    ),
    path(
        "app-versions/<int:pk>/",
        views.AppVersionViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="appversion-detail",
    ),
    # Articles
    path(
        "articles/",
        views.ArticleViewSet.as_view({"get": "list", "post": "create"}),
        name="article-list",
    ),
    path(
        "articles/<slug:slug>/",
        views.ArticleViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="article-detail",  # This name must match the 'view_name' in your serializer's extra_kwargs
    ),
    path(
        "articles/<int:pk>/",
        views.ArticleViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="article-detail",
    ),
    # FAQs
    path(
        "faqs/",
        views.FAQViewSet.as_view({"get": "list", "post": "create"}),
        name="faq-list",
    ),
    path(
        "faqs/<int:pk>/",
        views.FAQViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="faq-detail",
    ),
    # Terms and Conditions
    path(
        "terms-and-conditions/",
        views.TermsAndConditionsViewSet.as_view({"get": "list", "post": "create"}),
        name="termsandconditions-list",
    ),
    path(
        "terms-and-conditions/<int:pk>/",
        views.TermsAndConditionsViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="termsandconditions-detail",
    ),
    # Privacy Terms
    path(
        "privacy-terms/",
        views.PrivacyTermsViewSet.as_view({"get": "list", "post": "create"}),
        name="privacyterms-list",
    ),
    path(
        "privacy-terms/<int:pk>/",
        views.PrivacyTermsViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="privacyterms-detail",
    ),
]
