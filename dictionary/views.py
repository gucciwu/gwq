from .models import Dictionary
from rest_framework import viewsets
from .serializers import DictionarySerializer


class DictionaryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows dictionary entries to be viewed or edited.
    """
    queryset = Dictionary.objects.all().order_by('modified_at')
    serializer_class = DictionarySerializer

