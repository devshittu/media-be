import logging
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

# Set up the logger for this module
logger = logging.getLogger('app_logger')


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def list(self, request, *args, **kwargs):
        logger.debug('Listing all tags')
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        logger.debug(f"Retrieving tag with id {kwargs['pk']}")
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        logger.debug('Creating a new tag')
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        logger.debug(f"Updating tag with id {kwargs['pk']}")
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        logger.debug(f"Partially updating tag with id {kwargs['pk']}")
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        logger.debug(f"Deleting tag with id {kwargs['pk']}")
        return super().destroy(request, *args, **kwargs)


class AppVersionViewSet(viewsets.ModelViewSet):
    queryset = AppVersion.objects.all()
    serializer_class = AppVersionSerializer

    def list(self, request, *args, **kwargs):
        logger.debug('Listing all app versions')
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        logger.debug(f"Retrieving app version with id {kwargs['pk']}")
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        logger.debug('Creating a new app version')
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        logger.debug(f"Updating app version with id {kwargs['pk']}")
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        logger.debug(f"Partially updating app version with id {kwargs['pk']}")
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        logger.debug(f"Deleting app version with id {kwargs['pk']}")
        return super().destroy(request, *args, **kwargs)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "slug"

    def get_queryset(self):
        """
        Optionally restricts the returned categories to only parent categories,
        by filtering against a 'is_parent' query parameter in the URL.
        """
        logger.debug('Retrieving category queryset')
        queryset = super().get_queryset()
        is_parent = self.request.query_params.get("is_parent", None)
        if is_parent is not None:
            if is_parent.lower() in ["true", "1"]:
                queryset = queryset.filter(parent__isnull=True)
                logger.debug('Filtered to parent categories only')
            elif is_parent.lower() in ["false", "0"]:
                queryset = queryset.filter(parent__isnull=False)
                logger.debug('Filtered to non-parent categories only')
        return queryset


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def list(self, request, *args, **kwargs):
        logger.debug('Listing all tickets')
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        logger.debug(f"Retrieving ticket with id {kwargs['pk']}")
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        logger.debug('Creating a new ticket')
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        logger.debug(f"Updating ticket with id {kwargs['pk']}")
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        logger.debug(f"Partially updating ticket with id {kwargs['pk']}")
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        logger.debug(f"Deleting ticket with id {kwargs['pk']}")
        return super().destroy(request, *args, **kwargs)


class TicketResponseViewSet(viewsets.ModelViewSet):
    queryset = TicketResponse.objects.all()
    serializer_class = TicketResponseSerializer

    def list(self, request, *args, **kwargs):
        logger.debug('Listing all ticket responses')
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        logger.debug(f"Retrieving ticket response with id {kwargs['pk']}")
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        logger.debug('Creating a new ticket response')
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        logger.debug(f"Updating ticket response with id {kwargs['pk']}")
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        logger.debug(
            f"Partially updating ticket response with id {kwargs['pk']}")
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        logger.debug(f"Deleting ticket response with id {kwargs['pk']}")
        return super().destroy(request, *args, **kwargs)


class ArticleViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    lookup_field = "slug"  # Use the 'slug' field to look up objects instead of 'pk'

    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "content", "category__name", "tags__name"]

    def get_queryset(self):
        logger.debug('Retrieving article queryset')
        queryset = Article.objects.all()
        version_prefix = self.kwargs.get("version")
        search_query = self.request.query_params.get("search", None)

        if version_prefix:
            if not version_prefix.startswith("v"):
                logger.error('Invalid version parameter')
                raise ValidationError(
                    'Version parameter is mandatory and should start with "v"'
                )
            version = get_latest_version(version_prefix.lstrip("v"))
            if not version:
                logger.error('Version not found')
                raise Http404("Version not found.")
            queryset = queryset.filter(app_version__version=version)
            logger.debug('Filtered articles by version')

        if search_query:
            logger.debug('Filtering articles by search query')
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
        logger.debug('Retrieving single article object')
        queryset = self.filter_queryset(self.get_queryset())
        slug = self.kwargs.get("slug")
        pk = self.kwargs.get("pk")

        if slug:
            obj = get_object_or_404(queryset, slug=slug)
            logger.debug(f'Article found by slug: {slug}')
        elif pk:
            obj = get_object_or_404(queryset, pk=pk)
            logger.debug(f'Article found by ID: {pk}')
        else:
            logger.error('No slug or ID provided for lookup')
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
        logger.debug(
            f'Retrieving articles by category {category_slug} and version {version}')
        if not category_slug:
            logger.error('Category slug not provided')
            return Response(
                {"detail": "Category slug not provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Retrieve the version and filter articles
        if not version.startswith("v"):
            logger.error('Invalid version parameter')
            raise ValidationError(
                'Version parameter is mandatory and should start with "v"'
            )

        version = get_latest_version(version.lstrip("v"))
        if not version:
            logger.error('Version not found')
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
        logger.debug('Retrieving FAQ queryset')
        version_prefix = self.kwargs.get("version")
        if version_prefix:
            if not version_prefix.startswith("v"):
                logger.error('Invalid version parameter')
                raise ValidationError(
                    'Version parameter is mandatory and should start with "v"'
                )
            version = get_latest_version(version_prefix.lstrip("v"))
            if not version:
                logger.error('Version not found')
                raise Http404("Version not found.")
            return FAQ.objects.filter(app_version__version=version)
        return FAQ.objects.all()


class TermsAndConditionsViewSet(viewsets.ModelViewSet):
    serializer_class = TermsAndConditionsSerializer

    def retrieve(self, request, *args, **kwargs):
        logger.debug('Retrieving terms and conditions')
        version_prefix = kwargs.get("version")
        if not version_prefix or not version_prefix.startswith("v"):
            logger.error('Invalid version parameter')
            raise ValidationError(
                'Version parameter is mandatory and should start with "v"'
            )
        version = get_latest_version(version_prefix.lstrip("v"))
        if not version:
            logger.error('Version not found')
            raise Http404("Version not found.")
        instance = get_object_or_404(TermsAndConditions, app_version__version=version)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class PrivacyPolicyViewSet(viewsets.ModelViewSet):
    serializer_class = PrivacyPolicySerializer

    def retrieve(self, request, *args, **kwargs):
        logger.debug('Retrieving privacy policy')
        version_prefix = kwargs.get("version")
        if not version_prefix or not version_prefix.startswith("v"):
            logger.error('Invalid version parameter')
            raise ValidationError(
                'Version parameter is mandatory and should start with "v"'
            )
        version = get_latest_version(version_prefix.lstrip("v"))
        if not version:
            logger.error('Version not found')
            raise Http404("Version not found.")
        instance = get_object_or_404(PrivacyPolicy, app_version__version=version)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


# support/views.py
