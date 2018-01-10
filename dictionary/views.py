from dictionary.models import SecurityType
from security.serializers import SecurityTypeSerializer
from .models import System
from base.views import BaseViewSet
from .serializers import DictionarySerializer


class DictionaryViewSet(BaseViewSet):
    """
    API endpoint that allows dictionary entries to be viewed or edited.
    """
    queryset = System.objects.all().order_by('modified_at')
    serializer_class = DictionarySerializer


class SecurityTypeViewSet(BaseViewSet):
    """
    API endpoint that allows security type entries to be viewed or edited.
    """
    queryset = SecurityType.objects.all().order_by('modified_at')
    serializer_class = SecurityTypeSerializer