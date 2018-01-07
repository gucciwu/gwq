from .models import Dictionary
from common.views import BaseViewSet
from .serializers import DictionarySerializer


class DictionaryViewSet(BaseViewSet):
    """
    API endpoint that allows dictionary entries to be viewed or edited.
    """
    queryset = Dictionary.objects.all().order_by('modified_at')
    serializer_class = DictionarySerializer
