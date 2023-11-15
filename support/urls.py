from django.urls import path
from . import views

urlpatterns = [
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
    # Categories
    path(
        "categories/",
        views.CategoryViewSet.as_view({"get": "list", "post": "create"}),
        name="category-list",
    ),
    path(
        "categories/<slug:slug>/",  # Use slug in the URL pattern
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
    # Versioned Articles
    path(
        "<str:version>/articles/",
        views.ArticleViewSet.as_view({"get": "list"}),
        name="article-list-versioned",
    ),
    path(
        "<str:version>/articles/category/<slug:category_slug>/",
        views.ArticleViewSet.as_view({"get": "articles_by_category"}),
        name="articles-by-category",
    ),
    path(
        "<str:version>/articles/<int:pk>/",
        views.ArticleViewSet.as_view({"get": "retrieve"}),
        name="article-detail-versioned",
    ),
    path(
        "<str:version>/articles/<slug:slug>/",
        views.ArticleViewSet.as_view({"get": "retrieve"}),
        name="article-detail-versioned-slug",
    ),
    # Versioned FAQ list view
    path(
        "<str:version>/faqs/",
        views.FAQViewSet.as_view({"get": "list"}),
        name="faq-list-versioned",
    ),
    # FAQ detail view with version
    path(
        "<str:version>/faqs/<int:pk>/",
        views.FAQViewSet.as_view({"get": "retrieve"}),
        name="faq-detail-versioned",
    ),
    path(
        "<str:version>/privacy-policies/",
        views.PrivacyPolicyViewSet.as_view({"get": "retrieve"}),
        name="privacypolicy-detail-versioned",
    ),
    # Terms and Conditions
    path(
        "<str:version>/terms-and-conditions/",
        views.TermsAndConditionsViewSet.as_view({"get": "retrieve"}),
        name="termsandconditions-detail-versioned",
    ),
]

# support/urls.py
