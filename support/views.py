from django.shortcuts import get_object_or_404
from rest_framework import viewsets
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
    PrivacyTerms,
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
    PrivacyTermsSerializer,
)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer


class TicketResponseViewSet(viewsets.ModelViewSet):
    queryset = TicketResponse.objects.all()
    serializer_class = TicketResponseSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class AppVersionViewSet(viewsets.ModelViewSet):
    queryset = AppVersion.objects.all()
    serializer_class = AppVersionSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = "slug"  # Use the 'slug' field to look up objects instead of 'pk'

    def get_object(self):
        # Override the default method to use the slug from the URL
        queryset = self.filter_queryset(self.get_queryset())
        filter_kwargs = {self.lookup_field: self.kwargs[self.lookup_field]}
        obj = get_object_or_404(queryset, **filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj


class FAQViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer


class TermsAndConditionsViewSet(viewsets.ModelViewSet):
    queryset = TermsAndConditions.objects.all()
    serializer_class = TermsAndConditionsSerializer


class PrivacyTermsViewSet(viewsets.ModelViewSet):
    queryset = PrivacyTerms.objects.all()
    serializer_class = PrivacyTermsSerializer


class TermsAndConditionsViewSet(viewsets.ModelViewSet):
    queryset = TermsAndConditions.objects.all()
    serializer_class = TermsAndConditionsSerializer


class PrivacyTermsViewSet(viewsets.ModelViewSet):
    queryset = PrivacyTerms.objects.all()
    serializer_class = PrivacyTermsSerializer
