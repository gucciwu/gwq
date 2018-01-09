from base.views import BaseViewSet, BaseAPIView
from .models import Security, Type
from .serializers import SecurityTypeSerializer, SecuritySerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.decorators import detail_route, list_route
import logging


class SecurityViewSet(BaseViewSet):
    """
    API endpoint that allows security entries to be viewed or edited.
    """
    queryset = Security.objects.all().order_by('modified_at')
    serializer_class = SecuritySerializer

    logger = logging.getLogger(__name__)

    @list_route()
    def sync(self, *args, **kwargs):
        import tushare as ts
        stocks = ts.get_stock_basics()
        login_user = self.request.user
        type_of_stock = Type.objects.get_or_create(code='stock', owner=login_user,
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


class SecurityTypeViewSet(BaseViewSet):
    """
    API endpoint that allows security type entries to be viewed or edited.
    """
    queryset = Type.objects.all().order_by('modified_at')
    serializer_class = SecurityTypeSerializer


class SecuritySync(BaseAPIView):
    """
    Sync security information
    """
    def post(self):
        return Response(self.sync())

    @api_view(['GET', 'POST'])
    def sync(self):
        import tushare as ts
        stocks = ts.get_stock_basics()
        type_of_stock = Type.objects.get_or_create(code='stock')[0]

        for stock in stocks:
            security = Security()
            security.code = stock.code
            security.name = stock.name
            security.area = stock.area
            security.industry = stock.industry
            security.type = type_of_stock
            security.save()

        return stocks.size
