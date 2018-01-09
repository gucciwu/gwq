from .models import Dictionary, SecurityType, Security
from base.views import BaseViewSet
from .serializers import DictionarySerializer, SecurityTypeSerializer, SecuritySerializer


class DictionaryViewSet(BaseViewSet):
    """
    API endpoint that allows dictionary entries to be viewed or edited.
    """
    queryset = Dictionary.objects.all().order_by('modified_at')
    serializer_class = DictionarySerializer


class SecurityViewSet(BaseViewSet):
    """
    API endpoint that allows security entries to be viewed or edited.
    """
    queryset = Security.objects.all().order_by('modified_at')
    serializer_class = SecuritySerializer


class SecurityTypeViewSet(BaseViewSet):
    """
    API endpoint that allows security type entries to be viewed or edited.
    """
    queryset = SecurityType.objects.all().order_by('modified_at')
    serializer_class = SecurityTypeSerializer
