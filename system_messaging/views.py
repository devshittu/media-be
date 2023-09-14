from rest_framework import viewsets
from .models import MessageTemplate
from .serializers import MessageTemplateSerializer

class MessageTemplateViewSet(viewsets.ModelViewSet):
    queryset = MessageTemplate.objects.all()
    serializer_class = MessageTemplateSerializer
