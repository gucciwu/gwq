from base.views import BaseViewSet
from .models import Security
from dictionary.models import SecurityType
from .serializers import SecuritySerializer
from rest_framework.response import Response
from rest_framework.decorators import list_route
import logging


class SecurityViewSet(BaseViewSet):
    """
    API endpoint that allows security entries to be viewed or edited.
    """
    queryset = Security.objects.all().order_by('modified_at')
    serializer_class = SecuritySerializer

    logger = logging.getLogger(__name__)

    """
    API endpoint that sync stock information.
    """
    @list_route()
    def sync(self, *args, **kwargs):
        import tushare as ts
        stocks = ts.get_stock_basics()
        login_user = self.request.user
        type_of_stock = SecurityType.objects.get_or_create(code='stock', owner=login_user,
                                                           modified_by=login_user, created_by=login_user)[0]

        stock_base_info = stocks.loc[:, ['name', 'industry', 'area']]
        for index, row in stock_base_info.iterrows():
            security = Security()
            security.code = index
            security.name = row['name']
            security.area = row['area']
            security.industry = row['industry']
            security.type = type_of_stock
            security.set_user(login_user)
            security.save()

        return Response(stocks.size)


