from django.http import Http404
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from django.db.models import Q
from rest_framework import filters
from .utils import get_latest_version
from .models import (
    Category,
    Ticket,
    TicketResponse,
    Tag,
    AppVersion,
    Article,
    FAQ,
    Ticket,
    TermsAndConditions,
    PrivacyPolicy,
)
from .serializers import (
    CategorySerializer,
    TicketSerializer,
    TicketResponseSerializer,
    TagSerializer,
    AppVersionSerializer,
    ArticleSerializer,
    FAQSerializer,
    TermsAndConditionsSerializer,
    PrivacyPolicySerializer,
)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class AppVersionViewSet(viewsets.ModelViewSet):
    queryset = AppVersion.objects.all()
    serializer_class = AppVersionSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "slug"

    def get_queryset(self):
        """
        Optionally restricts the returned categories to only parent categories,
        by filtering against a 'is_parent' query parameter in the URL.
        """
        queryset = super().get_queryset()
        is_parent = self.request.query_params.get("is_parent", None)
        if is_parent is not None:
            if is_parent.lower() in ["true", "1"]:
                queryset = queryset.filter(parent__isnull=True)
            elif is_parent.lower() in ["false", "0"]:
                queryset = queryset.filter(parent__isnull=False)
        return queryset


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer


class TicketResponseViewSet(viewsets.ModelViewSet):
    queryset = TicketResponse.objects.all()
    serializer_class = TicketResponseSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    lookup_field = "slug"  # Use the 'slug' field to look up objects instead of 'pk'

    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "content", "category__name", "tags__name"]

    def get_queryset(self):
        queryset = Article.objects.all()
        version_prefix = self.kwargs.get("version")
        search_query = self.request.query_params.get("search", None)

        if version_prefix:
            if not version_prefix.startswith("v"):
                raise ValidationError(
                    'Version parameter is mandatory and should start with "v"'
                )
            version = get_latest_version(version_prefix.lstrip("v"))
            if not version:
                raise Http404("Version not found.")
            queryset = queryset.filter(app_version__version=version)

        if search_query:
            search_terms = search_query.split()
            query = Q()
            for term in search_terms:
                query |= Q(title__icontains=term)
                query |= Q(content__icontains=term)
                query |= Q(category__name__icontains=term)
                query |= Q(tags__name__icontains=term)
            queryset = queryset.filter(query).distinct()

        return queryset

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        slug = self.kwargs.get("slug")
        pk = self.kwargs.get("pk")

        if slug:
            obj = get_object_or_404(queryset, slug=slug)
        elif pk:
            obj = get_object_or_404(queryset, pk=pk)
        else:
            raise Http404("No slug or ID provided for lookup.")

        self.check_object_permissions(self.request, obj)
        return obj

    @action(
        detail=False, methods=["get"], url_path="category/(?P<category_slug>[-\w]+)"
    )
    def articles_by_category(self, request, version, category_slug=None):
        """
        Retrieve articles by category slug and version.
        """
        if not category_slug:
            return Response(
                {"detail": "Category slug not provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Retrieve the version and filter articles
        if not version.startswith("v"):
            raise ValidationError(
                'Version parameter is mandatory and should start with "v"'
            )

        version = get_latest_version(version.lstrip("v"))
        if not version:
            raise Http404("Version not found.")

        articles = Article.objects.filter(
            category__slug=category_slug, app_version__version=version
        )

        page = self.paginate_queryset(articles)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(articles, many=True)
        return Response(serializer.data)


class FAQViewSet(viewsets.ModelViewSet):
    serializer_class = FAQSerializer

    def get_queryset(self):
        version_prefix = self.kwargs.get("version")
        if version_prefix:
            if not version_prefix.startswith("v"):
                raise ValidationError(
                    'Version parameter is mandatory and should start with "v"'
                )
            version = get_latest_version(version_prefix.lstrip("v"))
            if not version:
                raise Http404("Version not found.")
            return FAQ.objects.filter(app_version__version=version)
        return FAQ.objects.all()


class TermsAndConditionsViewSet(viewsets.ModelViewSet):
    serializer_class = TermsAndConditionsSerializer

    def retrieve(self, request, *args, **kwargs):
        version_prefix = kwargs.get("version")
        if not version_prefix or not version_prefix.startswith("v"):
            raise ValidationError(
                'Version parameter is mandatory and should start with "v"'
            )
        version = get_latest_version(version_prefix.lstrip("v"))
        if not version:
            raise Http404("Version not found.")
        instance = get_object_or_404(TermsAndConditions, app_version__version=version)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class PrivacyPolicyViewSet(viewsets.ModelViewSet):
    serializer_class = PrivacyPolicySerializer

    def retrieve(self, request, *args, **kwargs):
        version_prefix = kwargs.get("version")
        if not version_prefix or not version_prefix.startswith("v"):
            raise ValidationError(
                'Version parameter is mandatory and should start with "v"'
            )
        version = get_latest_version(version_prefix.lstrip("v"))
        if not version:
            raise Http404("Version not found.")
        instance = get_object_or_404(PrivacyPolicy, app_version__version=version)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


# support/views.py
